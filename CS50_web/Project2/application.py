import os

from flask import Flask, render_template
from flask_socketio import SocketIO, emit, send

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


@socketio.on('confirmingConnection')
def confirmingMessage(data):
    text = data['data']
    print(f'\033[1;32;40m{text}')


@socketio.on("message_test")
def print_mes(data):
    emit('receivingMessage', {'msg': data['data']}, broadcast=True)


@socketio.on('newUser')
def newUser(data):
    emit('receivingUser', {'user': data['data']}, broadcast=True)