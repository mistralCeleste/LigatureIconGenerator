import os
from typing import List

from ..glyph_info import GlyphInfo


class HtmlShowcaseWriter:
    """Writes a browsable grid of every glyph in the generated font variant."""

    @staticmethod
    def write(
            output_dir: str,
            font_name: str,
            font_weight: str,
            glyphs_info: List[GlyphInfo]
    ) -> str:
        font_name_lower = font_name.lower()
        font_weight_lower = font_weight.lower()
        css_filename = f"{font_name_lower}-{font_weight_lower}.css"
        items_html = ""

        for info in glyphs_info:
            css_class = info.name.replace('_', '-').lower()
            full_icon_class = f"icon {font_name_lower} {font_weight_lower} {font_name_lower}-{font_weight_lower}-{css_class}"

            items_html += f"""        <div class="icon-item">
            <div class="{full_icon_class}"></div>
            <div class="icon-name">{info.name}</div>
            <div class="unicode">U+{info.unicode_value:04X}</div>
        </div>\n"""

        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{font_name} ({font_weight}) Font Demo</title>
    <link rel="stylesheet" href="{css_filename}">
    <style>
        body {{ font-family: system-ui, -apple-system, sans-serif; margin: 24px; background: #fafafa; color: #111; }}
        header {{ margin-bottom: 24px; display: flex; align-items: baseline; gap: 12px; }}
        h1 {{ margin: 0; font-size: 1.8rem; }}
        .badge {{ background: #e2e8f0; color: #334155; padding: 4px 10px; border-radius: 12px; font-size: 0.85rem; font-weight: 600; text-transform: capitalize; }}
        .icon-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 16px; }}
        .icon-item {{ display: flex; flex-direction: column; align-items: center; padding: 16px; background: #fff; border: 1px solid #e2e8f0; border-radius: 8px; transition: transform 0.1s ease, box-shadow 0.1s ease; }}
        .icon-item:hover {{ transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0,0,0,0.05); }}
        .icon {{ font-size: 40px; margin-bottom: 12px; height: 40px; display: flex; align-items: center; justify-content: center; }}
        .icon-name {{ font-size: 12px; font-weight: 500; text-align: center; color: #334155; word-break: break-word; }}
        .unicode {{ font-size: 10px; color: #94a3b8; margin-top: 4px; font-family: monospace; }}
    </style>
</head>
<body>
    <header>
        <h1>{font_name}</h1>
        <span class="badge">{font_weight}</span>
    </header>
    <p style="color: #64748b; font-size: 0.9rem;">Demonstrating {len(glyphs_info)} glyphs in this style variant.</p>
    <div class="icon-grid">
{items_html}
    </div>
</body>
</html>"""

        html_filename = f"{font_name_lower}-{font_weight_lower}_demo.html"
        html_path = os.path.join(output_dir, html_filename)

        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

        return html_path
