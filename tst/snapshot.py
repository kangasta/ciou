from io import IOBase
from os import getenv, makedirs, path

def rewind_and_read(f: IOBase):
    f.seek(0)
    return f.read()

def snapshot(testfile, key, value):
    filepath = path.join(path.dirname(testfile), 'snapshots', f'{key}.snapshot')

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
