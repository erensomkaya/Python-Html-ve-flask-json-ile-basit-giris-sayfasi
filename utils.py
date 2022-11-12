from io import TextIOWrapper
import json

class Users:
    def __init__(self, path: str = "./users.json"):
        self.path = path
    def openfile(self, path: str = None, mode: str = "r") -> TextIOWrapper:
        file = open(path, mode=mode, encoding="utf8")
        file.close()
        return file

    def json(self):
        data = dict(users=[])
        with open(self.path, mode="w+") as file:
            file.write(json.dumps(data))
        return file
    
    def add_user(self, name, email, username, password):
        user = dict(name=name, email=email, username=username, password=password)
        try:
           with open(self.path) as file:
            user_data: dict = json.load(file)
        except:pass
        if isinstance(user_data.get("users"), list):
            user_data["users"].append(user)
            with open(self.path, mode="w+") as file:
                file.write(json.dumps(user_data))
            return self.get_user(username)
        print(1234)
    def get_user(self, username):
        with open(self.path) as file:
            user_data: dict = json.load(file)
        if isinstance(user_data.get("users"), list):
            users = user_data.get("users")
            user = [user for user in users if user.get("username").lower() == username.lower()]
            if user:
                return user[0]
            else:
                return {}
        else:
            return self.json()

