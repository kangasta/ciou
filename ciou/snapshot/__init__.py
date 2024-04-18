'''Test utilities for validating output using snapshot files.
'''

import inspect
from io import IOBase
from os import getenv, makedirs, path


def rewind_and_read(f: IOBase) -> str:
    '''Move cursor to the beginning of the file and read file content.

    See `snapshot` documentation for example usage.
    '''
    f.seek(0)
    return f.read()


def snapshot(
        key: str,
        value: str,
        directory_name: str = 'snapshots',
        testfile: str = None) -> str:
    '''Testing utility that returns the value of a snapshot:

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

    For example:

    ```python
    .. include:: ../../examples/snapshot.py
    ```
    '''
    if not testfile:
        testfile = inspect.getsourcefile(inspect.stack()[1].frame)

    filepath = path.join(
        path.dirname(testfile),
        directory_name,
        f'{key}.snapshot')

    try:
        with open(filepath, "r") as f:
            prev = f.read()
    except FileNotFoundError:
        prev = None

    if getenv("UPDATE_SNAPSHOTS") or prev is None:
        makedirs(path.dirname(filepath), exist_ok=True)
        with open(filepath, "w+") as f:
            f.write(value)
            return value

    return prev
