from dataclasses import dataclass, InitVar
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional

from ciou.time import utcnow


class MessageStatus(Enum):
    PENDING = "pending"
    '''Message has not been started yet.'''
    STARTED = "started"
    '''Message has been started and is thus in-progress.'''
    SUCCESS = "success"
    '''Message has been finished successfully.'''
    WARNING = "warning"
    '''Message has been finished with warning.'''
    ERROR = "error"
    '''Message has been finished with error.'''
    SKIPPED = "skipped"
    '''Message was finished without it reaching in-progress state.'''
    UNKNOWN = "unknown"
    '''Message was finished while it was in-progress.'''

    def __init__(self, status):
        self._status = status

    @property
    def in_progress(self):
        return self._status == MessageStatus.STARTED.value

    @property
    def finished(self):
        return self._status in (
            MessageStatus.SUCCESS.value,
            MessageStatus.WARNING.value,
            MessageStatus.ERROR.value,
            MessageStatus.SKIPPED.value,
            MessageStatus.UNKNOWN.value,
        )


@dataclass()
class Update:
    key: InitVar[Optional[str]] = None
    message: Optional[str] = None
    status: MessageStatus = None
    progress_message: Optional[str] = None
    details: Optional[str] = None

    def __post_init__(self, key):
        self.key = key if key else self.message


@dataclass()
class Message:
    key: Optional[str] = None
    message: Optional[str] = None
    status: Optional[MessageStatus] = MessageStatus.PENDING
    progress_message: Optional[str] = None
    details: Optional[str] = None
    created: Optional[datetime] = None
    started: Optional[datetime] = None
    finished: Optional[datetime] = None

    def update(self, update: Update):
        if not self.created:
            self.created = utcnow()

        if update.status != MessageStatus.PENDING and not self.started:
            self.started = utcnow()

        if update.status and update.status.finished:
            self.finished = utcnow()

            if not self.started:
                self.started = utcnow()

        if not self.key:
            self.key = update.key

        if update.message is not None:
            self.message = update.message

        if update.status is not None:
            self.status = update.status

        if update.details is not None:
            self.details = update.details

        # Clear progress message if it is not set in the update
        self.progress_message = update.progress_message

    def __lt__(self, other):
        # Sort zero before any value
        if not self.started and other.started:
            return True

        if self.started and not other.started:
            return False

        # For not started, sort by created time
        if not self.started and not other.started:
            return self.created < other.created

        # Sort by started time
        return self.started < other.started

    @property
    def elapsed_seconds(self):
        if not self.started:
            return 0

        end = self.finished if self.finished else utcnow()
        return (end - self.started).total_seconds()


class MessageStore:
    def __init__(self):
        self._in_progress: Dict[str, Message] = {}
        self._finished: List[Message] = []

    def _store(self, message: Message):
        if message.status.finished:
            if message.key in self._in_progress:
                del self._in_progress[message.key]
            self._finished.append(message)
        else:
            self._in_progress[message.key] = message

    def push(self, update: Update):
        message = self._in_progress.get(update.key, Message())
        message.update(update)
        self._store(message)

    def close(self):
        for message in self.in_progress:
            if message.status == MessageStatus.PENDING:
                self.push(
                    Update(
                        key=message.key,
                        status=MessageStatus.SKIPPED))
            if message.status == MessageStatus.STARTED:
                self.push(
                    Update(
                        key=message.key,
                        status=MessageStatus.UNKNOWN))

    @property
    def in_progress(self):
        in_progess = sorted(
            [message for _, message in self._in_progress.items()])
        return in_progess

    @property
    def finished(self):
        return self._finished
