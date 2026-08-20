import os
import urllib.request
from typing import Optional

import fontforge


class FontLoader:
    """Handles downloading base fonts and loading FontForge font instances."""

    BASE_FONT_URL = "https://github.com/adobe-fonts/source-sans/raw/refs/heads/release/TTF/SourceSans3-Regular.ttf"


    @classmethod
    def create_empty_font(cls):
        print(f"Using an empty font")
        return fontforge.font()


    @classmethod
    def load_font(cls, base_font_path: Optional[str] = None):
        if base_font_path:
            if not os.path.exists(base_font_path):
                raise FileNotFoundError(f"Base font not found at path: {base_font_path}")
            print(f"Using base font: {base_font_path}")
            return fontforge.open(base_font_path)
        return cls.create_empty_font()


    @classmethod
    def load_font_from_url(cls, base_font_url: str, download_path: Optional[str] = None):
        """
        Downloads a font from a URL (if not already downloaded) and loads it with FontForge.
        """
        if download_path is None:
            download_path = os.path.basename(base_font_url)
            if not download_path.lower().endswith((".ttf", ".otf")):
                download_path = "downloaded_base_font.ttf"

        if not os.path.exists(download_path):
            print(f"Downloading base font from {base_font_url}...")
            urllib.request.urlretrieve(base_font_url, download_path)

        print(f"Using downloaded base font: {download_path}")
        return cls.load_font(download_path)
