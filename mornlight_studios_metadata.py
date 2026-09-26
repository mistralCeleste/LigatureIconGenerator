from dataclasses import dataclass
from typing import Optional
from ligature_font import FontMetadataConfig


@dataclass
class MornlightStudiosMetadataConfig(FontMetadataConfig):
    """
    Configuration model for OpenType SFNT metadata table entries.
    """
    copyright: str = (
        "Copyright 2026 Mornlight Studios (https://www.mornlightstudios.com/). "
        "Portions Copyright 2010-2024 Adobe (http://www.adobe.com/) under OFL-1.1 License with Reserved Font Name 'Source'. "
        "Portions of icons from GameIcons.net (https://game-icons.net/) under CC BY 3.0."
    )
    manufacturer: str = "Mornlight Studios"
    vendor_url: str = "https://www.mornlightstudios.com/"
    designer: str = "Mornlight Studios, Paul D. Hunt (Adobe), & Lorc (GameIcons)"
    designer_url: str = "https://www.mornlightstudios.com/"
    trademark: str = "Source is a trademark of Adobe."
    license_url: str = "http://scripts.sil.org/OFL"
    license_description: Optional[str] = (
        "This Font Software is licensed under the SIL Open Font License, Version 1.1. "
        "This license is available with a FAQ at: http://scripts.sil.org/OFL"
    )
