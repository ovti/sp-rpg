from player import Player


class Game:
    def __init__(self):
        self.characters = {
            'fighter': Player('Fighter', 100, 10),
            'mage': Player('Mage', 80, 15),
            'thief': Player('Thief', 90, 12),
            'priest': Player('Priest', 70, 8),
        }

        self.enemies = {
            'butters': Player('Butters', 50, 8),
            'stan': Player('Stan', 70, 12),
            'kyle': Player('Kyle', 150, 20),
        }

        self.levels = {
            1: {'enemy': 'butters'},
            2: {'enemy': 'stan'},
            3: {'enemy': 'kyle'},
        }

        self.current_level = 1

    def select_character(self, character):
        if character in self.characters:
            return True
        else:
            return False

    def start_solo(self):
        character = self.characters['fighter']
        enemy = self.enemies.get(self.levels[self.current_level]['enemy'])
        return character, enemy, self.current_level

    def fight(self, character, enemy):
        character.take_damage(enemy.attack)
        enemy.take_damage(character.attack)

        if not character.is_alive():
            pass
        if not enemy.is_alive():
            pass
        return character, enemy

    def next_level(self):
        self.current_level += 1

        if self.current_level <= len(self.levels):
            return True
        else:
            return False
