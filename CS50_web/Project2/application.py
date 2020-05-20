import os, json

from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, send

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

channel = str()
begin, end = int(), int()

with open('messages.json', 'r') as m:
    messages = json.load(m)


def writingMessage(message):
    messages[channel].append(message)
    with open('messages.json', 'w') as m:
        json.dump(messages, m, indent=2)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/channels")
def channels():
    return render_template('channels.html')


@app.route("/chat/<ch>", methods=['GET', 'POST'])
def choosenChannel(ch):
    global channel
    channel = ch
    print(f'\033[1;32;40mThe channel sent was: {ch}')
    print(f'\033[1;32;40mThe channel being used is: {channel}')
    global end
    if len(messages[channel]) < 20:
        mes = messages[channel][::-1]
        return render_template("chat.html", m=mes)
    else:
        end = 20
        mes = messages[channel][begin: end]
        mes = mes[::-1]
        return render_template("chat.html", m=mes)


@socketio.on('confirmingConnection')
def confirmingMessage(data):
    text = data['data']
    print(f'\033[1;32;40m{text}')


@socketio.on("message_test")
def print_mes(data):
    writingMessage(data['data'])
    emit('receivingMessage', {'msg': data['data']}, broadcast=True)


@socketio.on('newUser')
def newUser(data):
    emit('receivingUser', {'user': data['data']}, broadcast=True)