from queue import Queue
from threading import Event, Thread

from ._timestamp import timestamp


class Ticker:
    def __init__(self, interval: int, queue: Queue):
        self._interval = interval
        self._queue = queue

        self._thread = None
        self._stop_event = Event()

    def _run(self):
        while not self._stop_event.wait(self._interval):
            self._queue.put(timestamp())

    def start(self):
        self._thread = Thread(
            target=self._run
        )
        self._stop_event.clear()
        self._thread.start()

    def stop(self):
        self._stop_event.set()
        if self._thread:
            self._thread.join()
            self._thread = None
