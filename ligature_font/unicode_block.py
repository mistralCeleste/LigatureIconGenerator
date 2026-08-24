from enum import IntEnum


class UnicodeBlock(IntEnum):
    """Common Unicode block starting offsets for font glyph generation."""

    # Private Use Areas
    PUA_BASIC = 0xE000  # Private Use Area (U+E000 to U+F8FF - 6,400 code points)
    PUA_A = 0xF0000  # Supplementary Private Use Area-A (U+F0000 to U+FFFFD - 65,534 code points)
    PUA_B = 0x100000  # Supplementary Private Use Area-B (U+100000 to U+10FFFD - 65,534 code points)

    # Common Symbol & Icon Ranges
    BASIC_LATIN = 0x0020  # Printable ASCII
    LATIN_1_SUPPLEMENT = 0x00A0
    GENERAL_PUNCTUATION = 0x2000
    CURRENCY_SYMBOLS = 0x20A0
    LETTERLIKE_SYMBOLS = 0x2100
    ARROWS = 0x2190
    MATHEMATICAL_OPERATORS = 0x2200
    MISC_TECHNICAL = 0x2300
    BOX_DRAWING = 0x2500
    BLOCK_ELEMENTS = 0x2580
    GEOMETRIC_SHAPES = 0x25A0
    MISC_SYMBOLS = 0x2600  # Warning signs, weather, UI elements
    DINGBATS = 0x2700
    MISC_SYMBOLS_AND_ARROWS = 0x2B00

    # Modern Emoji / Icon Font Blocks
    MISC_SYMBOLS_AND_PICTOGRAPHS = 0x1F300
    EMOTICONS = 0x1F600
    TRANSPORT_AND_MAP = 0x1F680
    SYMBOLS_AND_PICTOGRAPHS_EXT_A = 0x1FA70
