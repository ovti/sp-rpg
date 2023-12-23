from flask import Flask, render_template, redirect, url_for 
  
app = Flask(__name__) 

@app.route("/hello") 
def home(): 
    return render_template("hello.html") 