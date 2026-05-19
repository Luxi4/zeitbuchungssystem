class UserData:
    def __init__(self, username, email, password, role="einfach", vip_request=False, admin_request=False, is_active=True, user_id=None):
        self.username = username
        self.email = email
        self.password = password
        self.role = role
        self.vip_request = vip_request
        self.admin_request = admin_request
        self.is_active = is_active
        self.id = user_id

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "password": self.password,
            "role": self.role,
            "vip_request": self.vip_request,
            "admin_request": self.admin_request,
            "is_active": self.is_active,
        }

def from_dict(data):
    return UserData(
        username=data.get("username"),
        email=data.get("email"),
        password=data.get("password"),
        role=data.get("role", "einfach"),
        vip_request=data.get("vip_request", False),
        admin_request=data.get("admin_request", False),
        is_active=data.get("is_active", True),
        user_id=data.get("id"),
    )