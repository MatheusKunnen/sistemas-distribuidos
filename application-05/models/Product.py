from dataclasses import dataclass

@dataclass
class Product:
    id: int
    name: str
    stock: float
    price: float

    @staticmethod
    def from_dict(data):
        return Product(id=data['id'], name=data['name'], stock=data['stock'], price=data['price'])


