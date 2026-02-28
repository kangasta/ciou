import random


# From Kubernetes random postfix.
RANDOM_POSTFIX_CHARS = 'bcdfghjklmnpqrstvwxz2456789'
RANDOM_POSTFIX_LEN = 5


def postfix_generator(separator: str = None):
    '''Yields random postfixes.'''
    if separator is None:
        separator = '-'

    for _ in range(13):
        yield separator + ''.join(
            random.choices(RANDOM_POSTFIX_CHARS, k=RANDOM_POSTFIX_LEN))


def with_random_postfix(value: str, separator: str = None) -> str:
    '''Returns `value` with random postfix.'''
    return value + next(postfix_generator(separator))
