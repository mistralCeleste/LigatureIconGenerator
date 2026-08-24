import os
from typing import List

from ..glyph_info import GlyphInfo



class HtmlShowcaseWriter:
    """Writes a browsable grid of every glyph in the generated font."""


    @staticmethod
    def write(output_dir: str, font_name: str, glyphs_info: List[GlyphInfo]) -> str:
        font_name_lower = font_name.lower()
        items_html = ""
        for info in glyphs_info:
            css_class = info.name.replace('_', '-').lower()
            items_html += f"""        <div class="icon-item">
            <div class="icon {font_name_lower} {font_name_lower}-{css_class}"></div>
            <div class="icon-name">{info.name}</div>
            <div class="unicode">U+{info.unicode_value:04X}</div>
        </div>\n"""

        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{font_name_lower} Font Demo</title>
    <link rel="stylesheet" href="{font_name_lower}.css">
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
    <h1>{font_name} Font Demo</h1>
    <p>Demonstrating {len(glyphs_info)} available icons.</p>
    <div class="icon-grid">
{items_html}
    </div>
</body>
</html>"""

        html_path = os.path.join(output_dir, f"{font_name_lower}_demo.html")
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        return html_path
