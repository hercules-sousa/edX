import os

from flask import Flask, render_template
from flask_socketio import SocketIO, emit

messages = {'main': []}

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/chat")
def test():
    return render_template("chat.html")


@socketio.on("message_test")
def print_message(data):
    print(data['data'])


@socketio.on("message")
def message(data):
    print(data)