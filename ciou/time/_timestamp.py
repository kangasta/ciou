from datetime import datetime


def timestamp():
    return f'{datetime.utcnow().isoformat()}Z'
