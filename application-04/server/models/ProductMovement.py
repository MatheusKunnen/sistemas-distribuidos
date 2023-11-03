from dataclasses import dataclass
from datetime import datetime

@dataclass
class ProductMovement:
    id: int
    quantity: float
    timestamp: str

    @staticmethod
    def from_dict(data):
        timestamp = data.get('timestamp') if 'timestamp' in data else datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return ProductMovement(data['id'], data['quantity'], timestamp)



