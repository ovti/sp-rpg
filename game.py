from player import Player


class Game:
    def __init__(self):
        self.players = {}
        self.battles = {}
        self.bosses = {1: {'name': 'Stan', 'hp': 100, 'attack': 10},
                       2: {'name': 'Kyle', 'hp': 200, 'attack': 20},
                       3: {'name': 'Cartman', 'hp': 300, 'attack': 30},
                       }

    def add_player(self, name, user_id):
        if user_id not in self.players:
            self.players[user_id] = {'name': name, 'hp': 100, 'attack': 10, 'defeated': False}
            print(self.players)

    def remove_player(self, user_id):
        if user_id in self.players:
            del self.players[user_id]

    def get_name(self, user_id):
        return self.players.get(user_id, {}).get('name', '')

    def get_players(self):
        return self.players

    def get_bosses(self):
        return self.bosses
