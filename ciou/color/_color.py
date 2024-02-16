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


def colors(*colors: Color) -> Color:
    def color(text: str) -> str:
        text = reduce(lambda c, i: i(c), colors, text)
        return re.sub("(\033\\[0m)+", "\033[0m", text)

    return color
