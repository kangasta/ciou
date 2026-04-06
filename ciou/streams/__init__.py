'''Module for capturing console output with stream and timestamp information
when using `subprocess`.
'''

from ._streams import Streams, Stream, StreamsData, StreamsDataRow
from ._run import RunResult, run

__all__ = [
    "Streams",
    "Stream",
    "StreamsData",
    "StreamsDataRow",
    "run",
    "RunResult",
]
