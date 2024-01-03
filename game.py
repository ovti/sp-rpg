import random
from player import Player


class Game:
    def __init__(self):
        self.players = {}
        self.battles = {}
        self.bosses = {1: {'name': 'Stan', 'hp': 100, 'attack': 10, 'defeated': False},
                       2: {'name': 'Kyle', 'hp': 200, 'attack': 20, 'defeated': False},
                       3: {'name': 'Cartman', 'hp': 300, 'attack': 30, 'defeated': False},
                       }

    def add_player(self, username, user_id):
        if user_id not in self.players:
            self.players[user_id] = {'username': username, 'hp': 100, 'attack': 10, 'defeated': False}
            # self.players[user_id]['hp'] = random.randint(100, 200)
            print(self.players)

    def remove_player(self, user_id):
        if user_id in self.players:
            del self.players[user_id]

    def get_username(self, user_id):
        return self.players.get(user_id, {}).get('username', '')

    def get_bosses(self):
        return self.bosses
