import os
from typing import List

from ..models import GlyphInfo



class CssStylesheetWriter:
    """Writes the @font-face stylesheet exposing one class per glyph."""


    @staticmethod
    def write(input_dir: str, output_name: str, glyphs_info: List[GlyphInfo]) -> str:
        css_content = f"""/* {output_name} Font CSS */
@font-face {{
    font-family: '{output_name}';
    src: url('{output_name}.woff2') format('woff2'),
         url('{output_name}.woff') format('woff'),
         url('{output_name}.ttf') format('truetype');
    font-weight: normal;
    font-style: normal;
}}

.{output_name.lower()} {{
    font-family: '{output_name}';
    font-weight: normal;
    font-style: normal;
    font-size: 24px;
    line-height: 1;
    display: inline-block;
    direction: ltr;
    -webkit-font-smoothing: antialiased;
}}
"""
        for info in glyphs_info:
            css_class = info.name.replace('_', '-').lower()
            css_content += f".{output_name.lower()}-{css_class}::before {{ content: '\\{info.unicode_value:04X}'; }}\n"

        css_path = os.path.join(input_dir, f"{output_name}.css")
        with open(css_path, 'w', encoding='utf-8') as f:
            f.write(css_content)
        return css_path
