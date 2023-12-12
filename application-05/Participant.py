from Logger import Logger, LogLevel
from models.Transaction import ParticipantTransaction, TransactionStatus
from models.Register import Register
import json
import requests

class Participant:
    def __init__(self, name:str, coordinator:str, reference:str):
        self.name = name
        self.coordinator = coordinator
        self.reference = reference
        self.last_row_id = 0
        self.rows:list[Register] = []
        self.transactions:list[ParticipantTransaction] = []

        self.logger = Logger(name)

        self.__initialize()

    def prepareTransaction(self, tid):
        self.__updateTransactionStatus(tid, TransactionStatus.PREPARED)

    def commitTransaction(self, tid):
        rows, last_row_id = self.getRowsWithTransaction(tid)

        self.__updateTransactionStatus(tid, TransactionStatus.COMMITED)

        self.rows = rows

        self.last_row_id = last_row_id
        self.persist()

    def getData(self, tid:int = -1):
        if tid <= 0:
            return [Register.from_dict(r.__dict__.copy()) for r in self.rows.copy()]
        
        transaction = self.getTransaction(tid)
        if transaction.status != TransactionStatus.IN_PROGRESS:
            msg = f'Cannot get from {transaction.status} transaction {tid}.'
            self.logger.log(msg, tid, LogLevel.ERROR)
            raise RuntimeError(msg)
        
        rows, l = self.getRowsWithTransaction(tid)
        return rows

    def updateRegister(self, register:Register, tid:int):
        transaction = self.getTransaction(tid)

        if transaction.status != TransactionStatus.IN_PROGRESS:
            msg = f'Cannot update from {transaction.status} transaction {tid}.'
            self.logger.log(msg, tid, LogLevel.ERROR)
            raise RuntimeError(msg)
        
        if self.isRowBlocked(id):
            msg = f'Cannot update blocked register {id}'
            self.logger.log(msg, tid, LogLevel.WARN)
            raise RuntimeError(msg)

        for i in range(len(self.transactions)):
            transaction = self.transactions[i]
            if transaction.tid == tid:
                found = False
                for j in range(len(transaction.updated)):
                    if transaction.updated[j].id == register.id:
                        found = True
                        self.transactions[i].updated[j] = register
                        self.logger.log(f'Updating {register} in transaction. (U)', tid)
                if not found:
                    self.transactions[i].updated.append(register)
                    self.logger.log(f'Updating {register} in transaction. (N)', tid)

        self.persist()

    def insertRegister(self, register:Register, tid:int):
        transaction = self.getTransaction(tid)

        if transaction.status != TransactionStatus.IN_PROGRESS:
            msg = f'Cannot insert to {transaction.status} transaction {tid}.'
            self.logger.log(msg, tid, LogLevel.ERROR)
            raise RuntimeError(msg)

        for i in range(len(self.transactions)):
            if self.transactions[i].tid == tid:
                register.tid = tid
                self.transactions[i].inserted.append(register)
                self.logger.log(f'Inserting {register} in transaction.', tid)

        self.persist()

    def deleteRegister(self, id:int, tid:int):
        transaction = self.getTransaction(tid)

        if transaction.status != TransactionStatus.IN_PROGRESS:
            msg = f'Cannot delete from {transaction.status} transaction {tid}.'
            self.logger.log(msg, tid, LogLevel.ERROR)
            raise RuntimeError(msg)

        if self.isRowBlocked(id):
            msg = f'Cannot deleted blocked register {id}'
            self.logger.log(msg, tid, LogLevel.WARN)
            raise RuntimeError(msg)

        for i in range(len(self.transactions)):
            if self.transactions[i].tid == tid:
                found = False
                for deleted in self.transactions[i].deleted:
                    if deleted == id:
                        found = True
                        break
                if not found:
                    self.logger.log(f'Deleting {id} in transaction {tid}', tid)
                    self.transactions[i].deleted.append(id)
                else:
                    self.logger.log(f'Trying to deleted {id} already deleted. {tid}', tid, LogLevel.WARN)
                break

        self.persist()

    def abortTransaction(self, tid):
        self.__updateTransactionStatus(tid, TransactionStatus.ABORTED)

    def getTransaction(self, tid):
        tid = int(tid)
        try:
            return self.getLocalTransaction(tid)
        except:
            transaction = ParticipantTransaction(tid, TransactionStatus.IN_PROGRESS, [],[],[])
            self.__registerAsParticipant(tid)
            self.transactions.append(transaction)
            self.persist()
            return transaction
        
    def getLocalTransaction(self, tid: int):
        transaction = None
        for t in self.transactions:
            if t.tid == tid:
                transaction = t
                break
        
        if transaction is None:
            raise ValueError(f"Transaction with TID={tid} not found")
        
        return transaction
    
    def getLocalTransactionStatus(self, tid: int):
        return self.getLocalTransaction(tid).status
    
    def getRowsWithTransaction(self, tid:int):
        transaction = self.getTransaction(tid)
        
        deleted_ids = [r.id for r in transaction.deleted]

        rows = []
        for row in self.rows.copy():
            if row.id not in deleted_ids:
                rows.append(row)

        l_rowid = self.last_row_id
        for row in transaction.inserted:
            row.id = l_rowid + 1
            l_rowid += 1
            rows.append(row)
        
        for row_u in transaction.updated:
            for i in range(len(rows)):
                if rows[i].id == row_u.id:
                    rows[i] = row_u
                    break

        return rows, l_rowid
    
    def isRowBlocked(self, rowid:int):
        for transaction in self.transactions:
            if transaction.status not in [TransactionStatus.COMMITED, TransactionStatus.ABORTED]:
                for updated in transaction.updated:
                    if updated.id == rowid:
                        return True
                for deleted in transaction.deleted:
                    if deleted == rowid:
                        return True
        return False
                
    def __initialize(self):
        self.logger.log(f'Participant {self.name} initializing. Coordinator: {self.coordinator}')
        self.load()

        pendingTransactions = []
        for transaction in self.transactions:
            if transaction.status not in [TransactionStatus.COMMITED, TransactionStatus.ABORTED]:
                pendingTransactions.append(transaction)

        for transaction in pendingTransactions:
            self.__syncTransaction(transaction.tid)
        pass

    def __registerAsParticipant(self, tid:int):
        try:
            res = requests.put(f'{self.coordinator}/transaction/{tid}/participant',json={'participant': self.reference})

            if res.ok:
                return
            
            msg = f'Cannot register participant ({self.reference}) into coordinator {self.coordinator}'
            self.logger.log(msg, tid, LogLevel.ERROR)
            raise RuntimeError(msg)

        except requests.exceptions.RequestException as e:
            cause = e.args[0]
            msg = f'Coordinator is not available {self.coordinator} {cause.args[0]}'
            self.logger.log(msg, tid, LogLevel.ERROR)
            raise RuntimeError(msg)
            

    def __syncTransaction(self, tid:int):
        try:
            res = requests.get(f'{self.coordinator}/transaction/{tid}')

            if not res.ok:
                msg = f'Invalid transaction {tid}. Cannot check status. ({res.status_code})'
                self.__updateTransactionStatus(tid, TransactionStatus.ABORTED)
                self.logger.log(msg, tid, LogLevel.FATAL)
            
            data = res.json()
            actual_status = TransactionStatus(data['status'])

            if actual_status == self.getLocalTransactionStatus(tid):
                return
            
            if actual_status == TransactionStatus.ABORTED:
                self.__updateTransactionStatus(tid, TransactionStatus.ABORTED)
            elif actual_status in [TransactionStatus.COMMITED, TransactionStatus.PREPARED]:
                self.commitTransaction(tid)


        except requests.exceptions.RequestException as e:
            cause = e.args[0]
            msg = f'Coordinator is not available {self.coordinator} {cause.args[0]}'
            self.logger.log(msg, tid, LogLevel.ERROR)
            raise RuntimeError(msg)

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

    def persist(self):
        data = {
            'transactions': self.transactions,
            'rows': self.rows,
            'last_row_id': self.last_row_id
        }

        with open(f'data-{self.name}.json', 'w') as file:
            json.dump(data, file, default=lambda o: o.__dict__, ensure_ascii=True, indent=4)

    def load(self):
        try:
            data = None
            
            with open(f'data-{self.name}.json', 'r') as file:
                data = json.load(file)
            
            if data is None:
                raise Exception('Invalid file')

            self.transactions = [ParticipantTransaction.from_dict(d) for d in data['transactions']]
            self.rows = [Register.from_dict(d) for d in data['rows']]
            self.last_row_id = int(data['last_row_id'])
        except Exception as e:
            print(e)
            self.transactions = []
            self.rows = []
            self.last_row_id = 0
            self.persist()

if __name__ == '__main__':
    p = Participant('test', 'http://localhost:5002')