from ligature_font import FontBuilder, FontBuildTargetSettings


if __name__ == "__main__":
    font_builder = FontBuilder()

    font_family = "GameIcons"
    base_font_name = "SourceSans3"
    base_font_extension = "otf"
    base_font_dir = f"../source-sans-release/OTF"
    svg_input_dir = f"./resources/{font_family}"
    build_output_dir = "./.build"

    variants = [
        "Black"
        , "BlackIt"
        , "Bold"
        , "BoldIt"
        , "ExtraLight"
        , "ExtraLightIt"
        , "It"
        , "Light"
        , "LightIt"
        , "Medium"
        , "MediumIt"
        , "Regular"
        , "RegularIt"
        , "Semibold"
        , "SemiboldIt"
    ]

    print(f"Starting batch generation for {len(variants)} font variants...\n")

    for font_weight in variants:
        base_font_path = f"{base_font_dir}/{base_font_name}-{font_weight}.{base_font_extension}"

        print(f"Building variant: {font_family} ({font_weight})...")

        font_build_settings = FontBuildTargetSettings(
            input_dir=svg_input_dir,
            output_dir=build_output_dir,
            font_family=font_family,
            font_weight=font_weight,
            base_font_path=base_font_path
        )

        try:
            font_builder.build(font_build_settings)
            print(f"Successfully built: GameIcons-{font_weight}\n")
        except Exception as e:
            print(f"Failed to build GameIcons-{font_weight}: {e}\n")

    print("All builds completed!")
