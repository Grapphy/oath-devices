import random

class User:
    id: str
    name: str
    password: str
    oath_secret: str
    backup_codes: list
    mfa_enabled: bool

    def __init__(self, id: str, name: str, password: str):
        self.id = id
        self.name = name
        self.password = password
        self.oath_secret = None
        self.backup_codes = None
        self.mfa_enabled = False


data = [
    User("1", "Carlo Magno", "TestPassword")
]


def get_user_by_id(user_id: str):
    for user in data:
        if user.id == user_id:
            return user


def get_user_by_username(username: str):
    for user in data:
        if user.name == username:
            return user


def create_user(username: str, password: str):
    user = User(random.randint(2, 999999), username, password)
    data.append(user)
    return user