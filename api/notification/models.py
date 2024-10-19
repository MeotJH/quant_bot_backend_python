from dataclasses import asdict, dataclass

@dataclass
class Notification:
    title: str
    body: str
    user_mail: str

    def to_dict(self):
        return asdict(self)