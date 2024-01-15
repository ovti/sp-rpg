from flask import flash
from player import Player


class Game:
    def __init__(self):

        self.enemies = {
            'kid1': Player('Kid1', 'Enemy', 10, 5),
            'scott': Player('Scott', 'Enemy', 20, 6, 0, 1, 1),
            'kid2': Player('Kid2', 'Enemy', 30, 8, 0, 0, 1),
            'tweek': Player('Tweek', 'Enemy', 40, 10, 0, 1, 0),
            'kid3': Player('Kid3', 'Enemy', 50, 12, 0, 2, 1),
            'clyde': Player('Clyde', 'Enemy', 60, 14, 0, 1, 2),
            'kid4': Player('Kid4', 'Enemy', 70, 16, 0, 2, 2),
            'craig': Player('Craig', 'Enemy', 80, 18, 0, 2, 2),
            'butters': Player('Butters', 'Enemy', 30, 8),
            'token': Player('Token', 'Enemy', 60, 12),
            'stan': Player('Stan', 'Enemy', 70, 12),
            'kyle': Player('Kyle', 'Enemy', 150, 20),
            'cartman': Player('Cartman', 'Enemy', 200, 25, 0, 3, 0),
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

        self.combat_log = []

    def add_to_combat_log(self, message):
        self.combat_log.append(message)

    def get_combat_log(self):
        return self.combat_log

    def create_player(self, name, character):
        if character == 'fighter':
            return Player(name, 'Fighter', 100, 10, 15, 6, 3)  # has chance to block attack
        elif character == 'mage':
            return Player(name, 'Mage', 80, 15, 5, 1, 1)  # can cast protective spell
        elif character == 'thief':
            return Player(name, 'Thief', 90, 12, 25, 1, 2)  # has chance to parry attack
        elif character == 'priest':
            return Player(name, 'Priest', 60, 12, 15, 3, 1)  # can heal

    def get_info(self):
        enemy = self.enemies.get(self.levels[self.current_level]['enemy'])
        if not self.is_not_solo:
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
            if enemy.health < 15 and enemy.health_potions > 0:
                self.heal(enemy)
                flash('{} used a health potion'.format(enemy.name))
            else:
                self.enemy_attack(enemy, player)
                flash('{} attacked player {} for {} damage'.format(enemy.name, player.name, enemy.attack))

    def heal(self, character):
        if character.health_potions > 0 and character.action_points > 0:
            character.health += 10
            character.health_potions -= 1
            character.action_points -= 1
            flash('{} used a health potion'.format(character.name))

    def attack_potion(self, character):
        if character.attack_potions > 0 and character.action_points > 0:
            character.attack += 5
            character.attack_potions -= 1
            character.action_points -= 1
            flash('{} used an attack potion'.format(character.name))

    def enemy_attack(self, attacker, target):
        target.take_damage(attacker.attack)
        attacker.action_points = 5

    def perform_player_move(self, player, action):
        moves = {
            'attack': self.player_attack,
            'heal': self.heal,
            'attack_potion': self.attack_potion,
        }

        if action in moves:
            return moves[action](player)
        else:
            return None

    def player_attack(self, player):
        if player.action_points >= 4:
            player.action_points -= 4
            return player.attack
        else:
            return None

    def fight(self, player, action, enemy, is_not_solo=False, is_pvp=False):
        if player.is_alive() and enemy.is_alive() and not is_pvp:
            if action == 'pass':
                flash('{} passed the turn'.format(player.name))
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
                    enemy.take_damage(damage_dealt)

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
        elif action == 'attack' and player.gold >= 10:
            player.attack_potions += 1
            player.gold -= 10

    def give_gold(self, player):
        player.gold += 10

    def reset_action_points(self, player):
        if self.is_not_solo:
            self.player1.action_points = 5
            self.player2.action_points = 5
        else:
            player.action_points = 5

    # def enemy_move(self, enemy, player):
    #     if enemy.is_alive():
    #         if enemy.health < 15 and enemy.health_potions > 0:
    #             enemy.health += 10
    #             enemy.health_potions -= 1
    #             enemy.action_points -= 1
    #         else:
    #             player.take_damage(enemy.attack)
    #             enemy.action_points = 5
    #
    # def fight(self, player, action, enemy, is_not_solo=False):
    #     if player.is_alive() and enemy.is_alive():
    #         if player.action_points > 0:
    #             if action == 'attack' and player.action_points >= 4:
    #                 enemy.take_damage(player.attack)
    #                 player.action_points -= 4
    #             elif action == 'heal' and player.health_potions > 0 and player.action_points > 0:
    #                 player.health += 10
    #                 player.health_potions -= 1
    #                 player.action_points -= 1
    #         else:
    #             self.enemy_move(enemy, player)
    #             player.action_points = 5
    #         if is_not_solo:
    #             self.switch_player()
    #     return player, enemy

    # def fight(self, player, enemy, is_not_solo=False):
    #     if player.is_alive() and enemy.is_alive():
    #         enemy.take_damage(player.attack)
    #         player.take_damage(enemy.attack)
    #         if is_not_solo:
    #             self.switch_player()
    #         return player, enemy

    # def pvp_fight(self, attacker, opponent):
    #     if attacker.is_alive() and opponent.is_alive():
    #         opponent.take_damage(attacker.attack)
    #         self.switch_player()
    #         return attacker, opponent
