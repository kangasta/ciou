from typing import Callable
from functools import reduce
import re

_Color = Callable[[str], str]


def _color(ansi_code: int = None, name=None):
    def fn(text: str) -> str:
        if ansi_code:
            return f'\033[{ansi_code}m{text}\033[0m'
        return text

    if name:
        fn.__name__ = name
        fn.__doc__ = f"""Color the given *text* with `{name}` color.

Adds ANSI escapes to the beginning and the end of the text. E.g. `{name}`
would become `{fn(name)}`.
"""

    return fn


def _build_colors():
    type_ = dict(fg=30, bg=40, fg_hi=90, bg_hi=100)
    color = dict(
        black=0, red=1, green=2, yellow=3,
        blue=4, magenta=5, cyan=6, white=7
    )

    return {
        f"{type_key}_{color_key}": _color(
            type_value +
            color_value, f"{type_key}_{color_key}") for type_key,
        type_value in type_.items() for color_key,
        color_value in color.items()}


def colors(*colors: _Color) -> _Color:
    '''Create color function that combines multiple colors.
    '''
    def color(text: str) -> str:
        text = reduce(lambda c, i: i(c), colors, text)
        return re.sub(r"(\033\[0m)+", "\033[0m", text)

    return color


def len_without_ansi_escapes(input: str) -> int:
    '''Calculate the length of a string without ANSI escapes.

    For example, `len_without_ansi_escapes(bold("example"))` returns `7` while
    `len(bold("example"))` returns `15`.
    '''
    input_without_ansi_escapes = re.sub(r"(\033\[[0-9;]+m)", "", input)
    return len(input_without_ansi_escapes)
