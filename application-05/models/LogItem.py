from dataclasses import dataclass
from enum import Enum
from datetime import datetime

class TransactionStatus(Enum):
    IN_PROGRESS = 0
    PREPARED = 1
    COMMITED = 2
    ABORTED = 3

@dataclass
class LogItem:
    msg: str
    timestamp: str

    @staticmethod
    def from_msg(msg: str):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return LogItem(msg, timestamp)
    
    @staticmethod
    def from_dict(data):
        return LogItem(data['msg'], data['timestamp'])
