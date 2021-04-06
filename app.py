import os
import tictactoe
from flask import (
    Flask, flash, render_template, 
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


@app.route("/")
@app.route("/get_leaderboard")
def get_contenders():
    contenders = mongo.db.contenders.find()
    return render_template("leaderboard.html", contenders=contenders)


player_turn = "player1"
player1coordinates = []
player2coordinates = []
dimensions = 4
width = 4


@app.route("/")
@app.route("/play", methods=["GET", "POST"])
def play():
    global player_turn, dimensions, width
    global player1coordinates, player2coordinates
    result = ""
    new_coordinates = ""
    if request.method == "POST":
        if result != "":
            width = request.form.get('width')
            dimensions = request.form.get('dimensions')
        if player_turn == "player1":
            new_coordinates = list(map(int, request.form.get(
                    'coordinate').split(',')))
            if tictactoe.GameResult(
                player1coordinates,
                new_coordinates,
                player_turn,
                dimensions,
                width):
                result = "Victory for Player 1!"
                player1coordinates = []
                player2coordinates = []
            else:
                player1coordinates.append(new_coordinates)
            print("Player1: ", player1coordinates)
            player_turn = "player2"
        else:
            new_coordinates = list(map(int, request.form.get(
                    'coordinate').split(',')))
            if tictactoe.GameResult(
                player2coordinates,
                new_coordinates,
                player_turn,
                dimensions,
                width):
                result = "Victory for Player 2!"
                player1coordinates = []
                player2coordinates = []
            else:
                player2coordinates.append(new_coordinates)
            print("Player2: ", player2coordinates)
            player_turn = "player1"

    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]

    if session["user"]:
        return render_template("play.html",
                                result=result,
                                width=width,
                                player1coordinates=player1coordinates,
                                player2coordinates=player2coordinates,
                                player_turn=player_turn)
    else:
        return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # check if username already exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            flash("Username already exists")
            return redirect(url_for("register"))

        register = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password"))
        }
        mongo.db.users.insert_one(register)

        # put the new user into 'session' cookie
        session["user"] = request.form.get("username").lower()
        flash("Registration Successful!")
        return redirect(url_for(
            "play", username=session["user"]))
    return render_template("register.html")


@app.route("/sign_in", methods=["GET", "POST"])
def sign_in():
    if request.method == "POST":
        # check if username exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            # ensure hashed password matches user input
            if check_password_hash(
                existing_user["password"], request.form.get("password")):
                    session["user"] = request.form.get("username").lower()
                    flash("Welcome, {}".format(
                        request.form.get("username")))
                    return redirect(url_for(
                        "play", username=session["user"]))
            else:
                # invalid password match
                flash("Incorrect Username and/or Password")
                return redirect(url_for("sign_in"))

        else:
            # username doesn't exist
            flash("Incorrect Username and/or Password")
            return redirect(url_for("sign_in"))

    return render_template("signin.html")


@app.route("/sign_out")
def sign_out():
    # remove user from session cookie
    flash("You have signed out")
    session.pop("user")
    return redirect(url_for("sign_in"))


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
