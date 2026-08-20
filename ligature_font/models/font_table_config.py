from dataclasses import dataclass, field
from typing import Tuple


@dataclass(frozen=True)
class FontTableConfig:
    """Configuration for GSUB OpenType feature tables."""
    lookup_name: str
    subtable_name: str
    lookup_type: str = "gsub_ligature"
    flags: Tuple = field(default_factory=tuple)
    features: Tuple = field(default_factory=tuple)
