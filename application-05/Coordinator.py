from Logger import Logger
from models.LogItem import LogLevel
from models.Transaction import Transaction, TransactionStatus

import json
import requests

class Coordinator:
    def __init__(self):
        self.transactions = []
        self.logger = Logger('coordinator')
        self.__initialize()

    def startTransaction(self):
        tid = len(self.transactions) + 1
        self.transactions.append(Transaction(tid,TransactionStatus.IN_PROGRESS,[]))
        self.persist()
        self.logger.log(f"Transaction created.", tid)
        return tid
    
    def registerParticipant(self, participant, tid):
        found = False
        for i in range(len(self.transactions)):
            if self.transactions[i].tid == tid:
                self.transactions[i].participants.append(participant)
                found = True
        
        if not found:
            msg = f'Transaction {tid} not found. Cannot add participant.'
            self.logger.log(msg, tid, LogLevel.WARN);
            raise ValueError(msg)

    def getTransaction(self, tid: int):
        transaction = None
        for t in self.transactions:
            if t.tid == tid:
                transaction = t
                break
        
        if transaction is None:
            raise ValueError(f"Transaction with TID={tid} not found")
        
        return transaction
    
    def getTransactionStatus(self, tid: int):
        return self.getTransaction(tid).status

    def commitTransaction(self, tid: int):
        transaction = self.getTransaction(tid)

        # Check if transaction can be committed
        if transaction.status in [TransactionStatus.COMMITED, TransactionStatus.ABORTED]:
            msg = f'Transaction already {transaction.status}'
            self.logger.log(msg, tid, LogLevel.ERROR)
            raise RuntimeError(msg)
        
        self.logger.log('Preparing transaction.', tid)

        success = True
        # Prepare participants
        for participant in transaction.participants:
            success &= self.__prepareParticipant(participant, tid)

        if not success:
            msg = f'Failed to prepare transaction {tid}'
            self.logger.log(msg, tid, LogLevel.ERROR)
            self.rollbackTransaction(tid)
            raise RuntimeError(msg)

        self.__updateTransactionStatus(tid, TransactionStatus.COMMITED)

        success = True
        # Commit participants
        for participant in transaction.participants:
            success &= self.__commitParticipant(participant, tid)

        if not success:
            msg = f'Unexpected error commiting participants in transaction {tid}'
            self.logger(msg, tid, LogLevel.WARN)

    def rollbackTransaction(self, tid: int):
        transaction = self.getTransaction(tid)

        # Check if transaction can be rolledback
        if transaction.status in [TransactionStatus.COMMITED, TransactionStatus.ABORTED]:
            msg = f'Transaction already {transaction.status}'
            self.logger.log(msg, tid, LogLevel.ERROR)
            raise RuntimeError(msg)
        
        self.logger.load(f'Rolling back transaction.', tid)
        
        self.__updateTransactionStatus(tid, TransactionStatus.ABORTED)

        success = True
        for participant in transaction.participants:
            success &= self.__abortParticipant(participant, tid)
        
        if success:
            self.logger.log(f'Transaction aborted successfully.', tid)
        else:
            msg = f'Transaction aborted with errors'
            self.logger.log(msg, tid, LogLevel.FATAL)

    def __prepareParticipant(self, participan, tid):
        try:
            res = requests.post(f'{participan}/transaction/{tid}/prepare')

            if not res.ok():
                msg = f'Cannot prepare participan {participan} {res.status_code}'
                self.logger.log(msg, tid, LogLevel.ERROR)
                return False
            
            msg = f'Participan {participan} prepared'
            self.logger.log(msg, tid)
            return True
        except requests.exceptions.RequestException as e:
            cause = e.args[0]
            msg = f'Cannot prepare participan {participan} {cause.args[0]}'
            self.logger.log(msg, tid, LogLevel.ERROR)
            return False

    
    def __commitParticipant(self, participan, tid):
        try:
            res = requests.post(f'{participan}/transaction/{tid}/commit')

            if not res.ok():
                msg = f'Cannot commit participan {participan} {res.status_code}'
                self.logger.log(msg, tid, LogLevel.FATAL)
                return False
            
            return True
        except requests.exceptions.RequestException as e:
            cause = e.args[0]
            msg = f'Cannot commit participan {participan} {cause.args[0]}'
            self.logger.log(msg, tid, LogLevel.ERROR)
            return False
        
    def __abortParticipant(self, participan, tid):
        try:
            res = requests.post(f'{participan}/transaction/{tid}/abort')

            if not res.ok():
                msg = f'Cannot abort participan {participan} {res.status_code}'
                self.logger.log(msg, tid, LogLevel.FATAL)
                return False
            
            return True
        except requests.exceptions.RequestException as e:
            cause = e.args[0]
            msg = f'Cannot abort participan {participan} {cause.args[0]}'
            self.logger.log(msg, tid, LogLevel.ERROR)
            return False

    def __updateTransactionStatus(self, tid:int, status:TransactionStatus):
        updated = False
        previous_state = None
        for i in range(len(self.transactions)):
            if self.transactions[i].tid == tid:
                previous_state = self.transactions[i].status
                if previous_state != status and  previous_state in [TransactionStatus.ABORTED, TransactionStatus.COMMITED]:
                    msg = f'Cannot change an ended trasaction {tid} {previous_state}->{status}'
                    self.logger.log(msg, tid, LogLevel.FATAL)
                    raise RuntimeError(msg)
                self.transactions[i].status = status
                updated = True
        
        if updated:
            self.logger.log(f'Transaction state updated from {previous_state}->{status}', tid)
        else:
            msg = f'Transaction to updated not found.'
            self.logger.log(msg, tid, LogLevel.ERROR);
            raise ValueError(msg)
        
        self.persist()

    def __initialize(self):
        self.load()

        self.logger.log('Initializing coordinator')

        pendingTransactions = []
        for transaction in self.transactions:
            if transaction.status not in [TransactionStatus.COMMITED, TransactionStatus.ABORTED]:
                pendingTransactions.append()

        for transaction in pendingTransactions:
            self.rollbackTransaction(transaction.tid)

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

if __name__ == '__main__':
    coord = Coordinator()