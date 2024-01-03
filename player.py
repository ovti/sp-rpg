class Player:
    def __init__(self, game, name, user_id):
        self.game = game
        self.name = name
        self.user_id = user_id

    def enter_game(self):
        self.game.add_player(self.name, self.user_id)

    def quit_game(self):
        self.game.remove_player(self.user_id)
