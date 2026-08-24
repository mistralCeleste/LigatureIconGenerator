import os
import fontforge
from typing import Optional, List

from .unicode_block import UnicodeBlock
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
    def find_gsub_lookup(
            cls,
            font: fontforge.font,
            feature_tag: str
    ) -> str | None:
        found = None
        for lookup in font.gsub_lookups:
            if feature_tag in lookup:
                found = str(lookup)
                break
        return found


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
            lookup_type="gsub_ligature",
            flags=(),
            features=((gsub_feature_tag, (("latn", ("dflt",)),)),)
        )

        lookup = cls.find_gsub_lookup(font, gsub_feature_tag)
        if not lookup:
            lookup = table_config.lookup_name
            font.addLookup(
                table_config.lookup_name,
                table_config.lookup_type,
                table_config.flags,
                table_config.features
            )

        font.addLookupSubtable(lookup, table_config.subtable_name)
        glyph_builder = SVGGlyphBuilder(font, table_config, start_unicode)
        glyphs_info = glyph_builder.process_svg_directory(input_dir)
        glyph_builder.ensure_numeric_glyphs()
        glyph_builder.apply_standard_symbol_shortcuts()
        return glyphs_info


    @classmethod
    def export_font(
        cls,
        output_dir: str,
        font: fontforge.font,
        glyphs_info: List[GlyphInfo]
    ) -> str:
        """
        Generates OTF/TTF fonts and CSS/HTML preview files from an SVG directory.
        """
        output_path = os.path.join(output_dir, font.fontname)
        try:
            font.generate(f"{output_path}.otf")
            font.generate(f"{output_path}.ttf")
            font.generate(f"{output_path}.woff")
            font.generate(f"{output_path}.woff2") # note: requires libwoff2 binary
            DemoWebArtifactGenerator.generate_all(output_dir, font.familyname, glyphs_info)
            print(f"Font generated successfully: {output_path}")
        except Exception as e:
            print(f"Error generating font binaries: {str(e)}")
        return output_path


    @classmethod
    def create_ligature_font(
        cls,
        input_dir: str,
        output_dir: str,
        font_family: str,
        font_weight: str,
        base_font_path: str,
        feature_tag: str,
        start_unicode: int = UnicodeBlock.PUA_BASIC
    ) -> fontforge.font:
        """
        Generates OTF/TTF fonts given the font details and CSS/HTML preview files from an SVG directory.
        """
        resolved_font_path = base_font_path if os.path.isabs(base_font_path) else os.path.join(input_dir, base_font_path)
        resolved_output_dir = output_dir if os.path.isabs(output_dir) else os.path.join(input_dir, output_dir)

        if not os.path.exists(resolved_font_path):
            raise ValueError(f"Base font path does not exist: {resolved_font_path}")

        if not os.path.exists(resolved_output_dir):
            os.makedirs(resolved_output_dir)

        font = cls.load_font(font_family, font_weight, resolved_font_path)
        glyphs_info = cls.process_vectors_into_ligatures(input_dir, font, feature_tag, start_unicode)
        cls.export_font(resolved_output_dir, font, glyphs_info)
        return font
