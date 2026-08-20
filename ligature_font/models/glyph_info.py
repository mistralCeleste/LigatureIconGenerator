from dataclasses import dataclass


@dataclass(frozen=True)
class GlyphInfo:
    """Value object storing generated glyph metadata."""
    name: str
    unicode_value: int
