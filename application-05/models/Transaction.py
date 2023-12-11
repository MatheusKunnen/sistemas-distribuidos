from dataclasses import dataclass
from enum import Enum

from .Register import Register
class TransactionStatus(str, Enum):
    IN_PROGRESS = 'IN_PROGRESS'
    PREPARED = 'PREPARED'
    COMMITED = 'COMMITED'
    ABORTED = 'ABORTED'

@dataclass
class Transaction:
    tid: int
    status: TransactionStatus
    participants: list[str]

    @staticmethod
    def from_dict(data):
        return Transaction(int(data['tid']), data['status'], data['participants'])

@dataclass
class ParticipantTransaction:
    tid: int
    status: TransactionStatus
    inserted: list[Register]
    updated: list[Register]
    deleted: list[int]

    @staticmethod
    def from_dict(data):
        inserted = [Register.from_dict(r) for r in data['inserted']]
        updated = [Register.from_dict(r) for r in data['updated']]
        return ParticipantTransaction(int(data['tid']), data['status'], inserted, updated, data['deleted'])