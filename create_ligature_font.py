from ligature_font import FontBuilder

"""
Generates OTF/TTF fonts given the font details and CSS/HTML preview files from an SVG directory.

note:
- https://github.com/adobe-fonts/source-sans
- https://github.com/adobe-fonts/source-sans/raw/refs/heads/release/TTF/SourceSans3-Regular.ttf
"""


if __name__ == "__main__":
    FontBuilder.create_ligature_font(
        input_dir = r"D:\git\LigatureIconGenerator\fontTest",
        base_font_path = "SourceSans3-Regular.ttf",
        font_family = "GameIcons",
        font_weight = "Regular",
        feature_tag = "icon",
        start_unicode = 0xE000 # Basic Private Use Area (PUA-A)
    )
