from dataclasses import dataclass
from datetime import datetime
@dataclass
class Product:
    id: int
    name: str
    description: str 
    stock: float
    minimum_stock: float
    price: float
    timestamp: str

    @staticmethod
    def from_dict(data):
        timestamp = data.get('timestamp') if 'timestamp' in data else datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return Product(id=data['id'], name=data['name'], description=data['description'], stock=data['stock'], minimum_stock=data['minimum_stock'], price=data['price'], timestamp=timestamp)


