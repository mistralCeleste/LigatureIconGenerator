from typing import Optional


class NameSanitizer:
    """Handles character and glyph name conversions following Material conventions."""

    _NUMBER_WORDS = {
        '0': 'zero', '1': 'one', '2': 'two', '3': 'three', '4': 'four',
        '5': 'five', '6': 'six', '7': 'seven', '8': 'eight', '9': 'nine'
    }


    @classmethod
    def number_to_word(cls, num: str) -> str:
        return cls._NUMBER_WORDS.get(str(num), str(num))


    @classmethod
    def sanitize_glyph_name(cls, name: str) -> str:
        parts = name.split('-')
        sanitized_parts = []
        for part in parts:
            if part.isdigit():
                sanitized = '_'.join(cls.number_to_word(d) for d in part)
            else:
                sanitized = part
            sanitized_parts.append(sanitized)
        return '_'.join(sanitized_parts)


    @classmethod
    def sanitize_component(cls, char: str) -> Optional[str]:
        if char == '-':
            return None
        if char.isdigit():
            return cls.number_to_word(char)
        return char
