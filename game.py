from player import Player


class Game:
    def __init__(self):

        self.enemies = {
            'kid1': Player('Kid1', 'Enemy', 10, 5),
            'kid2': Player('Kid2', 'Enemy', 20, 6, 0, 1, 1),
            'kid3': Player('Kid3', 'Enemy', 30, 8, 0, 0, 1),
            'kid4': Player('Kid4', 'Enemy', 40, 10, 0, 1, 0),
            'kid5': Player('Kid5', 'Enemy', 50, 12, 0, 2, 1),
            'kid6': Player('Kid6', 'Enemy', 60, 14, 0, 1, 2),
            'kid7': Player('Kid7', 'Enemy', 70, 16, 0, 2, 2),

            'butters': Player('Butters', 'Enemy', 30, 8),
            'craig': Player('Craig', 'Enemy', 50, 10),
            'token': Player('Token', 'Enemy', 60, 12),
            'stan': Player('Stan', 'Enemy', 70, 12),
            'kyle': Player('Kyle', 'Enemy', 150, 20),
            'cartman': Player('Cartman', 'Enemy', 200, 25, 0, 3, 0),
        }

        self.levels = {
            1: {'enemy': 'kid1'},
            2: {'enemy': 'kid2'},
            3: {'enemy': 'butters'},
            4: {'enemy': 'kid3'},
            5: {'enemy': 'craig'},
            6: {'enemy': 'kid4'},
            7: {'enemy': 'token'},
            8: {'enemy': 'kid5'},
            9: {'enemy': 'stan'},
            10: {'enemy': 'kid6'},
            11: {'enemy': 'kyle'},
            12: {'enemy': 'kid7'},
            13: {'enemy': 'cartman'},
        }

        self.current_level = 1
        self.current_player = None
        self.player1 = None
        self.player2 = None

        self.is_not_solo = False

        self.game_score = 0

    def create_player(self, name, character):
        if character == 'fighter':
            return Player(name, 'Fighter', 100, 10, 15, 1, 3)  # has chance to block attack
        elif character == 'mage':
            return Player(name, 'Mage', 80, 15, 5, 1, 1)  # can cast protective spell
        elif character == 'thief':
            return Player(name, 'Thief', 90, 12, 25, 1, 2)  # has chance to parry attack
        elif character == 'priest':
            return Player(name, 'Priest', 60, 12, 15, 3, 1)  # can heal

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

    def pvp_fight(self, attacker, opponent):
        if attacker.is_alive() and opponent.is_alive():
            opponent.take_damage(attacker.attack)
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
