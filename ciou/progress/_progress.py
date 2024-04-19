from contextlib import contextmanager
from io import StringIO
from queue import Queue
from threading import Thread
from uuid import uuid4

from ciou.time import Ticker

from ._config import OutputConfig
from ._message import MessageStatus, MessageStore, Update
from ._renderer import MessageRenderer


SCREEN_WRITE_INTERVAL = 0.095
STOP = "_stop"


class Progress:
    '''The main interface of the `ciou.progress` module.
    '''

    def __init__(self, config: OutputConfig = None):
        if not config:
            config = OutputConfig()

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
        '''Start the rendering loop on a new thread.
        '''
        self._thread = Thread(
            target=self._run
        )
        self._thread.start()

        self._ticker = Ticker(SCREEN_WRITE_INTERVAL, self._queue)
        self._ticker.start()

    def push(self, update: Update):
        '''Push `Update` to the progress log.
        '''
        self._queue.put(update)

    def stop(self):
        '''Stop the rendering loop after rendering the final state of the
        progress log.
        '''
        self._ticker.stop()

        self._queue.put(STOP)

        if self._thread:
            self._thread.join()
            self._thread = None

    @contextmanager
    def task(self, message, key=None):
        '''Helper for automatically pushing updates to the progress log.

        For example:

        ```python
        .. include:: ../../examples/progress_contextmanager.py
        ```
        '''
        if not key:
            key = f'message-{uuid4()}'

        self.push(Update(
            key=key, message=message, status=MessageStatus.STARTED))

        try:
            yield key

            self.push(Update(
                key=key, status=MessageStatus.SUCCESS))
        except Warning as warning:
            self.push(
                Update(
                    key=key,
                    status=MessageStatus.WARNING,
                    details=str(warning)))
        except Exception as error:
            self.push(
                Update(
                    key=key,
                    status=MessageStatus.ERROR,
                    details=str(error)))


class Checks:
    '''Helper class for writing progress logs to a StringIO output without
    animations or threading.'''

    def __init__(self, config: OutputConfig = None):
        if not config:
            config = OutputConfig()

        self._target = StringIO()
        config.target = self._target

        self._renderer = MessageRenderer(config)
        self._store = MessageStore()

    def push(self, update: Update):
        '''Push `Update` to the checks log.
        '''
        self._store.push(update)

    def close(self):
        '''Close the proress log. Finishes in-progress messages.
        '''
        self._store.close()

    def getvalue(self) -> str:
        '''Return the progess log content.
        '''
        self._renderer.render(self._store)
        return self._target.getvalue()
