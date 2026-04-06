from datetime import timedelta


try:
    from datetime import datetime, UTC
except ImportError:
    from datetime import datetime, timezone
    UTC = timezone.utc


def utcnow():
    '''Return timezone aware datetime object with current UTC time.
    '''
    return datetime.now(UTC)


def timestamp(dt: datetime = None):
    '''Get current UTC time as ISO 8601 timestamp string.

    Args:
        dt: `datetime` instance to use instead of `utcnow`. Must be timezone
            aware and use UTC as the timezone.
    '''
    if not dt:
        dt = utcnow()

    if dt.utcoffset() != timedelta():
        raise ValueError(
            'dt must be timezone aware and use UTC as the timezone.')

    return dt.isoformat().replace("+00:00", "Z")
