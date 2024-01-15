from flask import Flask, render_template, request, session, redirect, url_for
import uuid
import itertools
from game import Game

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key'
SESSION_TYPE = 'redis'

games = {}
multiplayer_games = {}
multiplayer_games_id = itertools.count()


@app.route('/')
def index():
    if 'key' in session:
        if session['key'] in games:
            del games[session['key']]
        session.pop('key', None)
    if 'key' not in session:
        session['key'] = uuid.uuid4()
    if 'game_id' in session:
        multiplayer_games.pop(session['game_id'], None)
        session.pop('game_id', None)
    if 'player1' in session:
        session.pop('player1', None)
    if 'player2' in session:
        session.pop('player2', None)

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
            # game.current_player = game.player
            enemy, level = game.get_info()
            return render_template('singleplayer/solo.html', player=game.player, enemy=enemy, level=level)
        else:
            return redirect(url_for('index'))

    return redirect(url_for('singleplayer'))


@app.route('/fight', methods=['POST', 'GET'])
def fight():
    if session['key'] in games:
        game = games[session['key']]
        player = game.player
        enemy = game.enemies.get(game.levels[game.current_level]['enemy'])
        if request.method == 'POST':
            action = request.form['action']
        else:
            action = None
        if player.is_alive() and enemy.is_alive():
            player, enemy = game.fight(player, action, enemy)
            if not player.is_alive():
                return redirect(url_for('game_over', result='lost'))
            elif not enemy.is_alive():
                game.reset_action_points(player)
                game.give_gold(player)
                return redirect(url_for('between_levels'))
            return redirect(url_for('singleplayer'))
    else:
        return redirect(url_for('index'))


@app.route('/vendor', methods=['POST', 'GET'])
def vendor():
    if session['key'] in games:
        game = games[session['key']]
        player = game.player
        if request.method == 'POST':
            action = request.form['action']
        else:
            action = None
        game.vendor(player, action)
        return render_template('singleplayer/between_levels.html', player=game.player)
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
        return render_template('singleplayer/between_levels.html', player=game.player)
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
            enemy.boost_stats()
            return render_template('hotseat/hot.html', player1=game.player1, player2=game.player2, enemy=enemy,
                                   level=level, current_player=game.current_player)
        else:
            return redirect(url_for('index'))

    return redirect(url_for('hotseat'))


@app.route('/hotseat_fight', methods=['POST', 'GET'])
def hotseat_fight():
    if session['key'] in games:
        game = games[session['key']]
        player1 = game.player1
        player2 = game.player2
        enemy = game.enemies.get(game.levels[game.current_level]['enemy'])
        current_player = game.current_player
        if request.method == 'POST':
            action = request.form['action']
        else:
            action = None
        if player1.is_alive() and player2.is_alive() and enemy.is_alive():
            player, enemy = game.fight(current_player, action, enemy, is_not_solo=True)
            if not player.is_alive():
                return redirect(url_for('game_over', result='lost'))
            elif not enemy.is_alive():
                game.reset_action_points(player1)
                game.reset_action_points(player2)
                game.give_gold(player1)
                game.give_gold(player2)
                return redirect(url_for('between_levels_hotseat'))
            return redirect(url_for('hotseat_start'))

        else:
            return redirect(url_for('index'))


# @app.route('/hotseat_fight')
# def hotseat_fight():
#     if session['key'] in games:
#         game = games[session['key']]
#         player1 = game.player1
#         player2 = game.player2
#         enemy = game.enemies.get(game.levels[game.current_level]['enemy'])
#         current_player = game.current_player
#
#         if player1.is_alive() and player2.is_alive() and enemy.is_alive():
#             player, enemy = game.fight(current_player, enemy, is_not_solo=True)
#             if not player.is_alive():
#                 return redirect(url_for('game_over', result='lost'))
#             elif not enemy.is_alive():
#                 return redirect(url_for('between_levels_hotseat'))
#             return redirect(url_for('hotseat_start'))
#
#         else:
#             return redirect(url_for('index'))


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


@app.route('/vendor_hotseat_1', methods=['POST', 'GET'])
def vendor_hotseat_1():
    if session['key'] in games:
        game = games[session['key']]
        player = game.player1
        if request.method == 'POST':
            action = request.form['action']
        else:
            action = None
        game.vendor(player, action)
        return render_template('hotseat/between_levels_hotseat.html', player1=game.player1, player2=game.player2)
    else:
        return redirect(url_for('index'))


@app.route('/vendor_hotseat_2', methods=['POST', 'GET'])
def vendor_hotseat_2():
    if session['key'] in games:
        game = games[session['key']]
        player = game.player2
        if request.method == 'POST':
            action = request.form['action']
        else:
            action = None
        game.vendor(player, action)
        return render_template('hotseat/between_levels_hotseat.html', player1=game.player1, player2=game.player2)
    else:
        return redirect(url_for('index'))


# @app.route('/vendor', methods=['POST', 'GET'])
# def vendor():
#     if session['key'] in games:
#         game = games[session['key']]
#         player = game.player
#         if request.method == 'POST':
#             action = request.form['action']
#         else:
#             action = None
#         game.vendor(player, action)
#         return render_template('singleplayer/between_levels.html', player=game.player)
#     else:
#         return redirect(url_for('index'))


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

