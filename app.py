from flask import Flask, render_template, request, session, redirect, url_for
import uuid

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'


@app.route('/')
def index():
    return 'test'


if __name__ == '__main__':
    app.run(debug=True)
