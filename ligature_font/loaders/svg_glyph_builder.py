from pathlib import Path
from typing import List

from ..glyph_info import GlyphInfo
from .name_sanitizer import NameSanitizer
from ligature_font.font_table_config import FontTableConfig



class SVGGlyphLoader:
    """Imports SVG vectors and attaches bracketed GSUB ligature definitions."""


    def __init__(
            self,
            font,
            table_config: FontTableConfig
    ):
        self.font = font
        self.table_config = table_config
        self.current_unicode = table_config.start_unicode


    def process_svg_directory(self, input_dir: str) -> List[GlyphInfo]:
        svg_files = list(Path(input_dir).glob("**/*.svg"))
        glyphs_info: List[GlyphInfo] = []

        for svg_path in svg_files:
            original_name = svg_path.stem.lower()
            glyph_name = NameSanitizer.sanitize_glyph_name(original_name)

            try:
                glyph = self.font.createChar(self.current_unicode, glyph_name)
                glyphs_info.append(GlyphInfo(glyph_name, self.current_unicode))
                self.current_unicode += 1

                glyph.importOutlines(str(svg_path))
                glyph.width = 1000
                glyph.transform((1, 0, 0, 1, 0, 0))

                components = [
                    comp for char in original_name
                    if (comp := NameSanitizer.sanitize_component(char)) is not None
                ]

                if components:
                    if self.table_config.ligature_start:
                        components.insert(0, self.table_config.ligature_start)
                    if self.table_config.ligature_end:
                        components.append(self.table_config.ligature_end)
                    glyph.addPosSub(self.table_config.subtable_name, tuple(components))
                    print(f"Processed: {svg_path.name} as {glyph_name} with components [{', '.join(components)}]")

            except Exception as e:
                print(f"Error processing {svg_path.name}: {str(e)}")

        return glyphs_info


    def apply_standard_symbol_shortcuts(self):
        """Attaches ligature shortcuts for arrows and dashes if present."""
        symbol_map = {
            0x02192: ('hyphen', 'greater'),  # Right arrow ->
            0x02190: ('less', 'hyphen'),     # Left arrow <-
            0x02014: ('hyphen', 'hyphen')    # Em dash --
        }

        for char_code, sequence in symbol_map.items():
            if char_code in self.font:
                self.font[char_code].addPosSub(self.table_config.subtable_name, sequence)


    def ensure_numeric_glyphs(self):
        """Ensures word-based numbers exist in the font when using base loaders."""
        for word in range(10):
            glyph_name = NameSanitizer.number_to_word(str(word))
            if glyph_name not in self.font:
                glyph = self.font.createChar(-1, glyph_name)
                glyph.width = self.font[str(word)].width if str(word) in self.font else 500
