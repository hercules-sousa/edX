import os 
from flask import Flask, render_template
from flask_socketio import SocketIO, emit, send

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

@app.route("/")
def index():
    return render_template("index.html")


@socketio.on("my event test")
def print_message(data):
    print(data)
    print("\n\n\n")


@socketio.on("event2")
def print_mes(data):
    print(data)
    print("\n\n\n")
    emit('returningMessage', {"mens": data["data"]}, broadcast=True)


@socketio.on('message')
def handleMessage(mens):
    print(mens)
