from dataclasses import dataclass
from enum import Enum

class TransactionStatus(Enum):
    IN_PROGRESS = 0
    PREPARED = 1
    COMMITED = 2
    ABORTED = 3

@dataclass
class Transaction:
    id: int
    status: TransactionStatus

    @staticmethod
    def from_dict(data):
        return Transaction(data['id'], data['status'])
