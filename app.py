from flask import Flask, render_template, request, session, redirect, url_for
import uuid
from game import Game

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key'

games = {}


@app.route('/')
def index():
    if 'key' not in session:
        session['key'] = uuid.uuid4()
    return render_template('index.html')


@app.route('/singleplayer')
def singleplayer():
    return render_template('singleplayer/singleplayer.html')


@app.route('/singleplayer_start', methods=['POST'])
def singleplayer_start():
    if session['key'] not in games:
        games[session['key']] = Game()
    return redirect(url_for('solo'))


@app.route('/solo')
def solo():
    if session['key'] in games:
        game = games[session['key']]
        character, enemy, level = game.start_solo()
        return render_template('singleplayer/solo.html', character=character, enemy=enemy, level=level)
    else:
        return redirect(url_for('index'))


@app.route('/fight')
def fight():
    if session['key'] in games:
        game = games[session['key']]
        character = game.characters['warrior']  # Example
        enemy = game.enemies.get(game.levels[game.current_level]['enemy'])

        result = game.fight(character, enemy)

        if isinstance(result, tuple):
            character, enemy = result
            return render_template('singleplayer/fight.html', character=character, enemy=enemy)
        else:
            return result
    else:
        return redirect(url_for('index'))


@app.route('/next_level')
def next_level():
    if session['key'] in games:
        game = games[session['key']]
        if game.next_level():
            return redirect(url_for('solo'))
        else:
            return "Congratulations! You completed all levels."
    else:
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
