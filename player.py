class Player:
    def __init__(self, name, character, health, attack):
        self.name = name
        self.character = character
        self.health = health
        self.attack = attack
        self.potions = {'health': 3, 'attack': 3}

    def take_damage(self, damage):
        self.health -= damage

    def use_potion(self, potion):
        if self.potions[potion] > 0:
            if potion == 'health':
                self.health += 10
                self.potions[potion] -= 1
            elif potion == 'attack':
                self.attack += 5
                self.potions[potion] -= 1

    def is_alive(self):
        return self.health > 0
