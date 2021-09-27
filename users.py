import random
class User:
    user_id = 0

    def __init__(self):
        self.health = 100
        self.money = 100
        self.exp = 100
        self.power = 100
        clans = ['Учиха', 'Узумаки', 'Хьюго']
        self.user_clan = random.choice(clans)
        if self.user_clan == 'Учиха':
            self.Uchiha_clan()
        elif self.user_clan == 'Узумаки':
            self.Udzumaki_clan()
        elif self.user_clan == 'Хьюго':
            self.Huygo_clan()
        User.user_id += 1

    def Uchiha_clan(self):
        self.health -= 30
        self.power += 30

    def Udzumaki_clan(self):
        self.health += 30
        self.power -= 10

    def Huygo_clan(self):
        self.health -= 10
        self.power += 15