############### MULTIPLAYER #####################
@app.route('/multiplayer')
def multiplayer():
    return render_template('multiplayer/multiplayer.html', multiplayer_games=multiplayer_games)


@app.route('/multiplayer_new')
def multiplayer_new():
    return render_template('multiplayer/multiplayer_new.html')


@app.route('/multiplayer_start', methods=['POST'])
def multiplayer_start():
    name = request.form['name']
    character = request.form['character']
    if name and character:
        game_id = next(multiplayer_games_id)
        multiplayer_games[game_id] = Game()
        game = multiplayer_games[game_id]
        game.player1 = game.create_player(name, character)
        game.current_player = game.player1
        session['game_id'] = game_id
        session['player1'] = 'player1'
        return redirect('/multiplayer_wait')
    else:
        return redirect(url_for('index'))


@app.route('/multiplayer_join/', methods=['POST', 'GET'])
def multiplayer_join():
    if request.method == 'POST':
        game_id = request.form['game_id']
        game_id = int(game_id)
        if game_id in multiplayer_games:
            game = multiplayer_games[game_id]
            name = request.form['name']
            character = request.form['character']
            if name and character:
                game.player2 = game.create_player(name, character)
                session['game_id'] = game_id
                session['player2'] = 'player2'
                return redirect('/multiplayer_wait')
            else:
                return redirect(url_for('index'))
        else:
            return redirect(url_for('index'))
    else:
        if request.method == 'GET':
            game_id = request.args.get('game')
            return render_template('multiplayer/multiplayer_join.html', game_id=game_id)


@app.route('/multiplayer_wait', methods=['POST', 'GET'])
def multiplayer_wait():
    if 'game_id' in session:
        game_id = session['game_id']
        if game_id in multiplayer_games:
            game = multiplayer_games[game_id]
            if game.player1 and game.player2:
                return redirect('/multiplayer_fight')
            return render_template('multiplayer/multiplayer_wait.html', game=game)
        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))


@app.route('/multiplayer_fight')
def multiplayer_fight():
    if 'game_id' in session:
        game_id = session['game_id']
        if game_id in multiplayer_games:
            game = multiplayer_games[game_id]
            player1 = game.player1
            player2 = game.player2

            if player1.is_alive() and player2.is_alive():
                if not ('player1' in session or 'player2' in session):
                    return redirect(url_for('index'))
                return render_template('multiplayer/multiplayer_fight.html', player1=game.player1,
                                       player2=game.player2, level=game.current_level,
                                       current_player=game.current_player)
            else:
                return redirect(url_for('index'))

    return redirect(url_for('index'))


@app.route('/multiplayer_attack', methods=['POST', 'GET'])
def multiplayer_attack():
    if 'game_id' in session:
        game_id = session['game_id']
        if game_id in multiplayer_games:
            game = multiplayer_games[game_id]
            player1 = game.player1
            player2 = game.player2
            current_player = game.current_player
            if request.method == 'POST':
                action = request.form['action']
            else:
                action = None
            if player1.is_alive() and player2.is_alive():
                attacker, opponent = game.fight(current_player, action,
                                                player2 if current_player == player1 else player1, is_pvp=True)
                if not attacker.is_alive():
                    return redirect(url_for('game_over', result='lost'))
                elif not opponent.is_alive():
                    return redirect(url_for('multiplayer_result'))
                return redirect(url_for('multiplayer_fight'))
            else:
                return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))


# @app.route('/multiplayer_attack', methods=['POST', 'GET'])
# def multiplayer_attack():
#     if 'game_id' in session:
#         game_id = session['game_id']
#         if game_id in multiplayer_games:
#             game = multiplayer_games[game_id]
#             player1 = game.player1
#             player2 = game.player2
#             current_player = game.current_player
#             if player1.is_alive() and player2.is_alive():
#                 attacker, opponent = game.pvp_fight(current_player, player2 if current_player == player1 else player1)
#                 if not attacker.is_alive():
#                     return redirect(url_for('game_over', result='lost'))
#                 elif not opponent.is_alive():
#                     return redirect(url_for('multiplayer_result'))
#                 return redirect(url_for('multiplayer_fight'))
#             else:
#                 return redirect(url_for('index'))
#     else:
#         return redirect(url_for('index'))


@app.route('/multiplayer_result', methods=['POST', 'GET'])
def multiplayer_result():
    if 'game_id' in session:
        game_id = session['game_id']
        if game_id in multiplayer_games:
            game = multiplayer_games[game_id]
            if game.is_last_level():
                return redirect(url_for('game_over', result='win'))
            if request.method == 'POST':
                player1_stat = request.form['player1_stat']
                player2_stat = request.form['player2_stat']
                game.player1.level_up(player1_stat)
                game.player2.level_up(player2_stat)
                return redirect(url_for('next_level_multiplayer'))
            return render_template('multiplayer/multiplayer_result.html', player1=game.player1,
                                   player2=game.player2)
        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))


############### MULTIPLAYER #####################

@app.route('/game_over/<result>')
def game_over(result):
    if session['key'] in games:
        game = games[session['key']]
        del games[session['key']]
        return render_template('game_over.html', result=result)
    else:
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=12122, debug=True)
