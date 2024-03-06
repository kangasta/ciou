from queue import Queue
from threading import Event, Thread

from ._timestamp import timestamp


class Ticker:
    '''Ticker pushes timestamps to a queue at given interval.
    '''

    def __init__(self, interval: float, queue: Queue):
        '''Initialize the ticker.

        Args:
            interval: interval of the ticks in seconds.
            queue: queue where to push the timestamp strings.
        '''
        self._interval = interval
        self._queue = queue

        self._thread = None
        self._stop_event = Event()

    def _run(self):
        while not self._stop_event.wait(self._interval):
            self._queue.put(timestamp())

    def start(self):
        '''Start the ticker.
        '''
        self._thread = Thread(
            target=self._run
        )
        self._stop_event.clear()
        self._thread.start()

    def stop(self):
        '''Stop the ticker.
        '''
        self._stop_event.set()
        if self._thread:
            self._thread.join()
            self._thread = None
