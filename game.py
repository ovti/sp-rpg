import random
from player import Player

class Game:
    def __init__(self):
        self.players = {}
        self.battles = {}
        
    def add_player(self, username):
        self.players[username] = {'hp': 100, 'attack': 10}
        
    def initiate_battle(self, attacker, opponent):
        if attacker not in self.battles:
            self.battles[attacker] = {'opponent': opponent, 'turn': attacker}
            
    def attack(self, attacker):
        if attacker not in self.battles:
            return None
        
        opponent = self.battles[attacker]['opponent']
        damage = self.players[attacker]['attack']
        self.players[opponent]['hp'] -= damage
        self.battles[attacker]['turn'] = opponent
        
        return {'attacker': attacker, 'opponent': opponent, 'damage': damage, 'turn': opponent}

    # def player_attack(self):
    #     damage = random.randint(5, 15)
    #     self.ai_player.take_damage(damage)
    #     return damage
    # def ai_attack(self):
    #     damage = random.randint(5, 15)
    #     self.player1.take_damage(damage)
    #     return damage

    # def get_player_status(self):
    #     return f"{self.player1.name}: {self.player1.hp}  {self.ai_player.name}: {self.ai_player.hp}"
    
    # def is_dead(self):
    #     if self.player1.hp == 0:
    #         return f"{self.player1.name} is dead"
    #     elif self.ai_player.hp == 0:
    #         return f"{self.ai_player.name} is dead"
    #     else:
    #         return None
