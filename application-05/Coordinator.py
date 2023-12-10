from Logger import Logger
from models.Transaction import Transaction, TransactionStatus
import json

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
        data = {
            'transactions': self.transactions,
        }
        with open('transactions.json', 'w') as file:
            json.dump(data, file, default=lambda o: o.__dict__, ensure_ascii=True, indent=4)

    def load(self):
        try:
            data = None
            
            with open('transactions.json', 'r') as file:
                data = json.load(file)
            
            if data is None:
                raise Exception('Invalid file')
            
            self.transactions = [Transaction.from_dict(d) for d in data['transactions']]
        except:
            self.transactions = []