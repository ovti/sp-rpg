from flask import Flask, render_template, request, session, redirect, url_for
import uuid
from game import Game

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key'

games = {}


@app.route('/')
def index():
    if 'key' in session:
        if session['key'] in games:
            del games[session['key']]
        session.pop('key', None)
    if 'key' not in session:
        session['key'] = uuid.uuid4()
    return render_template('index.html')


############### SINGLEPLAYER #####################

@app.route('/singleplayer')
def singleplayer():
    if session['key'] in games:
        game = games[session['key']]
        return render_template('singleplayer/solo.html', player=game.player,
                               enemy=game.enemies.get(game.levels[game.current_level]['enemy']),
                               level=game.current_level)
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
            enemy, level = game.get_info()
            return render_template('singleplayer/solo.html', player=game.player, enemy=enemy, level=level)
        else:
            return redirect(url_for('index'))

    return redirect(url_for('singleplayer'))


@app.route('/fight')
def fight():
    if session['key'] in games:
        game = games[session['key']]
        player = game.player
        enemy = game.enemies.get(game.levels[game.current_level]['enemy'])

        if player.is_alive() and enemy.is_alive():
            player, enemy = game.fight(player, enemy)
            if not player.is_alive():
                return redirect(url_for('game_over', result='lost'))
            elif not enemy.is_alive():
                return redirect(url_for('between_levels'))
            return redirect(url_for('singleplayer'))
    else:
        return redirect(url_for('index'))


@app.route('/between_levels', methods=['POST', 'GET'])
def between_levels():
    if session['key'] in games:
        game = games[session['key']]
        if game.is_last_level():
            return redirect(url_for('game_over', result='win'))
        if request.method == 'POST':
            stat = request.form['stat']
            game.player.level_up(stat)
            return redirect(url_for('next_level'))
        return render_template('singleplayer/between_levels.html')
    else:
        return redirect(url_for('index'))


@app.route('/next_level', methods=['POST', 'GET'])
def next_level():
    if session['key'] in games:
        game = games[session['key']]
        game.next_level()
        if game.current_level <= len(game.levels):
            enemy, level = game.get_info()
            return redirect(url_for('singleplayer_start'))
        else:
            return 'You won!'
    else:
        return redirect(url_for('index'))


############### SINGLEPLAYER #####################

############### HOTSEAT #####################

@app.route('/hotseat')
def hotseat():
    if session['key'] in games:
        game = games[session['key']]
        return render_template('hotseat/hot.html', player1=game.player1, player2=game.player2,
                               enemy=game.enemies.get(game.levels[game.current_level]['enemy']),
                               level=game.current_level, current_player=game.current_player)
    return render_template('hotseat/hotseat.html')


@app.route('/hotseat_start', methods=['POST', 'GET'])
def hotseat_start():
    if session['key'] not in games:
        name1 = request.form['name1']
        character1 = request.form['character1']
        name2 = request.form['name2']
        character2 = request.form['character2']

        if name1 and character1 and name2 and character2:
            games[session['key']] = Game()
            game = games[session['key']]
            game.player1 = game.create_player(name1, character1)
            game.player2 = game.create_player(name2, character2)
            game.current_player = game.player1
            enemy, level = game.get_info()
            return render_template('hotseat/hot.html', player1=game.player1, player2=game.player2, enemy=enemy,
                                   level=level)
        else:
            return redirect(url_for('index'))

    return redirect(url_for('hotseat'))


@app.route('/hotseat_fight')
def hotseat_fight():
    if session['key'] in games:
        game = games[session['key']]
        player1 = game.player1
        player2 = game.player2
        enemy = game.enemies.get(game.levels[game.current_level]['enemy'])
        current_player = game.current_player

        if player1.is_alive() and player2.is_alive() and enemy.is_alive():
            player, enemy = game.fight(current_player, enemy, is_hotseat=True)
            if not player.is_alive():
                return redirect(url_for('game_over', result='lost'))
            elif not enemy.is_alive():
                return redirect(url_for('between_levels_hotseat'))
            return redirect(url_for('hotseat_start'))

        else:
            return redirect(url_for('index'))


@app.route('/between_levels_hotseat', methods=['POST', 'GET'])
def between_levels_hotseat():
    if session['key'] in games:
        game = games[session['key']]
        if game.is_last_level():
            return redirect(url_for('game_over', result='win'))
        if request.method == 'POST':
            player1_stat = request.form['player1_stat']
            player2_stat = request.form['player2_stat']
            game.player1.level_up(player1_stat)
            game.player2.level_up(player2_stat)
            return redirect(url_for('next_level_hotseat'))
        return render_template('hotseat/between_levels_hotseat.html', player1=game.player1, player2=game.player2)
    else:
        return redirect(url_for('index'))


@app.route('/next_level_hotseat', methods=['POST', 'GET'])
def next_level_hotseat():
    if session['key'] in games:
        game = games[session['key']]
        game.next_level()
        if game.current_level <= len(game.levels):
            enemy, level = game.get_info()
            return redirect(url_for('hotseat_start'))
        else:
            return 'You won!'
    else:
        return redirect(url_for('index'))


############### HOTSEAT #####################

@app.route('/game_over/<result>')
def game_over(result):
    if session['key'] in games:
        game = games[session['key']]
        del games[session['key']]
        return render_template('game_over.html', result=result)
    else:
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True, port=8000)
