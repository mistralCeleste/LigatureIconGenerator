from ligature_font import FontBuilder, FontBuildTargetSettings, FontTableConfig
from mornlight_studios_metadata import MornlightStudiosMetadataConfig, FontMetadataConfig


"""
Sample script that Generates OTF/TTF/WOFF/WOFF2 loaders given the font resources
and CSS/HTML preview files from an SVG directory.

note:
- https://github.com/adobe-fonts/source-sans
"""


if __name__ == "__main__":

    # Creates a font with ligatures starting with bracketleft '[' (U+005B) and ending with bracketright ']' (U+005D)
    # Adobe Fonts use AGLFN GlyphNames and can be referenced at https://github.com/adobe-type-tools/agl-aglfn.
    font_table_config = FontTableConfig(ligature_start='bracketleft', ligature_end='bracketright')

    # Initialize the font builder, one can be used for multiple font builds
    font_builder = FontBuilder(font_table_config)

    # The OFL license requires attribution, the default metadata config includes it, you can add your own.
    custom_metadata = MornlightStudiosMetadataConfig() # FontMetadataConfig(copyright="", trademark="", license_url="")

    # There can be multiple font build targets, each with different settings
    font_build_settings = FontBuildTargetSettings(
        input_dir=r"./resources/GameIcons", # location where the SVG files are located, used to make glyphs
        output_dir = "./.build", # location where the font files will be output
        font_family="GameIcons", # name of your font
        font_weight="Regular", # font weight that can be: "Regular", "Bold", "Italic", etc. see: FontBuilder.WEIGHT_MAP
        base_font_path="../source-sans-release/OTF/SourceSans3-Regular.otf", # path to the base font file
        metadata_config=custom_metadata # metadata config for attribution and licensing details
    )

    # Generate the font
    font_builder.build(font_build_settings)
