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
    return render_template("login.html", message=False, text="Login page")


@app.route("/trying_logging", methods=["POST"])
def trying_logging():
    user_page = request.form.get("user")
    password_page = request.form.get("password")
    account_db = db.execute("SELECT * FROM accounts WHERE username=:username AND password=:password",
                            {"username": user_page, "password": password_page}).fetchone()

    if account_db is None:
        return render_template("login.html", message=True, text="Login page")

    session["username"] = user_page
    return render_template("search.html", user=session["username"])


@app.route("/signing_up", methods=["GET"])
def signing_up():
    return render_template("signing_up.html", text="Signing up page")


@app.route("/signing_up_into_db", methods=["POST"])
def signing_up_into_db():
    user_page = request.form.get("user")
    password_page = request.form.get("password")

    if user_page == "" or password_page == "":
        return render_template("signing_up.html", login_fail=True)

    account_db = db.execute("SELECT * FROM accounts WHERE username=:username",
                            {"username": user_page}).fetchone()
    if account_db is None:
        db.execute("INSERT INTO accounts (username, password) VALUES (:user, :pass);", {"user": user_page, "pass": password_page})
        db.commit()
        return render_template("signing_up.html", login_success=True)
    return render_template("signing_up.html", login_fail=True)


@app.route("/searching", methods=["POST"])
def searching():
    s = request.form.get("searched")
    a = db.execute(f"SELECT * FROM books WHERE isbn LIKE '%{s}%';").fetchall()
    b = db.execute(f"SELECT * FROM books WHERE title LIKE '%{s}%';").fetchall()
    c = db.execute(f"SELECT * FROM books WHERE author LIKE '%{s}%';").fetchall()
    if s.isdigit():
        d = db.execute(f"SELECT * FROM books WHERE CAST(year AS VARCHAR) LIKE '%{s}%'").fetchall()
        results = a + b + c + d
    else:
        results = a + b + c
    return render_template("results.html", searched=results)
