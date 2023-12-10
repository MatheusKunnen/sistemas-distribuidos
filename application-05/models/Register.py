from dataclasses import dataclass

@dataclass
class Register:
    id: int
    payload: dict
    tid: int

    @staticmethod
    def from_dict(data):
        return Register(data['id'], data['payload'], data['tid'])
