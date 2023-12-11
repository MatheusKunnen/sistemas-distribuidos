from Participant import Participant
from models.Register import Register

class PaymentParticipant:

    DEFAULT_COORDINATOR = 'http://localhost:5001'
    __instance = None

    def __init__(self):
        self.participant = Participant('payment', PaymentParticipant.DEFAULT_COORDINATOR, 'http://localhost:5003')

    def updateBalance(self, tid:int, id:int, amount:float):
        rows = self.participant.getData(int(tid))
        register = None
        for i in range(len(rows)):
            if int(rows[i].payload['id']) == int(id):
                register = rows[i]
                break
        
        if register is None:
            raise KeyError(f'Account {id} not found')
        register = Register.from_dict(register.__dict__.copy())
        register.payload = register.payload.copy()
        register.payload['balance'] = float(register.payload['balance']) + amount

        self.participant.updateRegister(register, int(tid))

        return register.payload

    def getAccounts(self, tid:int):
        rows = self.participant.getData(int(tid))
        
        return [r.payload for r in rows]

    @staticmethod
    def GetInstance():
        if PaymentParticipant.__instance is None:
            PaymentParticipant.__instance = PaymentParticipant()
        return PaymentParticipant.__instance
