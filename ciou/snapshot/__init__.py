'''Test utilities for validating output using snapshot files.
'''

import inspect
from io import IOBase
import os
import re
from typing import List, Pattern, Tuple, Union


from ciou.types import ensure_list


def rewind_and_read(f: IOBase) -> str:
    '''Move cursor to the beginning of the file and read file content.

    See `snapshot` documentation for example usage.
    '''
    f.seek(0)
    return f.read()


REPLACE_CWD = (re.escape(os.getcwd()), '<CWD>')
'''Replace tuple for `snapshot` to remove dynamic durations from snapshots.
For example, `0.673 ms` → `<DURATION>`'''
REPLACE_DURATION = (r'[0-9]+\.[0-9]+.*s', '<DURATION>')
'''Replace tuple for `snapshot` to remove dynamic durations from snapshots.
For example, `0.673 ms` → `<DURATION>`'''
REPLACE_TIMESTAMP = (
    r'[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}.[0-9]+Z',
    '<TIMESTAMP>')
'''Replace tuple for `snapshot` to remove timestamps created with
`ciou.time.timestamp` from snapshot.'''
REPLACE_UUID = (
    r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}',
    '<UUID>')
'''Replace tuple for `snapshot` to remove UUIDs from snapshots.'''


_Replace = Tuple[Pattern, str]


def snapshot(
        key: str,
        value: str,
        directory_name: str = 'snapshots',
        testfile: str = None,
        replace: Union[_Replace, List[_Replace]] = None,
        encoding: str = 'utf-8',
        ) -> Tuple[str, str]:
    '''Testing utility that returns `value` after applying `replace`s and the
    value of the snapshot:

    - If snapshot exists and `UPDATE_SNAPSHOTS` environment variable is not
      set, return the value defined in the snapshot.
    - If snapshot does not exists or `UPDATE_SNAPSHOTS` environment variable
      is set, write given value to the snapshot and return the new snapshot
      value.

    Args:
      key: identifier of the snapshot that will be used in the snapshot
        filename.
      value: value to write into snapshot, if snapshot does not exists or
        `UPDATE_SNAPSHOTS` environment variable is set.
      directory_name: name to use for directory where the snapshots are stored.
      testfile: the path of the testfile. The snapshots directory is created
        into the directory where testfile is located in.
      replace: replace patterns, for example durations or UUIDs, in value with
        given placeholders.
      encoding: encoding to use when reading and writing the snapshot file.

    For example:

    ```python
    .. include:: ../../examples/snapshot.py
    ```
    '''
    if not testfile:
        testfile = inspect.getsourcefile(inspect.stack()[1].frame)

    replaces = ensure_list(replace)
    for r in replaces:
        pattern, repl = r
        value = re.sub(pattern, repl, value)

    filepath = os.path.join(
        os.path.dirname(testfile),
        directory_name,
        f'{key}.snapshot')

    try:
        with open(filepath, "r", encoding=encoding) as f:
            prev = f.read()
    except FileNotFoundError:
        prev = None

    if os.getenv("UPDATE_SNAPSHOTS") or prev is None:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, "w+", encoding=encoding) as f:
            f.write(value)
            return value, value

    return prev, value
