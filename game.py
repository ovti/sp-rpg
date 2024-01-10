from player import Player


class Game:
    def __init__(self):

        self.enemies = {
            'butters': Player('Butters', 'Enemy', 30, 8),
            'stan': Player('Stan', 'Enemy', 70, 12),
            'kyle': Player('Kyle', 'Enemy', 150, 20),
        }

        self.levels = {
            1: {'enemy': 'butters'},
            2: {'enemy': 'stan'},
            3: {'enemy': 'kyle'},
        }

        self.current_level = 1
        self.current_player = None
        self.player1 = None
        self.player2 = None

        self.is_not_solo = False

    def create_player(self, name, character):
        if character == 'fighter':
            return Player(name, 'Fighter', 15, 10)
        elif character == 'mage':
            return Player(name, 'Mage', 80, 15)
        elif character == 'thief':
            return Player(name, 'Thief', 90, 12)

    def get_info(self):
        enemy = self.enemies.get(self.levels[self.current_level]['enemy'])
        return enemy, self.current_level

    def switch_player(self):
        if self.current_player == self.player1:
            self.current_player = self.player2
        else:
            self.current_player = self.player1
        return self.current_player

    def fight(self, player, enemy, is_not_solo=False):
        if player.is_alive() and enemy.is_alive():
            enemy.take_damage(player.attack)
            player.take_damage(enemy.attack)
            if is_not_solo:
                self.switch_player()
            return player, enemy

    # pvp fight in multiplayer mode
    def pvp_fight(self, attacker, opponent):
        if attacker.is_alive() and opponent.is_alive():
            opponent.take_damage(attacker.attack)
            print('{} attacked {} for {} damage'.format(attacker.name, opponent.name, attacker.attack))
            self.switch_player()
            return attacker, opponent

    def is_last_level(self):
        return self.current_level == len(self.levels)

    def next_level(self):
        self.current_level += 1

        if self.current_level <= len(self.levels):
            return True
        else:
            return False

    def are_there_two_players(self):
        if self.player1 and self.player2:
            return True
