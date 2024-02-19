from dataclasses import dataclass, field
import os
import re
from sys import stderr
import textwrap
from typing import Dict, TextIO, List

from ciou import color
from ciou.terminal import (
    is_windows_terminal,
    is_unicode_safe_windows_term_program,
)

from ._message import MessageStatus, Message


def default_status_indicator_map():
    return {
        MessageStatus.SUCCESS: "✓",  # Check mark: U+2713
        MessageStatus.WARNING: "!",
        MessageStatus.ERROR: "✗",  # Ballot X: U+2717
        MessageStatus.STARTED: ">",
        MessageStatus.PENDING: "#",
        MessageStatus.SKIPPED: "-",
    }


def default_fallback_status_indicator_map():
    return {
        MessageStatus.SUCCESS: "√",  # Square root: U+221A
        MessageStatus.ERROR: "X",
    }


def default_status_color_map():
    return {
        MessageStatus.SUCCESS: color.fg_green,
        MessageStatus.WARNING: color.fg_yellow,
        MessageStatus.ERROR: color.fg_red,
        MessageStatus.STARTED: color.fg_blue,
        MessageStatus.PENDING: color.fg_cyan,
        MessageStatus.SKIPPED: color.fg_magenta,
    }


def default_in_progress_animation():
    return [
        "⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]


def default_fallback_in_progress_animation():
    return ["/", "-", "\\", "|"]


def elapsed_string(elapsed_seconds: float) -> str:
    if elapsed_seconds < 1:
        return ""

    if elapsed_seconds >= 999:
        return "> 999 s"

    return f"{int(elapsed_seconds):3} s"


@dataclass()
class OutputConfig:
    default_text_width: int = 100
    disable_colors: bool = False
    force_colors: bool = False
    show_status_indicator: bool = True
    status_indicator_map: Dict[MessageStatus, str] = field(
        default_factory=default_status_indicator_map)
    fallback_status_indicator_map: Dict[MessageStatus, str] = field(
        default_factory=default_fallback_status_indicator_map)
    status_color_map: Dict[MessageStatus, color.Color] = field(
        default_factory=default_status_color_map)
    in_progress_animation: List[str] = field(
        default_factory=default_in_progress_animation)
    fallback_in_progress_animation: List[str] = field(
        default_factory=default_fallback_in_progress_animation)
    unknown_color: color.Color = color.fg_white
    unknown_indicator: str = "?"
    details_color: color.Color = color.fg_hi_black
    color_message: bool = False
    stop_watch_color: color.Color = color.fg_hi_black
    show_stopwatch: bool = True
    target: TextIO = stderr

    @property
    def fallback(self):
        if is_windows_terminal and not is_unicode_safe_windows_term_program:
            return True

        return False

    def _get_color(self, color: color.Color):
        if self.force_colors:
            return color

        if self.disable_colors or os.getenv("NO_COLOR"):
            return color.no_color

        return color

    def get_status_color(self, status: MessageStatus):
        color = self.status_color_map.get(status, self.unknown_color)
        return self._get_color(color)

    def get_details_color(self):
        return self._get_color(self.details_color)

    def get_stop_watch_color(self):
        return self._get_color(self.stop_watch_color)

    def get_status_indicator(self, status: MessageStatus):
        indicator = self.status_indicator_map.get(
            status, self.unknown_indicator)

        if self.fallback:
            self.fallback_status_indicator_map.get(status, indicator)

        return indicator

    def get_in_progress_animation_frame(self, index: int):
        animation = self.in_progress_animation

        if self.fallback:
            animation = self.fallback_in_progress_animation

        i = index % len(animation)
        return animation[i]

    def get_dimensions(self) -> os.terminal_size:
        try:
            i = self.target.fileno()
            return os.get_terminal_size(i)
        except OSError:
            return os.terminal_size((self.default_text_width, 0,))

    @property
    def max_width(self) -> int:
        '''GetMaxWidth returns target terminals width

        If determining terminal dimensions failed, returns default value from
        OutputConfig.
        '''
        return self.get_dimensions().columns

    @property
    def max_height(self):
        '''GetMaxHeight returns target terminals height

        If determining terminal dimensions failed, returns zero.
        '''
        return self.get_dimensions().lines

    def format_details(self, msg: Message) -> str:
        indent = {}
        if self.show_status_indicator:
            indent = dict(initial_indent='  ', subsequent_indent='  ')

        whitespace = {}
        if "\n" in msg.details:
            whitespace = dict(expand_tabs=False, replace_whitespace=False)

        lines = msg.details.splitlines()

        return "\n" + "\n".join(textwrap.fill(
            line, width=self.max_width, **whitespace, **indent,
        ) for line in lines)

    def get_message_text(self, msg: Message, i: int) -> str:
        status = ""
        status_color = self.get_status_color(msg.status)
        if self.show_status_indicator:
            indicator = self.get_status_indicator(msg.status)
            if msg.status.in_progress and self.max_height > 0:
                indicator = self.get_in_progress_animation_frame(i)

            status = status_color(f'{indicator} ')

        elapsed = elapsed_string(msg.elapsed_seconds)
        if elapsed:
            elapsed = self.get_stop_watch_color()(f' {elapsed}')

        len_fn = color.len_without_ansi_escapes
        message = msg.message
        if msg.progress_message:
            message += f" {msg.progress_message}"

        max_message_width = self.max_width - len_fn(status) - len_fn(elapsed)
        if max_message_width < 0:
            return ""

        message = re.sub(r"\s", " ", message)
        if len(message) > max_message_width:
            message = f'{message[:max_message_width-1]}…'
        else:
            message = message.ljust(max_message_width)

        if self.color_message:
            message = status_color(message)

        details = ""
        if msg.details and msg.status.finished:
            details = self.get_details_color()(self.format_details(msg))

        return f'{status}{message}{elapsed}{details}\n'
