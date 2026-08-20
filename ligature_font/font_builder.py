import os
import fontforge
from typing import Optional, List

from .fonts import FontLoader, SVGGlyphBuilder
from .models import FontTableConfig, GlyphInfo
from .web import DemoWebArtifactGenerator

class FontBuilder:
    """Builds a font from SVG glyphs."""


    @staticmethod
    def get_os2_font_weight(
            font_weight: str
    ):
        if font_weight == "Thin":
            return 100
        if font_weight == "ExtraLight":
            return 200
        if font_weight == "Light":
            return 300
        elif font_weight == "Regular":
            return 400
        elif font_weight == "Bold":
            return 700
        elif font_weight == "ExtraBold":
            return 800
        elif font_weight == "Black":
            return 900
        else:
            raise ValueError(f"Invalid font weight: {font_weight}")


    @classmethod
    def load_font(
        cls,
        font_family: str,
        font_weight: str = "Regular",
        base_font_full_path: Optional[str] = None,
    ):
        font = FontLoader.load_font(base_font_full_path)
        font.familyname = font_family
        font.weight = font_weight
        font.os2_weight = cls.get_os2_font_weight(font_weight)
        font.fontname = f"{font_family}-{font_weight}"
        font.fullname = f"{font_family} {font_weight}"
        return font


    @classmethod
    def process_vectors_into_ligatures(
        cls,
        input_dir: str,
        font: fontforge.font,
        gsub_feature_tag: str,
        start_unicode: int
    ) -> List[GlyphInfo]:

        table_config = FontTableConfig(
            lookup_name=gsub_feature_tag,
            subtable_name=f"{gsub_feature_tag} subtable",
            features=((gsub_feature_tag, (("latn", "dflt"),)),)
        )

        font.addLookup(
            table_config.lookup_name,
            table_config.lookup_type,
            table_config.flags,
            table_config.features
        )

        font.addLookupSubtable(table_config.lookup_name, table_config.subtable_name)
        glyph_builder = SVGGlyphBuilder(font, table_config, start_unicode)
        glyphs_info = glyph_builder.process_svg_directory(input_dir)
        glyph_builder.ensure_numeric_glyphs()
        glyph_builder.apply_standard_symbol_shortcuts()
        return glyphs_info


    @classmethod
    def export_font(
        cls,
        input_dir: str,
        font: fontforge.font,
        glyphs_info: List[GlyphInfo]
    ) -> str:
        """
        Generates OTF/TTF fonts and CSS/HTML preview files from an SVG directory.
        """
        output_path = os.path.join(input_dir, font.fontname)
        try:
            font.generate(f"{output_path}.otf")
            font.generate(f"{output_path}.ttf")
            DemoWebArtifactGenerator.generate_all(input_dir, font.familyname, glyphs_info)
            print(f"Font generated successfully: {output_path}")
        except Exception as e:
            print(f"Error generating font binaries: {str(e)}")
        return output_path


    @classmethod
    def create_ligature_font(
        cls,
        input_dir: str,
        font_family: str,
        font_weight: str = "Regular",
        base_font_path: Optional[str] = None,
        feature_tag: str = "icon",
        start_unicode: int = 0xE000
    ) -> fontforge.font:
        """
        Generates OTF/TTF fonts given the font details and CSS/HTML preview files from an SVG directory.
        """
        resolved_font_path = base_font_path

        if base_font_path and not os.path.isabs(base_font_path):
            resolved_font_path = os.path.join(input_dir, base_font_path)

        font = cls.load_font(font_family, font_weight, resolved_font_path)
        glyphs_info = cls.process_vectors_into_ligatures(input_dir, font, feature_tag, start_unicode)
        cls.export_font(input_dir, font, glyphs_info)
        return font
