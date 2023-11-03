from dataclasses import dataclass

@dataclass
class User:
    name: str
    public_key: str

    @staticmethod
    def from_dict(data):
        return User(name=data['name'], public_key=data['public_key'])



