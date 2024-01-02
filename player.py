class Player:
    def __init__(self, game, username):
        self.game = game
        self.username = username

    def enter_game(self):
        self.game.add_player(self.username)

    def challenge(self, opponent):
        self.game.initiate_battle(self.username, opponent)

    def attack(self, opponent):
        return self.game.attack(self.username, opponent)
    
    # def __init__(self, name, hp=100):
    #     self.name = name
    #     self.hp = hp

    # def take_damage(self, damage):
    #     self.hp -= damage
    #     if self.hp < 0:
    #         self.hp = 0
