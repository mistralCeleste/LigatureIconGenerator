from dataclasses import dataclass
from typing import Optional
from datetime import date

@dataclass
class FontMetadataConfig:
    """
    Configuration model for OpenType SFNT metadata table entries.
    """
    copyright: str = "Copyright " + date.today().strftime("%Y")
    manufacturer: str = ""
    vendor_url: str = ""
    designer: str = ""
    designer_url: str = ""
    trademark: str = ""
    license_url: str = ""
    license_description: Optional[str] = ""
