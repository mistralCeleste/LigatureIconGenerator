import os
from typing import List

from ..models import GlyphInfo



class HtmlShowcaseWriter:
    """Writes a browsable grid of every glyph in the generated font."""


    @staticmethod
    def write(input_dir: str, output_name: str, glyphs_info: List[GlyphInfo]) -> str:
        items_html = ""
        for info in glyphs_info:
            css_class = info.name.replace('_', '-').lower()
            items_html += f"""        <div class="icon-item">
            <div class="icon {output_name.lower()} {output_name.lower()}-{css_class}"></div>
            <div class="icon-name">{info.name}</div>
            <div class="unicode">U+{info.unicode_value:04X}</div>
        </div>\n"""

        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{output_name} Font Demo</title>
    <link rel="stylesheet" href="{output_name}.css">
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .icon-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(180px, 1fr)); gap: 15px; }}
        .icon-item {{ display: flex; flex-direction: column; align-items: center; padding: 12px; border: 1px solid #eee; border-radius: 6px; }}
        .icon {{ font-size: 36px; margin-bottom: 8px; }}
        .icon-name {{ font-size: 12px; text-align: center; color: #333; }}
        .unicode {{ font-size: 10px; color: #888; }}
    </style>
</head>
<body>
    <h1>{output_name} Font Demo</h1>
    <p>Demonstrating {len(glyphs_info)} available icons.</p>
    <div class="icon-grid">
{items_html}
    </div>
</body>
</html>"""

        html_path = os.path.join(input_dir, f"{output_name}_demo.html")
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        return html_path
