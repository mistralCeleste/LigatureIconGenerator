from dataclasses import dataclass, field
from typing import Tuple


@dataclass(frozen=True)
class FontTableConfig:
    """Configuration for GSUB OpenType feature tables."""
    lookup_name: str = "icon"
    subtable_name: str = "icon subtable"
    lookup_type: str = "gsub_ligature"
    flags: Tuple = field(default_factory=tuple)
    features: Tuple = field(
        default_factory=lambda: (("icon", (("latn", "dflt"),)),)
    )
