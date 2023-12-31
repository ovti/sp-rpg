import random
from player import Player

class Game:
    def __init__(self):
        self.player1 = Player("Cartman")
        self.ai_player = Player("Kyle")

    def player_attack(self):
        damage = random.randint(1, 3)
        self.ai_player.take_damage(damage)
        return damage
    def ai_attack(self):
        damage = random.randint(1, 3)
        self.player1.take_damage(damage)
        return damage

    def get_player_status(self):
        return f"{self.player1.name}: {self.player1.hp}  {self.ai_player.name}: {self.ai_player.hp}"
    
    def is_dead(self):
        if self.player1.hp == 0:
            return f"{self.player1.name} is dead"
        elif self.ai_player.hp == 0:
            return f"{self.ai_player.name} is dead"
        else:
            return None
