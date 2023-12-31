class Player:
    def __init__(self, name, hp=100):
        self.name = name
        self.hp = hp

    def take_damage(self, damage):
        self.hp -= damage
        if self.hp < 0:
            self.hp = 0
