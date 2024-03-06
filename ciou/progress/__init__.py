'''Library for outputting progress logs to stdout and stderr.

Python implementation of
[UpCloudLtd / progress](https://github.com/UpCloudLtd/progress).
'''

from ._config import (
    OutputConfig,
)

from ._message import (
    Message,
    MessageStatus,
    Update,
)

from ._progress import Progress

__all__ = ["Progress", "OutputConfig", "Message", "MessageStatus", "Update"]
