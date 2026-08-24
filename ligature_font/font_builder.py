import os
import fontforge
from typing import Callable, List, Optional, Tuple

from .loaders import FontLoader, SVGGlyphLoader
from .generators import DemoWebArtifactGenerator
from .font_table_config import FontTableConfig
from .glyph_info import GlyphInfo
from .font_build_target_settings import FontBuildTargetSettings


class FontBuilder:
    """
    Maintains persistent rules (e.g., FontTableConfig) while building
    fonts across various SVG input directories and font metadata.
    """

    WEIGHT_MAP = {
        "Thin": 100,
        "ExtraLight": 200,
        "Light": 300,
        "Regular": 400,
        "Bold": 700,
        "ExtraBold": 800,
        "Black": 900
    }


    def __init__(
        self,
        font_table_config: Optional[FontTableConfig] = None
    ):
        """Initialize the builder with persistent ligature generation rules."""
        self.font_table_config = font_table_config or FontTableConfig()


    @classmethod
    def get_os2_font_weight(
        cls,
        font_weight: str
    ) -> int:
        if font_weight in cls.WEIGHT_MAP:
            return cls.WEIGHT_MAP[font_weight]
        raise ValueError(f"Invalid font weight: {font_weight}. Expected one of {list(cls.WEIGHT_MAP.keys())}")


    @staticmethod
    def _resolve_path(
        base_dir: str,
        target_path: Optional[str]
    ) -> Optional[str]:
        if not target_path:
            return None
        return target_path if os.path.isabs(target_path) else os.path.normpath(os.path.join(base_dir, target_path))

    def load_font(self, settings: FontBuildTargetSettings) -> fontforge.font:
        abs_input_dir = os.path.abspath(settings.input_dir)
        resolved_base_path = self._resolve_path(abs_input_dir, settings.base_font_path)

        if resolved_base_path and not os.path.exists(resolved_base_path):
            raise FileNotFoundError(f"Base font file does not exist: {resolved_base_path}")

        font = FontLoader.load_font(resolved_base_path)
        font.familyname = settings.font_family
        font.weight = settings.font_weight
        font.os2_weight = self.get_os2_font_weight(settings.font_weight)
        font.fontname = f"{font.familyname}-{font.weight}"
        font.fullname = f"{font.familyname} {font.weight}"
        return font


    @staticmethod
    def find_gsub_lookup(
        font: fontforge.font,
        feature_tag: str
    ) -> Optional[str]:
        for lookup in font.gsub_lookups:
            if feature_tag in lookup:
                return str(lookup)
        return None


    def process_vectors_into_ligatures(
        self,
        font: fontforge.font,
        input_dir: str
    ) -> List[GlyphInfo]:
        lookup = self.find_gsub_lookup(font, self.font_table_config.lookup_name)

        if not lookup:
            lookup = self.font_table_config.lookup_name
            font.addLookup(
                self.font_table_config.lookup_name,
                self.font_table_config.lookup_type,
                self.font_table_config.flags,
                self.font_table_config.features
            )

        font.addLookupSubtable(lookup, self.font_table_config.subtable_name)
        glyph_builder = SVGGlyphLoader(font, self.font_table_config)
        glyphs_info = glyph_builder.process_svg_directory(input_dir)
        glyph_builder.ensure_numeric_glyphs()
        glyph_builder.apply_standard_symbol_shortcuts()
        return glyphs_info


    @staticmethod
    def export_font(
        font: fontforge.font,
        output_dir: str,
        glyphs_info: List[GlyphInfo]
    ) -> str:
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        output_path = os.path.join(output_dir, font.fontname)
        try:
            font.generate(f"{output_path}.otf")
            font.generate(f"{output_path}.ttf")
            font.generate(f"{output_path}.woff")
            font.generate(f"{output_path}.woff2")
            DemoWebArtifactGenerator.generate_all(output_dir, font.familyname, font.weight, glyphs_info)
            print(f"Font successfully exported to: {output_path}")
        except Exception as e:
            print(f"Error generating font files: {str(e)}")

        return output_path


    def load_and_process_glyphs(
            self,
            font_build_settings: FontBuildTargetSettings
    ) -> Tuple[fontforge.font, List[GlyphInfo]]:
        font = self.load_font(font_build_settings)
        abs_input_dir = os.path.abspath(font_build_settings.input_dir)
        glyphs_info = self.process_vectors_into_ligatures(font, abs_input_dir)
        return font, glyphs_info


    def build(
        self,
        font_build_settings: FontBuildTargetSettings,
    ) -> None:
        """
        Builds a single font set given target build settings,
        reusing the instance's FontTableConfig settings.
        """
        abs_input_dir = os.path.abspath(font_build_settings.input_dir)
        font, glyphs_info = self.load_and_process_glyphs(font_build_settings)
        abs_output_dir = self._resolve_path(abs_input_dir, font_build_settings.output_dir) or abs_input_dir
        self.export_font(font, abs_output_dir, glyphs_info)
        font.close()


    def build_variant(
        self,
        font_build_settings: FontBuildTargetSettings,
        font_transform: Callable[[fontforge.font], None],
    ) -> None:
        """
        Builds a single font set given target build settings,
        reusing the instance's FontTableConfig settings.
        """
        abs_input_dir = os.path.abspath(font_build_settings.input_dir)
        font, glyphs_info = self.load_and_process_glyphs(font_build_settings)
        font_transform(font)
        abs_output_dir = self._resolve_path(abs_input_dir, font_build_settings.output_dir) or abs_input_dir
        self.export_font(font, abs_output_dir, glyphs_info)
        font.close()
