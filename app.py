from flask import Flask, render_template, request, session, redirect, url_for
import uuid
from game import Game
from player import Player

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

game = Game()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/enter_game', methods=['POST'])
def enter_game():
    username = request.form['username']
    user_id = str(uuid.uuid4())
    session['user_id'] = user_id
    player = Player(game, username, user_id)
    player.enter_game()
    return redirect(url_for('game_map'))

@app.route('/game_map', methods=['POST', 'GET'])
def game_map():
    user_id = session.get('user_id')
    username = game.get_username(user_id)
    if not user_id or not username:
        return redirect(url_for('index'))
    
    return render_template('game_map.html', username=username)

@app.route('/lobby')
def lobby():
    user_id = session.get('user_id')
    username = game.get_username(user_id)
    if not user_id or not username:
        return redirect(url_for('index'))
    return render_template('lobby.html', username=username, players=game.players)

@app.route('/quit_game', methods=['POST'])
def quit_game():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('index'))
    player = Player(game, None, user_id)
    player.quitGame()
    session.pop('user_id')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
