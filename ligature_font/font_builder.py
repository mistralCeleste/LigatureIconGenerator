import os
import fontforge
from typing import Callable, List, Optional, Tuple

from .loaders import FontLoader, SVGGlyphLoader
from .generators import DemoWebArtifactGenerator
from .font_table_config import FontTableConfig
from .font_metadata_config import FontMetadataConfig
from .glyph_info import GlyphInfo
from .font_build_target_settings import FontBuildTargetSettings


class FontBuilder:
    """
    Maintains persistent rules (e.g., FontTableConfig) while building
    fonts across various SVG input directories and font metadata.
    """

    # OpenType OS/2 numeric weight values (usWeightClass)
    WEIGHT_MAP = {
        "Thin": 100,
        "ExtraLight": 200,
        "Light": 300,
        "Regular": 400,
        "It": 400,          # Standalone Italic defaults to Regular weight (400)
        "Italic": 400,
        "Medium": 500,
        "Semibold": 600,
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
    def get_os2_font_weight(cls, font_weight: str) -> int:
        """
        Extracts the base weight name (stripping 'It' / 'Italic')
        and looks up the OS/2 numeric weight value.
        """
        # Strip trailing 'It' or 'Italic' if present (e.g., "BoldIt" -> "Bold")
        base_weight = font_weight.replace("Italic", "").replace("It", "").strip()

        # Handle standalone "It" or "Italic"
        if not base_weight:
            base_weight = "Regular"

        if base_weight in cls.WEIGHT_MAP:
            return cls.WEIGHT_MAP[base_weight]

        raise ValueError(f"Invalid font weight: '{font_weight}'. Expected base weight to be one of {list(cls.WEIGHT_MAP.keys())}")


    @staticmethod
    def _resolve_path(
        base_dir: str,
        target_path: Optional[str]
    ) -> Optional[str]:
        if not target_path:
            return None
        return target_path if os.path.isabs(target_path) else os.path.normpath(os.path.join(base_dir, target_path))


    @staticmethod
    def apply_metadata_config(font: fontforge.font, metadata: FontMetadataConfig):
        """
        Overwrites OpenType SFNT Name table entries from a FontMetadataConfig instance.
        Purges legacy Adobe metadata IDs before appending custom organization info.
        """
        if not metadata:
            return

        # High-level FontForge attributes
        if metadata.copyright:
            font.copyright = metadata.copyright

        # Purge legacy metadata IDs (0, 7, 8, 9, 10, 11, 12, 13, 14)
        metadata_ids = [0, 7, 8, 9, 10, 11, 12, 13, 14]
        cleaned_sfnt = [
            (lang, name_id, val)
            for lang, name_id, val in font.sfnt_names
            if name_id not in metadata_ids
        ]
        font.sfnt_names = tuple(cleaned_sfnt)

        # Map metadata fields to their exact OpenType Name IDs (English US: 0x0409)
        # ID 0:  Copyright
        # ID 7:  Trademark
        # ID 8:  Manufacturer (Windows "Company")
        # ID 9:  Designer (Windows "Authors")
        # ID 11: Vendor URL
        # ID 12: Designer URL
        # ID 13: License Description
        # ID 14: License Info URL
        id_mappings = [
            (0, metadata.copyright),
            (7, metadata.trademark),
            (8, metadata.manufacturer),
            (9, metadata.designer),
            (11, metadata.vendor_url),
            (12, metadata.designer_url),
            (13, metadata.license_description),
            (14, metadata.license_url),
        ]

        for name_id, val in id_mappings:
            if val:
                font.appendSFNTName(0x0409, name_id, val)


    def load_font(self, settings: FontBuildTargetSettings) -> fontforge.font:
        abs_input_dir = os.path.abspath(settings.input_dir)
        resolved_base_path = self._resolve_path(abs_input_dir, settings.base_font_path)

        if resolved_base_path and not os.path.exists(resolved_base_path):
            raise FileNotFoundError(f"Base font file does not exist: {resolved_base_path}")

        font = FontLoader.load_font(resolved_base_path)

        # 1. Normalize weight and style strings
        raw_weight = settings.font_weight  # e.g., "ExtraLightIt", "Regular", "It"
        is_italic = "It" in raw_weight or "Italic" in raw_weight

        weight_name = raw_weight.replace("Italic", "").replace("It", "").strip()
        if not weight_name:
            weight_name = "Regular"

        if raw_weight in ["It", "Italic"]:
            ps_suffix = "Italic"
        else:
            ps_suffix = raw_weight.replace("It", "Italic")

        postscript_name = f"{settings.font_family}-{ps_suffix}"

        if weight_name == "Regular":
            subfamily_style = "Italic" if is_italic else "Regular"
        else:
            subfamily_style = f"{weight_name} Italic" if is_italic else weight_name

        full_name = f"{settings.font_family} {subfamily_style}"

        # 2. Set FontForge properties
        font.familyname = settings.font_family
        font.weight = settings.font_weight
        font.os2_weight = self.get_os2_font_weight(settings.font_weight)
        font.fontname = postscript_name
        font.fullname = full_name
        font.fontlog = ""
        font.os2_vendor = "MLSF"

        # 3. Purge ALL structural and metadata SFNT Name IDs from the base Adobe font
        # IDs 0, 1, 2, 3, 4, 6, 7, 8, 9, 10, 11, 12, 13, 14, 16, 17
        purge_ids = [0, 1, 2, 3, 4, 6, 7, 8, 9, 10, 11, 12, 13, 14, 16, 17]
        cleaned_sfnt_names = [
            (lang, name_id, val)
            for lang, name_id, val in font.sfnt_names
            if name_id not in purge_ids
        ]
        font.sfnt_names = tuple(cleaned_sfnt_names)

        # 4. Apply custom metadata (Copyright, Manufacturer/Company, Designer/Author, etc.)
        if settings.metadata_config:
            self.apply_metadata_config(font, settings.metadata_config)

        # 5. Append mandatory OpenType structural IDs (0x0409 = US English)
        font.appendSFNTName(0x0409, 3, f"3.052;MS;{postscript_name}")  # ID 3: Unique ID
        font.appendSFNTName(0x0409, 4, full_name)                       # ID 4: Full Name
        font.appendSFNTName(0x0409, 6, postscript_name)                 # ID 6: PostScript Name

        # 6. RIBBI vs Non-RIBBI logic
        is_ribbi = raw_weight in [
            "Regular",
            "It",
            "Italic",
            "RegularIt",
            "Bold",
            "BoldIt",
            "BoldItalic",
        ]

        if is_ribbi:
            # RIBBI fonts MUST ONLY use ID 1 and ID 2
            font.appendSFNTName(0x0409, 1, settings.font_family)
            font.appendSFNTName(0x0409, 2, subfamily_style)
        else:
            # Non-RIBBI fonts
            legacy_family = f"{settings.font_family} {weight_name}"
            legacy_subfamily = "Italic" if is_italic else "Regular"
            font.appendSFNTName(0x0409, 1, legacy_family)
            font.appendSFNTName(0x0409, 2, legacy_subfamily)
            font.appendSFNTName(0x0409, 16, settings.font_family)
            font.appendSFNTName(0x0409, 17, subfamily_style)

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
            font.generate(f"{output_path}.otf", flags=("opentype",))
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
