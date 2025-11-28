import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
json_file = BASE_DIR / "data" / "userdata.json"

class UserData:
    def __init__(self, username, password_hash, email, role="einfach"):
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.role = role

    def to_dict(self):
        return {
            "username": self.username,
            "email": self.email,
            "password": self.password_hash.decode("utf-8"),
            "role": self.role,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            username=data.get("username"),
            password_hash=data.get("password-hash").encode("utf-8"),
            email=data.get("email"),
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