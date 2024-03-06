import sys

from ._color import _build_colors


class _Dynamic:
    __name__ = "_dynamic"

    def __init__(self):
        self._colors = _build_colors()
        setattr(self, "names", self._colors.keys())

        for name, value in self._colors.items():
            setattr(self, name, value)


sys.modules[__name__] = _Dynamic()
