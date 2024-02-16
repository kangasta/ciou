from typing import Callable
from functools import reduce
import re

Color = Callable[[str], str]


class _Color:
    def __init__(self, ansi_code: int = None):
        self._ansi_code = ansi_code

    def __call__(self, text: str):
        if self._ansi_code:
            return f'\033[{self._ansi_code}m{text}\033[0m'
        return text


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


def colors(*colors: Color) -> Color:
    def color(text: str) -> str:
        text = reduce(lambda c, i: i(c), colors, text)
        return re.sub("(\033\\[0m)+", "\033[0m", text)

    return color
