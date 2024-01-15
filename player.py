class Player:
    def __init__(self, name, character, health, attack, gold=0, health_potions=0, attack_potions=0, action_points=5):
        self.name = name
        self.character = character
        self.health = health
        self.attack = attack
        self.gold = gold
        self.health_potions = health_potions
        self.attack_potions = attack_potions
        self.action_points = action_points

    def take_damage(self, damage):
        self.health -= damage

    def level_up(self, stat):
        if stat == 'health':
            self.health += 10
            print('health increased to {}'.format(self.health))
        elif stat == 'attack':
            self.attack += 5
            print('attack increased to {}'.format(self.attack))

    def is_alive(self):
        return self.health > 0

    def boost_stats(self):
        self.health *= 2
        self.attack *= 2
