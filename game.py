import random
from player import Player

class Game:
    def __init__(self):
        self.players = {}
        self.battles = {}
        
    def add_player(self, username, user_id):
        if user_id not in self.players:
            self.players[user_id] = {'username': username, 'hp': 100, 'attack': 10}
            print (self.players)

    def remove_player(self, user_id):
        if user_id in self.players:
            del self.players[user_id]
        
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

    def get_username(self, user_id):
        return self.players.get(user_id, {}).get('username', '')
