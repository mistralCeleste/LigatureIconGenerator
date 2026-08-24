from dataclasses import dataclass
from typing import Optional

@dataclass
class FontBuildTargetSettings:
    """Describes the target font metadata and base template font."""
    input_dir: str
    font_family: str
    font_weight: str = "Regular"
    output_dir: Optional[str] = None
    base_font_path: Optional[str] = None
