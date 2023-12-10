from dataclasses import dataclass
from enum import Enum

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
