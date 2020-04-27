import os

from flask import Flask, session, render_template, request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    return render_template("login.html", message = False, text = "Login page")


@app.route("/trying_logging", methods=["POST"])
def trying_logging():
    user_page = request.form.get("user")
    password_page = request.form.get("password")
    account_db = db.execute("SELECT * FROM accounts WHERE username=:username AND password=:password", {"username": user_page, "password": password_page}).fetchone()

    if account_db is None:
        return render_template("login.html", message = True, text = "Login page")

    return render_template("hello.html", message="success")


@app.route("/signing_up", methods=["GET"])
def signing_up():
    return render_template("signing_up.html", text = "Signing up page")
