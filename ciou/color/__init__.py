'''Library for coloring text with ANSI escapes.
'''

import re

from ._color import (
    _build_colors,
    _color,
    _Color,
    colors,
    len_without_ansi_escapes,
)
# pylint: disable-next=no-name-in-module
from ._dynamic import (
    fg_black, fg_red, fg_green, fg_yellow,
    fg_blue, fg_magenta, fg_cyan, fg_white,
    bg_black, bg_red, bg_green, bg_yellow,
    bg_blue, bg_magenta, bg_cyan, bg_white,
    fg_hi_black, fg_hi_red, fg_hi_green, fg_hi_yellow,
    fg_hi_blue, fg_hi_magenta, fg_hi_cyan, fg_hi_white,
    bg_hi_black, bg_hi_red, bg_hi_green, bg_hi_yellow,
    bg_hi_blue, bg_hi_magenta, bg_hi_cyan, bg_hi_white,
    names,
)

Color = _Color
'''Type for color functions.'''

bold = _color(1, "bold")
no_color = _color(0)
no_color.__doc__ = """No-operation color function.

Returns the *text* parameter without any modifications.
"""


def color_palette():
    '''Create a string that demonstrates all available colors.
    '''
    _colors = _build_colors()

    def _text(key: str):
        if key.startswith("bg_"):
            return ""
        return key.split("_", 1)[1]

    output = ""
    for pattern in ['bg_[^h]', 'fg_[^h]', 'bg_hi_', 'fg_hi_',]:
        row = [(color, _text(key),)
               for key, color in _colors.items() if re.match(pattern, key)]
        output += f"{bold(pattern.split('_', 1)[0])}_ "
        for color, text in row:
            output += color(f' {text:11}')
        output += "\n"

    return output[:-1]


__all__ = [
    "Color",
    "colors",
    "len_without_ansi_escapes",
    "bold",
    "no_color",
    *names,
    "color_palette"]
