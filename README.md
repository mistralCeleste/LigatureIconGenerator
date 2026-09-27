# Ligature Icon Generator

Generate OpenType and TrueType icon fonts from a directory of SVG files. Each
SVG becomes a glyph and its filename becomes the ligature name.

## Requirements

- FontForge with `ffpython` (https://github.com/fontforge/fontforge)
- A FontForge Python installation that provides the `fontforge` module
- Python 3.6 or higher
- A base font, like from https://github.com/adobe-fonts/source-sans

On Windows, the FontForge interpreter may be located at:

```text
C:\Program Files (x86)\FontForgeBuilds\bin\ffpython.exe
```

## Input files

Place SVG files in an input directory. Do not use spaces or underscores in the file name since Font Forge cannot use them.
The filename (without `.svg`) is used as the ligature name.  Any hyphens used will be removed.

For example:

```text
./glyphs/
|-- alarm.svg
|-- arrow-right.svg
|-- d6.svg
```

The generated font can then be used with ligatures such as `alarm`, `arrowright`, and `d6`.
By default, the font table config uses square brackets around the ligature name (this can be overridden).
Adobe Fonts use AGLFN GlyphNames and can be referenced at https://github.com/adobe-type-tools/agl-aglfn.

Glyphs will be created, and you can use them like `[alarm]`, `[arrowright]`, or `[d6]`, for example.

A good place to find free vector icons:
- [Game-icons.net](https://game-icons.net/) - [CC BY 3.0](https://creativecommons.org/licenses/by/3.0/). 
- [Noun Project](https://thenounproject.com/) - [Various Licenses](https://thenounproject.com/legal/terms-of-use/#icon-licenses)


## Steps

1. Get this repo
2. Create a `MyFont` folder, named with your font name
3. Put your base font there, like SourceSans3-Regular.otf 
4. Put your SVG icons in the `MyFont/glyphs` folder
5. Clone and/or edit `create_ligature_font.py` using in your own parameters
6. Run the FontForge ffpython.exe with your script
7. Get the generated font from the output directory


## Example usage


### Running the Script

Run this with FontForge's Python interpreter from the project directory:

```commandline
pushd D:/git/LigatureIconGenerator
"C:\Program Files (x86)\FontForgeBuilds\bin\ffpython.exe" .\create_ligature_font.py
```

### Using the Script

For a custom input directory, use the API directly:

```python
from ligature_font import FontBuilder, FontBuildTargetSettings, FontMetadataConfig

if __name__ == "__main__":
    font_builder = FontBuilder()

    metadata = FontMetadataConfig \
    (
        copyright="Copyright 2026"
        , trademark="Source is a trademark of Adobe."
        , license_url="http://scripts.sil.org/OFL"
    )
    
    font_build_settings = FontBuildTargetSettings \
    (
        input_dir=r"./resources/MyFont",
        output_dir = "./.build",
        font_family="MyFont",
        font_weight="Regular",
        base_font_path="../SourceSans3-Regular.otf",
        metadata_config=metadata
    )

    font_builder.build(font_build_settings)
```

`base_font_path` is a local font path/filename. A relative local font path is
resolved relative to `input_dir`. If it is omitted, the generator creates an empty font.

Glyph lookup includes sub-dirs; for example, SVG glyphs can be placed flat in the directory,
or in a sub-dir named 'glyphs', which can include more sub-dirs.

`output_dir` will place the font files, the CSS, and HTML demo files.

Note that if `feature_tag` is omitted, the generator uses the default value `liga`.
Common values to use are `liga`, `dlig`, or `calt`. Most apps have liga enabled by default.
If using anything else, custom, like 'icon', it may become unusable by standard apps,
and it must be referenced directly, like with a custom CSS reference.


### The batch script

Similar to the `create_ligature_font`, there is the `create_ligature_font_with_variants`
which is a script that generates a ligature font with all the variants.

Font Forge does not support asynchronous executions, unless in its own process due to its shared memory model.


## Output

The generator writes these files into the input directory with
`font-name` being `font_family`-`font_weight`:

```text
./output_dir/
|-- <font-name>.otf
|-- <font-name>.ttf
|-- <font-name>.woff
|-- <font-name>.woff2
|-- <font-name>.css
|-- <font-name>.html
```

The CSS and HTML files provide a simple preview of the generated ligatures.


## Note on Licensing and Attribution

The Adobe Source Sans Pro font is licensed under the SIL Open Font License, Version 1.1.
This means you may use it freely in your projects as a base font, but
- You must rename the font file to something other than 'SourceSans3' to avoid confusion.
- You must include the license file and retain the copyright notice in your distribution.

To help with licensing, copyright, and attributions, use the `FontMetadataConfig` class
to complete the metadata for your font.