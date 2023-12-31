from flask import Flask, render_template, request, redirect, url_for
from game import Game

app = Flask(__name__)
game = Game()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        game.player_attack(10)  
        game.ai_attack(5)
    return render_template('index.html', status=game.get_player_status(), dead=game.is_dead())

if __name__ == '__main__':
    app.run(debug=True)