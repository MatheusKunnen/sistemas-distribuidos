from Logger import Logger
from models.Transaction import Transaction, TransactionStatus

class Coordinator:
    def __init__(self):
        self.transactions = []
        self.logger = Logger('coordinator')

    def startTransaction(self):
        tid = len(self.transactions) + 1
        self.transactions.append(Transaction(tid,TransactionStatus.IN_PROGRESS))
        self.persist()
        self.logger(f"Transaction created. TID={tid}")
        return tid

    def getTransactionStatus(self, tid: int):
        transaction = None
        for t in self.transactions:
            if t.tid == tid:
                transaction = t
                break
        
        if transaction is None:
            raise ValueError(f"Transaction with TID={tid} not found")
        
        return transaction.status

    def commitTransaction(self, tid: int):
        pass

    def rollbackTransaction(self, tid: int):
        pass

    def persist(self):
        pass

    def load(self):
        pass