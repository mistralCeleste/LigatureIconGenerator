from typing import List

from ..glyph_info import GlyphInfo
from .css_writer import CssStylesheetWriter
from .html_writer import HtmlShowcaseWriter


class DemoWebArtifactGenerator:
    """Generates preview CSS stylesheet and HTML showcase files."""


    @staticmethod
    def generate_all(
            output_dir: str,
            font_name: str,
            font_weight: str,
            glyphs_info: List[GlyphInfo]
    ) -> None:
        if not glyphs_info:
            return

        css_path = CssStylesheetWriter.write(output_dir, font_name, font_weight, glyphs_info)
        html_path = HtmlShowcaseWriter.write(output_dir, font_name, font_weight, glyphs_info)

        print(f"CSS generated: {css_path}")
        print(f"HTML Demo generated: {html_path}")
