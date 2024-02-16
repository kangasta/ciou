'''Library for coloring text with ANSI escapes
'''

import re

from ._color import Color, _Color, colors

bold = _Color(1)


def _build_colors():
    type_ = dict(fg=30, bg=40, fg_hi=90, bg_hi=100)
    color = dict(
        black=0, red=1, green=2, yellow=3,
        blue=4, magenta=5, cyan=6, white=7
    )

    return {
        f"{type_key}_{color_key}": _Color(
            type_value +
            color_value) for type_key,
        type_value in type_.items() for color_key,
        color_value in color.items()}


def _color_palette():
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


globals().update(_build_colors())
