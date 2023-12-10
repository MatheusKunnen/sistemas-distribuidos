from dataclasses import dataclass
from enum import Enum
from datetime import datetime
class LogLevel(str, Enum):
    INFO = 'INFO'
    WARN = 'WARN'
    ERROR = 'ERROR'
    FATAL = 'FATAL'

@dataclass
class LogItem:
    msg: str
    timestamp: str
    tid: int
    type: LogLevel

    @staticmethod
    def from_msg(msg: str, tid: int = -1, type = LogLevel.INFO):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return LogItem(msg, timestamp, tid, type)
    
    @staticmethod
    def from_dict(data):
        return LogItem(data['msg'], data['timestamp'], int(data['tid']), LogLevel(data['type']))
