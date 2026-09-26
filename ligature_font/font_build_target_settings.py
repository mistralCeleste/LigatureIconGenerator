from dataclasses import dataclass, field
from .font_metadata_config import FontMetadataConfig


@dataclass
class FontBuildTargetSettings:
    input_dir: str
    output_dir: str
    font_family: str
    font_weight: str
    base_font_path: str
    metadata_config: FontMetadataConfig = field(default_factory=FontMetadataConfig)
