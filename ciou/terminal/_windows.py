import os
import platform
from typing import TextIO

UNICODE_SAFE_WINDOWS_TERM_PROGRAMS = ["vscode"]


def is_windows_terminal(target: TextIO) -> bool:
    if platform.system() != "Windows":
        return False

    return target.isatty()


def is_unicode_safe_windows_term_program() -> bool:
    term_prog = os.getenv("TERM_PROGRAM")
    return term_prog in UNICODE_SAFE_WINDOWS_TERM_PROGRAMS
