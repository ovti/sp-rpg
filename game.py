from flask import flash
import random
from player import Player


class Game:
    def __init__(self):

        self.enemies = {
            'kid1': Player('Kid1', 'Enemy', 25, 5, 0, 1, 1),
            'scott': Player('Scott', 'Enemy', 30, 6, 0, 2, 1),
            'kid2': Player('Kid2', 'Enemy', 40, 8, 0, 0, 1),
            'tweek': Player('Tweek', 'Enemy', 50, 10, 0, 1, 0),
            'kid3': Player('Kid3', 'Enemy', 60, 12, 0, 2, 1),
            'clyde': Player('Clyde', 'Enemy', 70, 14, 0, 1, 2),
            'kid4': Player('Kid4', 'Enemy', 80, 16, 0, 2, 2),
            'craig': Player('Craig', 'Enemy', 90, 18, 0, 2, 2),
            'butters': Player('Butters', 'Enemy', 50, 12, 0, 1, 1),
            'token': Player('Token', 'Enemy', 90, 12, 0, 1, 1),
            'stan': Player('Stan', 'Enemy', 110, 12, 0, 1, 1),
            'kyle': Player('Kyle', 'Enemy', 130, 20, 0, 2, 2),
            'cartman': Player('Cartman', 'Enemy', 200, 25, 0, 3, 3),
        }

        self.levels = {
            1: {'enemy': 'kid1'},
            2: {'enemy': 'scott'},
            3: {'enemy': 'kid2'},
            4: {'enemy': 'tweek'},
            5: {'enemy': 'kid3'},
            6: {'enemy': 'clyde'},
            7: {'enemy': 'kid4'},
            8: {'enemy': 'craig'},
            9: {'enemy': 'butters'},
            10: {'enemy': 'token'},
            11: {'enemy': 'stan'},
            12: {'enemy': 'kyle'},
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
            return Player(name, 'Fighter', 100, 10, 15, 1, 1)
        elif character == 'mage':
            return Player(name, 'Mage', 80, 15, 5, 1, 1)
        elif character == 'thief':
            return Player(name, 'Thief', 90, 12, 25, 1, 0)
        elif character == 'priest':
            return Player(name, 'Priest', 60, 12, 15, 0, 2)

    def get_info(self):
        enemy = self.enemies.get(self.levels[self.current_level]['enemy'])
        if self.player1 and self.player2:
            enemy.boost_stats()
        return enemy, self.current_level

    def switch_player(self):
        if self.current_player == self.player1:
            self.current_player = self.player2
        else:
            self.current_player = self.player1
        return self.current_player

    def enemy_move(self, enemy, player):
        if enemy.is_alive():
            if enemy.health < 25 and enemy.attack_potions > 0:
                self.attack_potion(enemy)
            if enemy.health < 15 and enemy.health_potions > 0:
                self.heal(enemy)
            else:
                if player.character == 'Fighter':
                    if random.randint(1, 10) >= 8:
                        flash('{} blocked the attack'.format(player.name))
                    else:
                        self.enemy_attack(enemy, player)
                        flash('{} attacked player {} for {} damage'.format(enemy.name, player.name, enemy.attack))
                else:
                    self.enemy_attack(enemy, player)
                    flash('{} attacked player {} for {} damage'.format(enemy.name, player.name, enemy.attack))

    def check_enemy_enrage(self, enemy):
        if enemy.health <= enemy.max_health * 0.3:
            if random.randint(1, 10) >= 8:
                enemy.attack *= 1.5
                flash('{} enraged and increased its attack by 50%'.format(enemy.name))

    def heal(self, character):
        if character.character == 'Mage':
            if character.health_potions > 0:
                character.health += 10
                character.health_potions -= 1
                flash('{} used a health potion'.format(character.name))
        elif character.health_potions > 0 and character.action_points > 0:
            character.health += 10
            character.health_potions -= 1
            character.action_points -= 1
            flash('{} used a health potion'.format(character.name))

    def attack_potion(self, character):
        if character.character == 'Mage':
            if character.attack_potions > 0:
                character.attack += 5
                character.attack_potions -= 1
                flash('{} used an attack potion'.format(character.name))
        elif character.attack_potions > 0 and character.action_points > 0:
            character.attack += 5
            character.attack_potions -= 1
            character.action_points -= 1
            flash('{} used an attack potion'.format(character.name))

    def mysterious_potion(self, character):
        if character.mysterious_potions > 0 and character.action_points >= 5:
            character.health += 50
            character.attack += 50
            character.mysterious_potions -= 1
            character.action_points -= 5
            flash('{} used a mysterious potion'.format(character.name))

    def priest_heal(self, character):
        if character.character == 'Priest' and character.action_points >= 2:
            character.health += 5
            character.action_points -= 2
            flash('{} used a priest heal'.format(character.name))

    def enemy_attack(self, attacker, target):
        target.take_damage(attacker.attack)
        attacker.action_points = 5

    def perform_player_move(self, player, action):
        moves = {
            'attack': self.player_attack,
            'quick_attack': self.quick_attack,
            'heal': self.heal,
            'attack_potion': self.attack_potion,
            'mysterious_potion': self.mysterious_potion,
            'priest_heal': self.priest_heal,
        }

        if action in moves:
            return moves[action](player)
        else:
            return None

    def player_attack(self, player):
        if player.action_points >= 4:
            player.action_points -= 4
            if player.character == 'Thief':
                if random.randint(1, 10) >= 7:
                    return player.attack * 2
                else:
                    return player.attack
            else:
                return player.attack

    def quick_attack(self, player):
        if player.action_points >= 1:
            if random.randint(1, 10) > 4:
                player.action_points -= 1
                return player.attack / 2
            else:
                player.action_points -= 1
                player.health -= 5
                flash('Quick attack failed and enemy hit back for 5 damage')
                return None

    def fight(self, player, action, enemy, is_not_solo=False, is_pvp=False):
        if player.is_alive() and enemy.is_alive() and not is_pvp:
            if action == 'pass':
                flash('{} passed the turn'.format(player.name))
                self.check_enemy_enrage(enemy)
                self.enemy_move(enemy, player)
                player.action_points = 5
                if is_not_solo:
                    self.switch_player()

            if player.action_points > 0:
                damage_dealt = self.perform_player_move(player, action)
                if damage_dealt is not None:
                    flash('{} attacked {} for {} damage'.format(player.name, enemy.name, damage_dealt))
                    enemy.take_damage(damage_dealt)

            if player.action_points <= 0:
                self.check_enemy_enrage(enemy)
                self.enemy_move(enemy, player)
                player.action_points = 5
                if is_not_solo:
                    self.switch_player()

        elif player.is_alive() and enemy.is_alive() and is_pvp:
            if action == 'pass':
                flash('{} passed the turn'.format(player.name))
                player.action_points = 5
                self.switch_player()

            if player.action_points > 0:
                damage_dealt = self.perform_player_move(player, action)
                if damage_dealt is not None:
                    flash('{} attacked {} for {} damage'.format(player.name, enemy.name, damage_dealt))
                    if enemy.character == 'Fighter':
                        if random.randint(1, 10) >= 8:
                            flash('{} blocked the attack'.format(enemy.name))
                        else:
                            enemy.take_damage(damage_dealt)
                            flash('{} took {} damage'.format(enemy.name, damage_dealt))
                    else:
                        enemy.take_damage(damage_dealt)
                        flash('{} took {} damage'.format(enemy.name, damage_dealt))

            if player.action_points <= 0:
                player.action_points = 5
                self.switch_player()

        return player, enemy

    def is_last_level(self):
        return self.current_level == len(self.levels)

    def next_level(self):
        self.current_level += 1
        if self.current_level <= len(self.levels):
            return True
        else:
            return False

    def are_there_two_players(self):
        return self.player1 and self.player2

    def vendor(self, player, action):
        if action == 'health' and player.gold >= 10:
            player.health_potions += 1
            player.gold -= 10
        elif action == 'attack' and player.gold >= 15:
            player.attack_potions += 1
            player.gold -= 15
        elif action == 'mysterious-potion' and player.gold >= 250:
            player.mysterious_potions += 1
            player.gold -= 250

    def give_gold(self, player):
        player.gold += 20

    def reset_action_points(self, player):
        if self.is_not_solo:
            self.player1.action_points = 5
            self.player2.action_points = 5
        else:
            player.action_points = 5
