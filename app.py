from flask import Flask, render_template, request, redirect, url_for, session
import uuid
from game import Game

app = Flask(__name__)
app.secret_key = 'some_secret'
games = {}

@app.route('/')
def start():
    if 'key' not in session:
        session['key'] = str(uuid.uuid4())
    
    # if session['key'] not in games:
    #     games[session['key']] = Game()    
        
    return render_template('start.html')
    

@app.route('/form', methods=['GET', 'POST'])
def form():
    return 'hello';


@app.route('/battle', methods=['GET', 'POST'])
def battle():
    
    if request.method == 'POST':
        games[session['key']].player_attack()
        games[session['key']].ai_attack()
        return redirect(url_for('battle'))  # Redirect after POST
        
    return render_template('battle.html', status=games[session['key']].get_player_status(), dead=games[session['key']].is_dead())

if __name__ == '__main__':
    
    app.run(debug=True)