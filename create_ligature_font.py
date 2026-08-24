from ligature_font import FontBuilder, UnicodeBlock

"""
Sample script that Generates OTF/TTF/WOFF/WOFF2 fonts given the font resources
and CSS/HTML preview files from an SVG directory.

note:
- https://github.com/adobe-fonts/source-sans
- https://github.com/adobe-fonts/source-sans/raw/refs/heads/release/TTF/SourceSans3-Regular.ttf
"""


if __name__ == "__main__":
    FontBuilder.create_ligature_font(
        input_dir = r"D:\git\LigatureIconGenerator\resources",
        output_dir=r"D:\git\LigatureIconGenerator\resources\font",
        base_font_path = "./base-font/SourceSans3-Regular.ttf",
        font_family = "GameIcons",
        font_weight = "Regular",
        feature_tag = "liga",
        start_unicode = UnicodeBlock.PUA_BASIC
    )
