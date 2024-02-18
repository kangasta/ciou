import math

from ._message import Message, MessageStore
from ._config import OutputConfig


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

    def _prepare_message(self, msg: Message, *postfix):
        key = "-".join((msg.key, *postfix))

        if key in self._finished_map:
            return ""

        self._finished_map[key] = True
        return self._config.get_message_text(msg, self._animation_index)

    def render(self, store: MessageStore):
        text = self._move_to_in_progress_start()

        finished = store.finished[self._finished_index:]
        for msg in finished:
            if msg.status.finished:
                text += self._config.get_message_text(
                    msg, self._animation_index)
        self._finished_index += len(finished)

        in_progress = store.in_progress
        count = 0
        for msg in in_progress:
            if not msg.status.in_progress:
                continue
            if self._config.max_height == 0:
                text += self._prepare_message(msg, msg.message, "started")
            else:
                if count > self._config.max_height:
                    break
                text += self._config.get_message_text(
                    msg, self._animation_index)
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
