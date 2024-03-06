try:
    from datetime import datetime, UTC
except ImportError:
    from datetime import datetime, timezone
    UTC = timezone.utc


def utcnow():
    '''Return timezone aware datetime object with current UTC time.
    '''
    return datetime.now(UTC)


def timestamp():
    '''Get current UTC time as ISO 8601 string.
    '''
    return utcnow().isoformat().replace("+00:00", "Z")
