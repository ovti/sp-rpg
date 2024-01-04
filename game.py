from player import Player


class Game:
    def __init__(self):
        self.characters = {
            'warrior': Player('Warrior', 100, 10),
            'mage': Player('Mage', 80, 15),
            'archer': Player('Archer', 90, 12),
        }

        self.enemies = {
            'goblin': Player('Goblin', 50, 8),
            'orc': Player('Orc', 70, 12),
            'dragon': Player('Dragon', 150, 20),
        }

        self.levels = {
            1: {'enemy': 'goblin'},
            2: {'enemy': 'orc'},
            3: {'enemy': 'dragon'},
        }

        self.current_level = 1

    def select_character(self, character):
        if character in self.characters:
            return True
        else:
            return False

    def start_solo(self):
        character = self.characters['warrior']
        enemy = self.enemies.get(self.levels[self.current_level]['enemy'])
        return character, enemy, self.current_level

    def fight(self, character, enemy):
        character.take_damage(enemy.attack)
        enemy.take_damage(character.attack)

        # if not character.is_alive():
        #     return "You lost! Game over."
        #
        # if not enemy.is_alive():
        #     return "You won! Next level."

        return character, enemy

    def next_level(self):
        self.current_level += 1

        if self.current_level <= len(self.levels):
            return True
        else:
            return False
