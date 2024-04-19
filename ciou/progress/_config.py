from dataclasses import dataclass, field
import os
from sys import stderr
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


@dataclass()
class OutputConfig:
    default_text_width: int = 100
    '''Fallback value for terminal width in case determining terminal size
    fails.'''
    disable_animation: bool = False
    '''Print started message instead of a progress spinner.'''
    disable_colors: bool = False
    '''Do not render colors regardless of other color related configuration
    options.'''
    force_colors: bool = False
    '''Render colors even if user has `NO_COLOR` environment variable set.
    Overrides `disable_colors`.'''
    show_status_indicator: bool = True
    '''Show status indicator before the message.'''
    status_indicator_map: Dict[MessageStatus, str] = field(
        default_factory=default_status_indicator_map)
    '''Maps `MessageStatus` to a status indicator.'''
    fallback_status_indicator_map: Dict[MessageStatus, str] = field(
        default_factory=default_fallback_status_indicator_map)
    '''Overrides indicators defined in `status_indicator_map` when `fallback`
    returns `True`.'''
    status_color_map: Dict[MessageStatus, color.Color] = field(
        default_factory=default_status_color_map)
    '''Maps `MessageStatus` to a color.'''
    in_progress_animation: List[str] = field(
        default_factory=default_in_progress_animation)
    '''Animation frames for in-progress animation.'''
    fallback_in_progress_animation: List[str] = field(
        default_factory=default_fallback_in_progress_animation)
    '''Overrides frames defined in `in_progress_animation` when `fallback`
    returns `True`..'''
    unknown_color: color.Color = color.fg_white
    '''Color to use for unknown message status.'''
    unknown_indicator: str = "?"
    '''Indicator to use for unknown message status.'''
    details_color: color.Color = color.fg_hi_black
    '''Color to use for message details.'''
    color_message: bool = False
    '''Render message text with status color.'''
    stop_watch_color: color.Color = color.fg_hi_black
    '''Color to use for stopwatch.'''
    show_stopwatch: bool = True
    '''Render the task duration after message.'''
    target: TextIO = stderr
    '''Target file where to render the messages. By default `stderr`.'''

    @property
    def fallback(self):
        '''Returns `True` if current terminal is a Windows terminal that is
        not likely capable of rendering unicode characters.
        '''
        if is_windows_terminal and not is_unicode_safe_windows_term_program:
            return True

        return False

    @property
    def show_animation(self):
        '''Returns `True` if target is TTY and animation is not disabled.
        '''
        return self.max_height > 0 and not self.disable_animation

    def _get_color(self, color_: color.Color):
        if self.force_colors:
            return color_

        if self.disable_colors or os.getenv("NO_COLOR"):
            return color.no_color

        return color_

    def get_status_color(self, status: MessageStatus):
        '''Return the color to use for status indicator.
        '''
        color = self.status_color_map.get(status, self.unknown_color)
        return self._get_color(color)

    def get_details_color(self):
        '''Return the color to use for message details.
        '''
        return self._get_color(self.details_color)

    def get_stop_watch_color(self):
        '''Return the color to use for stopwatch.
        '''
        return self._get_color(self.stop_watch_color)

    def get_status_indicator(self, status: MessageStatus):
        '''Return the status indicator for given status.
        '''
        indicator = self.status_indicator_map.get(
            status, self.unknown_indicator)

        if self.fallback:
            self.fallback_status_indicator_map.get(status, indicator)

        return indicator

    def get_in_progress_animation_frame(self, index: int):
        '''Return the in-progress animation frame.

        Args:
            index: Animation render index that will be used as a basis for
                calculating the current frame: `index % len(animation)`.
        '''
        animation = self.in_progress_animation

        if self.fallback:
            animation = self.fallback_in_progress_animation

        i = index % len(animation)
        return animation[i]

    def get_dimensions(self) -> os.terminal_size:
        '''Returns the dimensions of the target terminal.

        See `max_width` and `max_height` for default values in case that
        determining terminal dimension failed.
        '''
        try:
            i = self.target.fileno()
            return os.get_terminal_size(i)
        except OSError:
            return os.terminal_size((self.default_text_width, 0,))

    @property
    def max_width(self) -> int:
        '''Returns target terminals width.

        If determining terminal dimensions failed, returns default value from
        OutputConfig.
        '''
        return self.get_dimensions().columns

    @property
    def max_height(self):
        '''Returns target terminals height.

        If determining terminal dimensions failed, returns zero.
        '''
        return self.get_dimensions().lines
