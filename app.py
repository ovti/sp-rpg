from flask import Flask, render_template, request, session, redirect, url_for, jsonify, flash
import uuid
from game import Game
from player import Player

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

game = Game()


@app.route('/')
def index():
    if session.get('user_id') and game.get_name(session.get('user_id')):
        return redirect(url_for('game_map'))
    return render_template('index.html')


@app.route('/enter_game', methods=['POST'])
def enter_game():
    name = request.form['name']
    user_id = str(uuid.uuid4())
    session['user_id'] = user_id
    player = Player(game, name, user_id)
    player.enter_game()
    return redirect(url_for('game_map'))


@app.route('/game_map', methods=['POST', 'GET'])
def game_map():
    user_id = session.get('user_id')
    name = game.get_name(user_id)
    if not user_id or not name:
        return redirect(url_for('index'))
    return render_template('game_map.html', name=name, user_id=user_id)


@app.route('/arena', methods=['POST', 'GET'])
def arena():
    user_id = session.get('user_id')
    name = game.get_name(user_id)
    if not user_id or not name:
        return redirect(url_for('index'))
    return render_template('arena.html', name=name)


@app.route('/arena_pve', methods=['POST', 'GET'])
def arena_pve():
    user_id = session.get('user_id')
    name = game.get_name(user_id)
    if not user_id or not name:
        return redirect(url_for('index'))
    boss = game.get_bosses()
    return render_template('singleplayer/arena_pve.html', name=name, boss=boss)


@app.route('/arena_pvp', methods=['POST', 'GET'])
def arena_pvp():
    user_id = session.get('user_id')
    name = game.get_name(user_id)
    if not user_id or not name:
        return redirect(url_for('index'))
    return render_template('multiplayer/arena_pvp.html', name=name, players=game.players)


@app.route('/battle/<opponent_id>', methods=['POST', 'GET'])
def battle(opponent_id):
    user_id = session.get('user_id')
    name = game.get_name(user_id)
    if not user_id or not name:
        return redirect(url_for('index'))

    player = game.get_players().get(user_id)
    opponent = game.get_bosses().get(int(opponent_id))

    return render_template('battle.html', player=player, opponent=opponent, opponent_id=opponent_id)


@app.route('/quit_game', methods=['POST', 'GET'])
def quit_game():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('index'))
    player = Player(game, None, user_id)
    player.quit_game()
    session.pop('user_id')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
