from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
import os
import re
from sys import stderr, stdout
from typing import Iterable

from ciou.time import timestamp, utcnow


class Stream(Enum):
    STDOUT = 'stdout'
    STDERR = 'stderr'
    STDIN = 'stdin'


@dataclass
class StreamsDataRow:
    stream: Stream
    timestamp: datetime
    text: str

    def to_serializable(self):
        return dict(
            stream=self.stream.value,
            timestamp=timestamp(self.timestamp),
            text=self.text,
        )


class StreamsData(list):
    '''List of `StreamsDataRow` instances with `to_serializable` helper method.
    '''

    def __init__(self, data: Iterable[StreamsDataRow] = None):
        super().__init__(data)

    def to_serializable(self):
        return [i.to_serializable() for i in self]


def _command_as_str(command):
    return ' '.join(
        i if not re.search(r'\s', i) else f"'{i}'" for i in command)


def _get_stream(stream: Stream):
    return stdout if stream == Stream.STDOUT else stderr


def _read_stream(stream, stream_fd, encoding, log_to_console):
    f = os.fdopen(stream_fd, encoding=encoding, errors='backslashreplace')
    data = []

    for line in iter(f.readline, ''):
        text = line.rstrip('\n')
        data.append(StreamsDataRow(
            stream=stream,
            timestamp=utcnow(),
            text=text))
        if log_to_console:
            print(text, file=_get_stream(stream))

    f.close()
    return data


class Streams:
    '''Context manager for capturing console output with stream and timestamp
    information when using `subprocess`. For example:

    ```python
    from ciou.streams import Streams
    from subprocess import run

    with Streams() as (stdout, stderr, streams):
        process = run(
            ("echo", "Hello, world!",),
            stderr=stderr,
            stdout=stdout,
            bufsize=0,
        )

    streams_data = streams.read(wait=True)
    ```
    '''
    def __init__(self, log_to_console=False):
        '''Initialize the `Streams` context manager.

        Args:
            log_to_console: If `True`, the output will be also streamed to the
            console.
        '''
        self._writes = []
        self._futures = []
        self._pool = ThreadPoolExecutor(max_workers=3)
        self._data = []
        self._log_to_console = log_to_console

    def __enter__(self):
        stdout = self._create(Stream.STDOUT)
        stderr = self._create(Stream.STDERR)

        return (stdout, stderr, self,)

    def __exit__(self, type_, value, traceback):
        self._close()

    def output(self, text: str):
        '''Push text to the captured stdout stream.'''
        if text:
            return self._push(Stream.STDOUT, text=text)

    def input(self, text: str | Iterable[str]):
        '''Push text to the captured stdin stream.'''
        if text and isinstance(text, str):
            return self._push(Stream.STDIN, text=text)

        if text:
            return self._push(Stream.STDIN, text=_command_as_str(text))

    def error(self, text: str):
        '''Push text to the captured stderr stream.'''
        if text:
            return self._push(Stream.STDERR, text=text)

    def _push(self, stream: Stream = None, timestamp=None, text=None):
        if not (stream and text):
            raise ValueError(
                'Cannot push data without both stream and text.')

        if not timestamp:
            timestamp = utcnow()

        self._data.append(StreamsDataRow(
            stream=stream,
            timestamp=timestamp,
            text=text,
        ))

        if self._log_to_console:
            if stream == Stream.STDIN and not text.startswith('# '):
                text = f'+ {text}'

            print(text, file=_get_stream(stream))

    def extend(self, data):
        self._data.extend(data)

    def _create(self, stream, encoding='utf-8'):
        read_fd, write_fd = os.pipe()
        self._writes.append(write_fd)
        self._futures.append(
            self._pool.submit(
                _read_stream,
                stream,
                read_fd,
                encoding,
                self._log_to_console
            ))
        return write_fd

    def _close(self):
        for f in self._writes:
            os.close(f)

    def read(self, wait=False):
        '''Read captured console output.

        If `wait` is `False`, it will return `None` if any of the stream
        reading threads is still running.'''
        data = []
        data.extend(self._data)

        for future in self._futures:
            if not wait and not future.done():
                return None

            data.extend(future.result())

        data.sort(key=lambda i: i.timestamp)
        return StreamsData(data)

    @property
    def data(self):
        '''Alias for `read()`.'''
        return self.read()
