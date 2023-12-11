from Participant import Participant
from models.Register import Register

class StockParticipant:

    DEFAULT_COORDINATOR = 'http://localhost:5001'
    __instance = None

    def __init__(self):
        self.participant = Participant('stock', StockParticipant.DEFAULT_COORDINATOR, 'http://localhost:5002')

    def updateProductStock(self, tid:int, id:int, stock:float):
        rows = self.participant.getData(int(tid))
        register = None
        for i in range(len(rows)):
            if int(rows[i].payload['id']) == int(id):
                register = rows[i]
                break
        
        if register is None:
            raise KeyError(f'Product {id} not found')
        register = Register.from_dict(register.__dict__.copy())
        register.payload = register.payload.copy()
        register.payload['stock'] = float(register.payload['stock']) + stock

        self.participant.updateRegister(register, int(tid))

        return register.payload

    def getProducts(self, tid:int):
        rows = self.participant.getData(int(tid))
        
        return [r.payload for r in rows]

    @staticmethod
    def GetInstance():
        if StockParticipant.__instance is None:
            StockParticipant.__instance = StockParticipant()
        return StockParticipant.__instance
