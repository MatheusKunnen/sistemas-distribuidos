from Participant import Participant
from models.Register import Register

class OrderParticipant:

    DEFAULT_COORDINATOR = 'http://localhost:5001'
    __instance = None

    def __init__(self):
        self.participant = Participant('order', OrderParticipant.DEFAULT_COORDINATOR, 'http://localhost:5004')

    def registerOrder(self, tid:int, client_id:int,  product_id:int, amount:float):
        rows = self.participant.getData(int(tid))
        max_id = 0
        for i in range(len(rows)):
            if int(rows[i].payload['id']) > max_id:
                max_id = int(rows[i].payload['id'])
        
        new_row = Register(-1, payload={
            'id': max_id + 1,
            'client_id':int(client_id),
            'product_id':int(product_id),
            'amount':float(amount)
        }, tid=tid)

        self.participant.insertRegister(new_row, int(tid))

        return new_row.payload

    def getOrders(self, tid:int):
        rows = self.participant.getData(int(tid))
        
        return [r.payload for r in rows]

    @staticmethod
    def GetInstance():
        if OrderParticipant.__instance is None:
            OrderParticipant.__instance = OrderParticipant()
        return OrderParticipant.__instance
