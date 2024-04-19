import math
import re
import textwrap


from ciou.color import len_without_ansi_escapes

from ._message import Message, MessageStore
from ._config import OutputConfig


def elapsed_string(elapsed_seconds: float) -> str:
    if elapsed_seconds < 1:
        return ""

    if elapsed_seconds >= 999:
        return "> 999 s"

    return f"{int(elapsed_seconds):3} s"


class MessageRenderer:
    def __init__(self, config: OutputConfig):
        self._config = config
        self._finished_map = {}
        self._animation_index = 0
        self._finished_index = 0
        self._in_progress_width = 0
        self._in_progress_height = 0

    def _print(self, *args):
        return print(*args, file=self._config.target, end="")

    def _format_details(self, msg: Message) -> str:
        indent = {}
        if self._config.show_status_indicator:
            indent = dict(initial_indent='  ', subsequent_indent='  ')

        whitespace = {}
        if "\n" in msg.details:
            whitespace = dict(expand_tabs=False, replace_whitespace=False)

        lines = msg.details.splitlines()

        return "\n" + "\n".join(textwrap.fill(
            line, width=self._config.max_width, **whitespace, **indent,
        ) for line in lines)

    def render_message(self, msg: Message) -> str:
        '''Build message text based on the configuration.
        '''
        status = ""
        status_color = self._config.get_status_color(msg.status)
        if self._config.show_status_indicator:
            indicator = self._config.get_status_indicator(msg.status)
            if msg.status.in_progress and self._config.show_animation:
                indicator = self._config.get_in_progress_animation_frame(
                    self._animation_index)

            status = status_color(f'{indicator} ')

        elapsed = elapsed_string(msg.elapsed_seconds)
        if elapsed:
            elapsed = self._config.get_stop_watch_color()(f' {elapsed}')

        len_fn = len_without_ansi_escapes
        message = msg.message
        if msg.progress_message:
            message += f" {msg.progress_message}"

        max_message_width = self._config.max_width - \
            len_fn(status) - len_fn(elapsed)
        if max_message_width < 0:
            return ""

        message = re.sub(r"\s", " ", message)
        if len(message) > max_message_width:
            message = f'{message[:max_message_width-1]}…'
        else:
            message = message.ljust(max_message_width)

        if self._config.color_message:
            message = status_color(message)

        details = ""
        if msg.details and msg.status.finished:
            details = self._config.get_details_color()(
                self._format_details(msg)
            )

        return f'{status}{message}{elapsed}{details}\n'

    def _prepare_message(self, msg: Message, *postfix):
        key = "-".join((msg.key, *postfix))

        if key in self._finished_map:
            return ""

        self._finished_map[key] = True
        return self.render_message(msg)

    def render(self, store: MessageStore):
        text = self._move_to_in_progress_start()

        finished = store.finished[self._finished_index:]
        for msg in finished:
            if msg.status.finished:
                text += self.render_message(msg)
        self._finished_index += len(finished)

        in_progress = store.in_progress
        count = 0
        for msg in in_progress:
            if not msg.status.in_progress:
                continue
            if not self._config.show_animation:
                text += self._prepare_message(msg, msg.message, "started")
            else:
                if (count + 1) >= self._config.max_height:
                    break
                text += self.render_message(msg)
                count += 1

        if text:
            self._print(text)

        self._in_progress_height = count
        self._in_progress_width = self._config.max_width
        self._animation_index += 1

    def _move_to_in_progress_start(self):
        if self._in_progress_height == 0:
            return ""

        current_width = self._config.max_width
        current_height = self._in_progress_height
        if current_width < self._in_progress_width:
            current_height *= math.ceil(
                self._in_progress_width / current_width)

        return "\r" + "\033[1A\033[2K" * current_height
