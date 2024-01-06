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


@app.route('/singleplayer_start', methods=['POST', 'GET'])
def singleplayer_start():
    if session['key'] not in games:
        name = request.form['name']
        character = request.form['character']

        if name and character:
            games[session['key']] = Game()
            game = games[session['key']]
            game.player = game.create_player(name, character)
            enemy, level = game.start_solo()
            return render_template('singleplayer/solo.html', player=game.player, enemy=enemy, level=level)
            # return 'Name: {}<br>Character: {}<br>Enemy: {}<br>Level: {}'.format(name, character, enemy.name, level)
            # return redirect(url_for('solo'))
        else:
            return redirect(url_for('index'))

    return redirect(url_for('solo'))


@app.route('/fight')
def fight():
    if session['key'] in games:
        game = games[session['key']]
        player = game.player
        enemy = game.enemies.get(game.levels[game.current_level]['enemy'])

        if player.is_alive() and enemy.is_alive():
            player, enemy = game.fight(player, enemy)
            return render_template('singleplayer/solo.html', player=player, enemy=enemy, level=game.current_level)
        else:
            return redirect(url_for('between_levels'))
    else:
        return redirect(url_for('index'))

    #     if player.is_alive() and enemy.is_alive():
    #         player, enemy = game.fight(player, enemy)
    #         return render_template('singleplayer/solo.html', player=player, enemy=enemy, level=game.current_level)
    #     else:
    #         return redirect(url_for('next_level'))
    # else:
    #     return redirect(url_for('index'))


@app.route('/between_levels', methods=['POST', 'GET'])
def between_levels():
    if session['key'] in games:
        game = games[session['key']]
        if request.method == 'POST':
            stat = request.form['stat']
            game.player.level_up(stat)
        return render_template('singleplayer/between_levels.html')
    else:
        return redirect(url_for('index'))


@app.route('/next_level')
def next_level():
    if session['key'] in games:
        game = games[session['key']]
        game.next_level()

        if game.current_level <= len(game.levels):
            enemy, level = game.start_solo()
            return render_template('singleplayer/solo.html', player=game.player, enemy=enemy, level=level)
        else:
            return 'You won!'
    else:
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True, port=8000)
