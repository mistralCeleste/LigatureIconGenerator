from ligature_font import FontBuilder, FontBuildTargetSettings


"""
Sample script that Generates OTF/TTF/WOFF/WOFF2 loaders given the font resources
and CSS/HTML preview files from an SVG directory.

note:
- https://github.com/adobe-fonts/source-sans
"""


if __name__ == "__main__":
    font_builder = FontBuilder()

    font_build_settings = FontBuildTargetSettings(
        input_dir=r"./resources/GameIcons",
        output_dir = "./.build",
        font_family="GameIcons",
        font_weight="Regular",
        base_font_path="../source-sans-release/OTF/SourceSans3-Regular.otf"
    )

    font_builder.build(font_build_settings)
