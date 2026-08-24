"""Building blocks for generating ligature icon fonts from SVG directories.

The pieces are assembled by ``create_ligature_font`` in ``create_ligature_font.py``.
"""

from .fonts import FontLoader, SVGGlyphBuilder
from .models import FontTableConfig, GlyphInfo
from .name_sanitizer import NameSanitizer
from .font_builder import FontBuilder
from .web import DemoWebArtifactGenerator
from .unicode_block import UnicodeBlock

__all__ = [
    "DemoWebArtifactGenerator",
    "FontLoader",
    "FontBuilder",
    "FontTableConfig",
    "GlyphInfo",
    "NameSanitizer",
    "SVGGlyphBuilder",
    "UnicodeBlock"
]
