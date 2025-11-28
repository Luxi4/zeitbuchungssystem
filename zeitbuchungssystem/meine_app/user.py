
class User:
    def __init__(self, username, password, email, role="einfach"):
        self.username = username
        self.password = password
        self.email = email
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
            username=data["username"],
            email=data["email"],
            password=data["password"],
            role=data.get("role", "einfach"),
        )
    

    
    @staticmethod
    def fieldnames():
        return [field.name for field in fields(User)]