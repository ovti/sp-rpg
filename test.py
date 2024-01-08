@app.route('/hotseat_fight')
def hotseat_fight():
    if session['key'] in games:
        game = games[session['key']]
        player1 = game.player1
        player2 = game.player2
        enemy = game.enemies.get(game.levels[game.current_level]['enemy'])
        current_player = game.current_player

        if player1.is_alive() and player2.is_alive() and enemy.is_alive():
            player, enemy = game.fight(current_player, enemy, is_not_solo=True)
            if not player.is_alive():
                return redirect(url_for('game_over', result='lost'))
            elif not enemy.is_alive():
                return redirect(url_for('between_levels_hotseat'))
            return redirect(url_for('hotseat_start'))

        else:
            return redirect(url_for('index'))


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
