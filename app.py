import os
import random
import tictactoe
from datetime import datetime
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
@app.route("/discussion", methods=["GET", "POST"])
def discussion():
    if request.method == "POST":
        new_comment = {
            "name": session["user"],
            "message": request.form.get("message"),
            "date": datetime.now().strftime("%d-%m-%Y")
        }
        mongo.db.comments.insert_one(new_comment)
    contenders = mongo.db.users.find().sort('score', -1)
    comments = mongo.db.comments.find().sort('date', -1)
    return render_template("discussion.html",
                           contenders=contenders,
                           comments=comments)


player_turn = "player1"
opponent = "player2"
player1coordinates = []
player2coordinates = []
partial_runsP1 = []
partial_runsP2 = []
spent_runs = []
dimensions = 4
width = 4
result = "Set Board"


@app.route("/play", methods=["GET", "POST"])
def play():
    global player_turn, dimensions, width, opponent
    global player1coordinates, player2coordinates
    global partial_runsP1, partial_runsP2, spent_runs
    global result
    print(result)
    new_coordinates = ""
    comp_coordinate = ""
    if request.method == "POST":
        if result != "":
            width = int(request.form.get('width'))
            dimensions = int(request.form.get('dimensions'))
            opponent = request.form.get('opponent')
            print(opponent)
            result = ""
        elif player_turn == "player1":
            new_coordinates = list(map(int, request.form.get(
                'coordinate').split(',')))
            # print("player1 success")
            if tictactoe.GameResult(
                    player1coordinates,
                    new_coordinates,
                    player_turn,
                    dimensions,
                    width,
                    partial_runsP1) == player_turn:
                result = f'{session["user"]} wins!!'
                player1coordinates = []
                player2coordinates = []
                partial_runsP1 = []
                partial_runsP2 = []
                spent_runs = []
                player_file = mongo.db.users.find_one(
                    {"username": session["user"]})
                player_score = player_file['score']
                new_score = ((width**dimensions) + player_score)
                player_update = {
                    "score": new_score
                }
                mongo.db.users.update_one(player_file, {"$set": player_update})
                print(player_file)
                print(player_score, "type of: ", type(player_score))
            elif opponent == "computer":
                player1coordinates.append(new_coordinates)
                comp_coordinate = tictactoe.CompPlay(partial_runsP1,
                                                     spent_runs,
                                                     player1coordinates,
                                                     player2coordinates,
                                                     width,
                                                     dimensions)
                # print("computer play success")
                if tictactoe.GameResult(
                        player2coordinates,
                        comp_coordinate,
                        "Computer",
                        dimensions,
                        width,
                        partial_runsP2) == "Computer":
                    result = "c0mPuTer WiN!"
                    player1coordinates = []
                    player2coordinates = []
                    partial_runsP1 = []
                    partial_runsP2 = []
                    spent_runs = []
                else:
                    player2coordinates.append(comp_coordinate)
                    print("Computer's: ", player2coordinates)
            else:
                player1coordinates.append(new_coordinates)
                player_turn = "player2"
            print("Player1's: ", player1coordinates)
        elif player_turn == "player2":
            print("please no")
            new_coordinates = list(map(int, request.form.get(
                'coordinate').split(',')))
            if tictactoe.GameResult(
                    player2coordinates,
                    new_coordinates,
                    player_turn,
                    dimensions,
                    width,
                    partial_runsP2) == player_turn:
                result = "The Guest wins!!"
                player1coordinates = []
                player2coordinates = []
                partial_runsP1 = []
                partial_runsP2 = []
            else:
                player2coordinates.append(new_coordinates)
                print("Player2's: ", player2coordinates)
                player_turn = "player1"
    username = session["user"]
    if session["user"]:
        return render_template("play.html",
                               username=username,
                               result=result,
                               width=width,
                               dimensions=dimensions,
                               player1coordinates=player1coordinates,
                               player2coordinates=player2coordinates,
                               player_turn=player_turn)
    else:
        return redirect(url_for("login"))


@app.route("/reset_board")
def reset_board():
    global player1coordinates, player2coordinates, player_turn
    global partial_runsP1, partial_runsP2, spent_runs
    player_turn = "player1"
    player1coordinates, player2coordinates = [], []
    partial_runsP1, partial_runsP2, spent_runs = [], [], []
    return redirect(url_for("play"))


@app.route("/set_new_board")
def set_new_board():
    global player1coordinates, player2coordinates, player_turn
    global partial_runsP1, partial_runsP2, spent_runs, result
    result = "Set Board"
    print(result)
    player_turn = "player1"
    player1coordinates, player2coordinates = [], []
    partial_runsP1, partial_runsP2, spent_runs = [], [], []
    return redirect(url_for("play", result=result))


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
            "password": generate_password_hash(request.form.get("password")),
            "score": 0
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


@app.route("/edit_comment/<comment_id>/<comment_date>",
            methods=["GET", "POST"])
def edit_comment(comment_id, comment_date):
    if request.method == "POST":
        edited = {
            "name": session["user"],
            "message": request.form.get("edited_message"),
            "date": comment_date
        }
        mongo.db.comments.update({"_id": ObjectId(comment_id)}, edited)
        flash("Comment Successfully Edited")

    return redirect(url_for("discussion"))


@app.route("/delete_comment/<comment_id>")
def delete_comment(comment_id):
    mongo.db.comments.remove({"_id": ObjectId(comment_id)})
    flash("Comment Successfully Deleted")
    return redirect(url_for("discussion"))


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
