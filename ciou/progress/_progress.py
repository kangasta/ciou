from queue import Queue
from threading import Thread

from ciou.time import Ticker

from ._config import OutputConfig
from ._message import MessageStore, Update
from ._renderer import MessageRenderer


SCREEN_WRITE_INTERVAL = 0.095
STOP = "_stop"


class Progress:
    def __init__(self, config: OutputConfig):
        self._renderer = MessageRenderer(config)
        self._store = MessageStore()

        self._queue = Queue()
        self._ticker = None

        self._thread = None

    def _run(self):
        while True:
            item = self._queue.get()
            if isinstance(item, Update):
                self._store.push(item)
            if item == STOP:
                self._store.close()
                self._renderer.render(self._store)
                break
            else:
                self._renderer.render(self._store)

    def start(self):
        self._thread = Thread(
            target=self._run
        )
        self._thread.start()

        self._ticker = Ticker(SCREEN_WRITE_INTERVAL, self._queue)
        self._ticker.start()

    def push(self, update: Update):
        self._queue.put(update)

    def stop(self):
        self._ticker.stop()

        self._queue.put(STOP)

        if self._thread:
            self._thread.join()
            self._thread = None
