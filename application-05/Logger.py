from models.LogItem import LogItem, LogLevel
import json

class Logger:
    def __init__(self, name:str):
        self.name = name
        self.logs = []
        self.load()

    def log(self, msg:str , tid:int = -1, type:LogLevel = LogLevel.INFO):
        log = LogItem.from_msg(msg, tid, type)
        self.logs.append(log)
        print(f'{log.timestamp} {log.tid} [{log.type}] {log.msg}')
        self.persist()

    def persist(self):
        data = {
            'logs': self.logs,
        }
        print(data)
        with open(f'log-{self.name}.json', 'w') as file:
            json.dump(data, file, default=lambda o: o.__dict__, ensure_ascii=True, indent=4)

    def load(self):
        try:
            data = None
            
            with open(f'log-{self.name}.json', 'r') as file:
                data = json.load(file)
            
            if data is None:
                raise Exception('Invalid file')
            
            self.logs = [LogItem.from_dict(d) for d in data['logs']]
        except:
            self.logs = []