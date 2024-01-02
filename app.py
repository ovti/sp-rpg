from flask import Flask, render_template, request, session, redirect, url_for, jsonify
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
    session['username'] = username
    player = Player(game, username)
    player.enter_game()
    return redirect(url_for('lobby'))

@app.route('/lobby')
def lobby():
    username = session.get('username')
    if not username:
        return redirect(url_for('index'))
    return render_template('lobby.html', username=username, players=game.players)




if __name__ == '__main__':
    app.run(debug=True)

# app = Flask(__name__)
# app.secret_key = 'some_secret'
# games = {}
# battles = {}

# @app.route('/')
# def start():
#     if 'key' not in session:
#         session['key'] = str(uuid.uuid4())
    
#     if session['key'] not in games:
#         games[session['key']] = Game()    
        
#     return render_template('start.html')
    

# @app.route('/create_character', methods=['GET', 'POST'])
# def form():
#     return render_template('create_character.html')

# @app.route('/enter_game', methods=['POST'])
# def enter_game():
#     username = request.form['username']
#     games[session['key']].player1.name = username
#     return 'Welcome to the game, ' + username + '!'


# @app.route('/battle', methods=['GET', 'POST'])
# def battle():
    
#     if request.method == 'POST':
#         games[session['key']].player_attack()
#         games[session['key']].ai_attack()
#         return redirect(url_for('battle'))  # Redirect after POST
        
#     return render_template('battle.html', status=games[session['key']].get_player_status(), dead=games[session['key']].is_dead())

# if __name__ == '__main__':
    
#     app.run(debug=True)