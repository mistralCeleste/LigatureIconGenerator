"""Building blocks for generating ligature icon loaders from SVG directories.

The pieces are assembled by ``create_ligature_font`` in ``create_ligature_font.py``.
"""

from .loaders import FontLoader, SVGGlyphLoader, FontTableConfig, UnicodeBlock
from .font_builder import FontBuilder
from .glyph_info import GlyphInfo
from .font_build_target_settings import FontBuildTargetSettings

__all__ = [
    "FontLoader",
    "FontBuilder",
    "FontBuildTargetSettings",
    "FontTableConfig",
    "GlyphInfo",
    "SVGGlyphLoader",
    "UnicodeBlock"
]
