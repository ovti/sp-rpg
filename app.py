from flask import Flask, render_template, redirect, url_for, request 
  
app = Flask(__name__) 
app.secret_key = "secret key"

@app.route("/", methods =["GET", "POST"])
def home():
    player_name = None 
    if request.method == 'POST':
        player_name = request.form.get('player_name')

    return render_template('home.html', player_name=player_name)

@app.route("/hello")
def hello():
    return render_template("hello.html")


if __name__ == '__main__':
    app.run(host='wierzba.wzks.uj.edu.pl', port=5127, debug=True)

