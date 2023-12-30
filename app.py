from flask import Flask, render_template, redirect, url_for 
  
app = Flask(__name__) 
app.secret_key = "secret key"

@app.route("/") 
def home(): 
    return render_template("hello.html") 

if __name__ == '__main__':
    app.run(host='wierzba.wzks.uj.edu.pl', port=5119, debug=True)

