from typing import List

from ..models import GlyphInfo
from .css_writer import CssStylesheetWriter
from .html_writer import HtmlShowcaseWriter


class DemoWebArtifactGenerator:
    """Generates preview CSS stylesheet and HTML showcase files."""


    @staticmethod
    def generate_all(input_dir: str, output_name: str, glyphs_info: List[GlyphInfo]):
        if not glyphs_info:
            return

        css_path = CssStylesheetWriter.write(input_dir, output_name, glyphs_info)
        html_path = HtmlShowcaseWriter.write(input_dir, output_name, glyphs_info)

        print(f"CSS generated: {css_path}")
        print(f"HTML Demo generated: {html_path}")
