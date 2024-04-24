from typing import Any, List
from types import GeneratorType


def ensure_list(value: Any) -> List:
    '''Ensure given `value` is a list:

    - If `value` is a list, return `value`.
    - If `value` is a generator, return generators content as a list.
    - If `value` is not a list, return value wrappep in a list.
    - If `value` is `None`, return empty list.
    '''
    if value is None:
        return []

    if isinstance(value, list):
        return value

    if isinstance(value, GeneratorType):
        return list(value)

    return [value]
