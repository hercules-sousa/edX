import os

import requests
from flask import Flask, session, render_template, request, jsonify
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
        return render_template("signing_up.html", text="Signing up page", login_fail=True)

    account_db = db.execute("SELECT * FROM accounts WHERE username=:username",
                            {"username": user_page}).fetchone()
    if account_db is None:
        db.execute("INSERT INTO accounts (username, password) VALUES (:user, :pass);",
                   {"user": user_page, "pass": password_page})
        db.commit()
        return render_template("signing_up.html", text="Signing up page", login_success=True)
    return render_template("signing_up.html", text="Signing up page", login_fail=True)


def looking_into_db(s):
    a = db.execute(f"SELECT * FROM books WHERE isbn LIKE '%{s}%';").fetchall()
    b = db.execute(f"SELECT * FROM books WHERE title LIKE '%{s}%';").fetchall()
    c = db.execute(f"SELECT * FROM books WHERE author LIKE '%{s}%';").fetchall()
    if s.isdigit():
        d = db.execute(f"SELECT * FROM books WHERE CAST(year AS VARCHAR) LIKE '%{s}%'").fetchall()
        return a + b + c + d
    else:
        return a + b + c


def looking_into_db_by_id(id):
    return db.execute(f"SELECT * FROM books WHERE id={id};").fetchall()


@app.route("/searching", methods=["POST"])
def searching():
    s = request.form.get("searched")
    book = looking_into_db(s)
    if not book:
        return "No such book", 404
    return render_template("results.html", searched=book, part_searched=s)


@app.route("/book_search/<int:id>", methods=["GET"])
def book_search(id):
    book = looking_into_db_by_id(id)
    isbn = book[0][0]
    print(f"ISBN = {isbn}")
    res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"KEY": "KEj26vrr38gcJPa6sF4vouwY", "isbns": isbn})
    if res.status_code != 200:
        raise Exception("Error: No such book")
    return render_template("books.html", data_in_db=book, request=res.json())


@app.route("/sending_review", methods=["POST"])
def sending_review():
    review_rating = request.form.get("review_rating")
    if not review_rating.isdigit():
        print(f"Review sent = {review_rating}")
        return render_template("error.html")
    review_rating = int(review_rating)
    if not 1 <= review_rating <= 5:
        print(f"Review sent = {review_rating}")
        return render_template("error.html", message="Invalid number")
    review_comment = request.form["review_comment"]
    print(f"{review_comment}")
    user = session["username"]
    user_in_db = db.execute("SELECT * FROM reviews WHERE username=:user;", {"user": user}).fetchone()
    if user_in_db is None:
        db.execute("INSERT INTO reviews(username, commentary) VALUES (:username, :review_comment);", {"username": user, "review_comment": review_comment})
        db.commit()
        return render_template("error.html", message="Tudo certo")
    else:
        return render_template("error.html", message="Usuário já comentou")


@app.route("/logging_out", methods=["GET"])
def logging_out():
    session["username"] = None
    return render_template("login.html", text="Login Page")
