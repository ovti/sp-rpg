from flask import Flask, render_template, request, redirect, url_for, session
import uuid
from game import Game

app = Flask(__name__)
app.secret_key = 'some_secret'
game = Game()

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'key' not in session:
        session['key'] = str(uuid.uuid4())
    
    if 'player_hp' not in session:
        session['player_hp'] = 100
        
    if request.method == 'POST':
        game.player_attack()  
        game.ai_attack()
        
        
    return render_template('index.html', status=game.get_player_status(), dead=game.is_dead())

if __name__ == '__main__':
    app.run(debug=True)

# @app.route("/", methods =["GET", "POST"])
# def home():
#     player_name = None 
#     if request.method == 'POST':
#         player_name = request.form.get('player_name')
#     return render_template('home.html', player_name=player_name)

# @app.route("/hello")
# def hello():
#     return render_template("hello.html")


# if __name__ == '__main__':
#     app.run(host='wierzba.wzks.uj.edu.pl', port=5127, debug=True)

