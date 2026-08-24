# Ligature Icon Generator

Generate OpenType and TrueType icon fonts from a directory of SVG files. Each
SVG becomes a glyph and its filename becomes the ligature name.

## Requirements

- FontForge with `ffpython` (https://github.com/fontforge/fontforge)
- A FontForge Python installation that provides the `fontforge` module

On Windows, the interpreter may be located at:

```text
C:\Program Files (x86)\FontForgeBuilds\bin\ffpython.exe
```

## Input files

Place SVG files in an input directory. The filename (without `.svg`) is used
as the ligature name. For example:

```text
./glyphs/
|-- alarm.svg
|-- arrow-right.svg
`-- github.svg
```

The generated font can then be used with ligatures such as `alarm`,
`arrow-right`, and `github`.


## Example usage

Run this with FontForge's Python interpreter from the project directory:

```powershell
& "C:\Program Files (x86)\FontForgeBuilds\bin\ffpython.exe" `
  .\ligature_creator.py
```

For a custom input directory, use the API directly:

```python
from ligature_font import FontBuilder

FontBuilder.create_ligature_font(
    input_dir=r"C:\path\to\glyphs",
    output_dir=r"C:\path\to\compile-font-files",
    font_family="MyIcons",
    font_weight="Regular",
    base_font_path=None,
    feature_tag="liga",
    start_unicode=0xE000, # Basic Private Use Area (PUA-A)
)
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
