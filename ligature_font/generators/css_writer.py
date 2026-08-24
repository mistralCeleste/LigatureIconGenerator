import os
from typing import List

from ..glyph_info import GlyphInfo


class CssStylesheetWriter:
    """Writes the @font-face stylesheet exposing one class per glyph."""


    @staticmethod
    def write(
            output_dir: str,
            font_name: str,
            glyphs_info: List[GlyphInfo]
    ) -> str:
        font_name_lower = font_name.lower()
        css_content = f"""/* {font_name} Font CSS */
@font-face {{
    font-family: '{font_name}';
    src: url('{font_name}.woff2') format('woff2'),
         url('{font_name}.woff') format('woff'),
         url('{font_name}.ttf') format('truetype');
    font-weight: normal;
    font-style: normal;
}}

.{font_name_lower} {{
    font-family: '{font_name}';
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
            css_content += f".{font_name_lower.lower()}-{css_class}::before {{ content: '\\{info.unicode_value:04X}'; }}\n"

        css_path = os.path.join(output_dir, f"{font_name_lower}.css")
        with open(css_path, 'w', encoding='utf-8') as f:
            f.write(css_content)
        return css_path
