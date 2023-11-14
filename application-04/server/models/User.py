from dataclasses import dataclass

@dataclass
class User:
    name: str
    password: str

    @staticmethod
    def from_dict(data):
        return User(name=data['name'], password=data['password'])



