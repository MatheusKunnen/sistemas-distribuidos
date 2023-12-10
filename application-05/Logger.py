from models.LogItem import LogItem

class Logger:
    def __init__(self, name:str):
        self.name = name
        self.logs = []
        self.load()

    def log(self, msg):
        self.logs.append(LogItem.from_msg(msg))
        self.persist()

    def load(self):
        pass

    def persist(self):
        pass