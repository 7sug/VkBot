class User:
    user_id = 0

    def __init__(self):
        self.health = 100
        self.money = 100
        self.exp = 100
        User.user_id += 1
