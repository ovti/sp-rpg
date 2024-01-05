class Player:
    def __init__(self, name, character, health, attack):
        self.name = name
        self.character = character
        self.health = health
        self.attack = attack

    def take_damage(self, damage):
        self.health -= damage

    def is_alive(self):
        return self.health > 0
