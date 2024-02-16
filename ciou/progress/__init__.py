'''Library for outputting progress logs to stdout and stderr.

Python implementation of UpCloudLtd/progress.
'''

from ._messages import (
    Message,
    MessageStatus,
    MessageStore,
    Update,
)

from ._config import (
    OutputConfig,
)
