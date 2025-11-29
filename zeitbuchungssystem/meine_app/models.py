import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
json_file = BASE_DIR / "data" / "userdata.json"

class UserData:
    def __init__(self, username, email, password, role="einfach"):
        self.username = username
        self.email = email
        self.password = password
        self.role = role

    def to_dict(self):
        return {
            "username": self.username,
            "email": self.email,
            "password": self.password,
            "role": self.role,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            username=data.get("username"),
            email=data.get("email"),
            password=data.get("password"),
            role=data.get("role", "einfach"),
        )

def load_users():
    if json_file.exists():
        with json_file.open("r", encoding="utf-8") as f:
            data = json.load(f)
            return [UserData.from_dict(obj) for obj in data]
    return []

def save_users(users):
    with json_file.open("w", encoding="utf-8") as f:
        json.dump([u.to_dict() for u in users], f, indent=4, ensure_ascii=False)