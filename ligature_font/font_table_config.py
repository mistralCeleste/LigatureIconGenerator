from dataclasses import dataclass, field
from typing import Tuple, Optional

from .unicode_block import UnicodeBlock


GlyphName = Optional[str]

@dataclass
class FontTableConfig:
    """
    Configuration for GSUB OpenType feature tables.

    Note: Adobe Fonts use AGLFN GlyphNames and can be referenced at https://github.com/adobe-type-tools/agl-aglfn.
    """
    lookup_name: str = "liga"
    subtable_name: str = "liga subtable"
    lookup_type: str = "gsub_ligature"
    start_unicode: int = UnicodeBlock.PUA_BASIC
    ligature_start: GlyphName = 'bracketleft'
    ligature_end: GlyphName = 'bracketright'
    flags: Tuple = field(default_factory=tuple)
    features: Tuple = field(default_factory=tuple)

    def __post_init__(self):
        # Auto-populate features tuple based on lookup_name if left empty
        if not self.features:
            self.features = ((self.lookup_name, (("latn", ("dflt",)),)),)
