from player import Player


class Game:
    def __init__(self):
        self.players = {}
        self.battles = {}
        self.bosses = {1: {'name': 'Stan', 'hp': 100, 'attack': 10, 'defeated': False},
                       2: {'name': 'Kyle', 'hp': 200, 'attack': 20, 'defeated': False},
                       3: {'name': 'Cartman', 'hp': 300, 'attack': 30, 'defeated': False},
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

    def start_battle(self, user_id, opponent_id):
        player = self.players.get(user_id)
        opponent = self.bosses.get(opponent_id)

        if player and opponent:
            battle_result = self._perform_battle(player, opponent)

            if battle_result:
                return True  # Player won the battle
            else:
                return False  # Player lost the battle

        return None  # Invalid player or boss

    def _perform_battle(self, player, opponent):
        # Logic for battle
        while player['hp'] > 0 and opponent['hp'] > 0:
            # Simulate a simple battle where each participant attacks in turn
            opponent['hp'] -= player['attack']
            player['hp'] -= opponent['attack']

        if player['hp'] > 0:
            player['defeated'] = False
            return True  # Player won
        else:
            player['defeated'] = True
            return False  # Player lost
