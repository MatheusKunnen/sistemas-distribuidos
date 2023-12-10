from dataclasses import dataclass
from enum import Enum

from .Register import Register
class TransactionStatus(Enum):
    IN_PROGRESS = 0
    PREPARED = 1
    COMMITED = 2
    ABORTED = 3

@dataclass
class Transaction:
    tid: int
    status: TransactionStatus
    participants: list[str]

    @staticmethod
    def from_dict(data):
        return Transaction(data['tid'], data['status'], data['participants'])

@dataclass
class ParticipantTransaction:
    tid: int
    status: TransactionStatus
    inserted: list[Register]
    updated: list[Register]
    deleted: list[int]

    @staticmethod
    def from_dict(data):
        return Transaction(data['tid'], data['status'], data['inserted'], data['updated'], data['deleted'])