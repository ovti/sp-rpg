from player import Player


class Game:
    def __init__(self):
        # self.characters = {
        #     'fighter': Player('Fighter', 100, 10),
        #     'mage': Player('Mage', 80, 15),
        #     'thief': Player('Thief', 90, 12),
        #     'priest': Player('Priest', 70, 8),
        # }

        self.enemies = {
            'butters': Player('Butters', 'Enemy', 50, 8),
            'stan': Player('Stan', 'Enemy', 70, 12),
            'kyle': Player('Kyle', 'Enemy', 150, 20),
        }

        self.levels = {
            1: {'enemy': 'butters'},
            2: {'enemy': 'stan'},
            3: {'enemy': 'kyle'},
        }

        self.current_level = 1

    # def select_character(self, character):
    #     if character in self.characters:
    #         return True
    #     else:
    #         return False

    def create_player(self, name, character):
        if character == 'fighter':
            return Player(name, 'Fighter', 100, 10)
        elif character == 'mage':
            return Player(name, 'Mage', 80, 15)
        elif character == 'thief':
            return Player(name, 'Thief', 90, 12)

    def start_solo(self):
        enemy = self.enemies.get(self.levels[self.current_level]['enemy'])
        return enemy, self.current_level

    def fight(self, player, enemy):
        player.take_damage(enemy.attack)
        enemy.take_damage(player.attack)

        if player.health < 50:
            # print ('test')
            player.use_potion('health')
            print('used health potion')

        if not player.is_alive():
            pass
        if not enemy.is_alive():
            pass
        return player, enemy

    def next_level(self):
        self.current_level += 1

        if self.current_level <= len(self.levels):
            return True
        else:
            return False
