import os
import tictactoe
from datetime import datetime
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
# from flask_pymongo import PyMongo
# from bson.objectid import ObjectId
# from werkzeug.security import generate_password_hash, check_password_hash
# if os.path.exists("env.py"):
#     import env


app = Flask(__name__)

# Configuring Database
# app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
# app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
# app.secret_key = os.environ.get("SECRET_KEY")

# mongo = PyMongo(app)


# For non existant pages
@app.errorhandler(404)
def not_found(e):
    flash("""If you are looking for an extension to this website the page you
    were looking for doesn't exist. Have a look in our menu and register, if
    you haven't.""")
    return redirect(url_for("play"))


# For server errors
@app.errorhandler(500)
def not_signedin(e):
    flash("""Oops! Sorry about this. An internal server error occured. Please
     sign in or, if you are already, try the action again.""")
    return redirect(url_for("play"))


# Landing Page with Top 10 and Comments
# @app.route("/")
# @app.route("/discussion", methods=["GET", "POST"])
# def discussion():
#     # If posting to DB insert the comment posted
#     # with timestamp and other details
#     if request.method == "POST":
#         new_comment = {
#             "name": session["user"],
#             "message": request.form.get("message"),
#             "date": datetime.now().strftime("%d-%m-%Y"),
#             "timestamp": datetime.now()
#         }
#         mongo.db.comments.insert_one(new_comment)
#     # Get contenders and comments from DB for display on discussion page
#     contenders = mongo.db.users.find().sort('score', -1)[:10]
#     comments = mongo.db.comments.find().sort('timestamp', -1)
#     return render_template("discussion.html",
#                            contenders=contenders,
#                            comments=comments)


# @app.route("/leaderboard")
# def leaderboard():
#     # Get username to highlight for the user so they
#     # can see their position easily on full leaderboard
#     if session["user"]:
#         username = session["user"]
#         contenders = mongo.db.users.find().sort('score', -1)
#         return render_template("leaderboard.html",
#                                     contenders=contenders,
#                                     username=username)
#     else:
#         return redirect(url_for("sign_in"))


# Variables for game
player_turn = "player1"
opponent = "player2"
player1coordinates = []
player2coordinates = []
playerCoordinates = {}
partial_runsP1 = []
partial_runsP2 = []
spent_runs = []
dimensions = 4
width = 4
result = "Set Board"

@app.route("/")
@app.route("/play", methods=["GET", "POST"])
def play():
    # Bring variables in for use
    global player_turn, dimensions, width, opponent
    global player1coordinates, player2coordinates, playerCoordinates
    global partial_runsP1, partial_runsP2, spent_runs
    global result
    # Create a set of lists for each user if there are
    # mutliple users playing at once. A dictionary holds the lists
    # with each corresponding to the user's username.
    # username = session["user"]
    username = "You"
    state = username + "State"
    opposition = username + "Opp"
    partialp1 = username + "Partialp1"
    partialp2 = username + "Partialp2"
    depth = username + "Depth"
    dimensional = username + "Dimensions"
    spent = username + "Spent"
    new_coordinate = ""
    comp_coordinate = ""
    # Asign each list to its corresponding user-list in the dictionary
    if state in playerCoordinates:
        result = playerCoordinates[state]
    if username in playerCoordinates:
        player1coordinates = playerCoordinates[username]
        partial_runsP1 = playerCoordinates[partialp1]
        spent_runs = playerCoordinates[spent]
    else:
        player1coordinates = []
        partial_runsP1 = []
        spent_runs = []
    if opposition in playerCoordinates:
        player2coordinates = playerCoordinates[opposition]
        partial_runsP2 = playerCoordinates[partialp2]
    else:
        player2coordinates = []
        partial_runsP2 = []
    # If there is a post then begin the game checking
    if request.method == "POST":
        if result != "":
            # Get game settings
            width = int(request.form.get('width'))
            dimensions = int(request.form.get('dimensions'))
            opponent = request.form.get('opponent')
            playerCoordinates[state] = ""
            playerCoordinates[depth] = width
            playerCoordinates[dimensional] = dimensions
            result = playerCoordinates[state]
        elif player_turn == "player1":
            # Get the coordinate that is inputted by player 1 once boad is set
            new_coordinate = list(map(int, request.form.get(
                'coordinate').split(',')))
            # If the gameresult function returns a win scenraio then do things
            if tictactoe.GameResult(
                    player1coordinates,
                    new_coordinate,
                    player_turn,
                    dimensions,
                    width,
                    partial_runsP1) == player_turn:
                # Set result message for page and clear variables and lists
                result = f"""{username.upper()} win!!
                     {width**dimensions}pts"""
                playerCoordinates[username] = []
                playerCoordinates[opposition] = []
                playerCoordinates[partialp1] = []
                playerCoordinates[partialp2] = []
                playerCoordinates[spent] = []
                playerCoordinates[state] = "Set Board"
                # Get the players score and add on to it the win score
                # player_file = mongo.db.users.find_one(
                #     {"username": session["user"]})
                # player_score = player_file['score']
                # new_score = ((width**dimensions) + player_score)
                # player_update = {
                #     "score": new_score
                # }
                # mongo.db.users.update_one(player_file, {"$set": player_update})
            # When the computer is set as the opponent
            elif opponent == "computer":
                player1coordinates.append(new_coordinate)
                if username in playerCoordinates:
                    playerCoordinates[username].append(new_coordinate)
                else:
                    playerCoordinates[username] = []
                    playerCoordinates[partialp1] = []
                    playerCoordinates[spent] = []
                    playerCoordinates[username].append(new_coordinate)
                # Get the computers move from its function
                comp_coordinate = tictactoe.CompPlay(partial_runsP1,
                                                     spent_runs,
                                                     player1coordinates,
                                                     player2coordinates,
                                                     width,
                                                     dimensions)
                #  If there is a win scenario for the computer perform reset
                if tictactoe.GameResult(
                        player2coordinates,
                        comp_coordinate,
                        "Computer",
                        dimensions,
                        width,
                        partial_runsP2) == "Computer":
                    result = "c0mPuTer WiN!"
                    # Clear the variables and lists
                    playerCoordinates[username] = []
                    playerCoordinates[opposition] = []
                    playerCoordinates[partialp1] = []
                    playerCoordinates[partialp2] = []
                    playerCoordinates[spent] = []
                    playerCoordinates[state] = "Set Board"
                    player_turn = "player1"
                else:
                    # else just add the coordinate to the list
                    player2coordinates.append(comp_coordinate)
                    if opposition in playerCoordinates:
                        playerCoordinates[opposition].append(comp_coordinate)
                    else:
                        playerCoordinates[opposition] = []
                        playerCoordinates[partialp2] = []
                        playerCoordinates[spent] = []
                        playerCoordinates[opposition].append(comp_coordinate)
            else:
                # If the opponent is set to local just add the coord
                # and change turn to player 2.
                player1coordinates.append(new_coordinate)
                if username in playerCoordinates:
                    playerCoordinates[username].append(new_coordinate)
                else:
                    playerCoordinates[username] = []
                    playerCoordinates[partialp1] = []
                    playerCoordinates[spent] = []
                    playerCoordinates[username].append(new_coordinate)
                player_turn = "player2"
        elif player_turn == "player2":
            # Get the coordinate that is inputted by player 2
            new_coordinate = list(map(int, request.form.get(
                'coordinate').split(',')))
            if tictactoe.GameResult(
                    player2coordinates,
                    new_coordinate,
                    player_turn,
                    dimensions,
                    width,
                    partial_runsP2) == player_turn:
                result = "The Guest wins!!"
                # Clear the variables and lists
                playerCoordinates[username] = []
                playerCoordinates[opposition] = []
                playerCoordinates[partialp1] = []
                playerCoordinates[partialp2] = []
                playerCoordinates[spent] = []
                playerCoordinates[state] = "Set Board"
                player_turn = "player1"
            else:
                # Else add the coordinates to the list and
                # change back to player one
                player2coordinates.append(new_coordinate)
                if opposition in playerCoordinates:
                    playerCoordinates[opposition].append(new_coordinate)
                else:
                    playerCoordinates[opposition] = []
                    playerCoordinates[partialp2] = []
                    playerCoordinates[spent] = []
                    playerCoordinates[opposition].append(new_coordinate)
                player_turn = "player1"
    # Asign the width and dimensions the user values from the dictionary
    if depth in playerCoordinates:
        width = playerCoordinates[depth]
        dimensions = playerCoordinates[dimensional]
    else:
        result = "Set Board"
    # If there is a user logged-in move the variables
    # to the front end and render the page, otherwise redirect to log-in.
    # if session["user"]:
    return render_template("play.html",
                            username=username,
                            result=result,
                            width=width,
                            dimensions=dimensions,
                            player1coordinates=player1coordinates,
                            player2coordinates=player2coordinates,
                            player_turn=player_turn)
    # else:
    #     return redirect(url_for("sign_in"))


# If the user resets the board then the lists
# are cleared and they are redirected back to the play page
@app.route("/reset_board")
def reset_board():
    global player_turn, playerCoordinates
    player_turn = "player1"
    username = "You"
    opposition = username + "Opp"
    partialp1 = username + "Partialp1"
    partialp2 = username + "Partialp2"
    spent = username + "Spent"
    playerCoordinates[username] = []
    playerCoordinates[opposition] = []
    playerCoordinates[partialp1] = []
    playerCoordinates[partialp2] = []
    playerCoordinates[spent] = []
    return redirect(url_for("play"))


# If the user sets new board then the lists
# are cleared and the variables too
# and they are redirected back to the play page to set new board.
@app.route("/set_new_board")
def set_new_board():
    global player_turn, playerCoordinates
    player_turn = "player1"
    username = "You"
    state = username + "State"
    opposition = username + "Opp"
    partialp1 = username + "Partialp1"
    partialp2 = username + "Partialp2"
    spent = username + "Spent"
    playerCoordinates[username] = []
    playerCoordinates[opposition] = []
    playerCoordinates[partialp1] = []
    playerCoordinates[partialp2] = []
    playerCoordinates[spent] = []
    playerCoordinates[state] = "Set Board"
    return redirect(url_for("play", result=result))


# Register page
# @app.route("/register", methods=["GET", "POST"])
# def register():
#     if request.method == "POST":
#         # check if username already exists in db
#         existing_user = mongo.db.users.find_one(
#             {"username": request.form.get("username").lower()})
#         # If the name already exists redirect them back to try again
#         if existing_user:
#             flash("Username already exists")
#             return redirect(url_for("register"))
#         # Take the name and password they inputted and
#         # create an object for the DB
#         register = {
#             "username": request.form.get("username").lower(),
#             "password": generate_password_hash(request.form.get("password")),
#             "score": 0
#         }
#         mongo.db.users.insert_one(register)

#         # put the new user into 'session' cookie
#         session["user"] = request.form.get("username").lower()
#         flash("Registration Successful!")
#         return redirect(url_for(
#             "play", username=session["user"]))
#     return render_template("register.html")


# @app.route("/sign_in", methods=["GET", "POST"])
# def sign_in():
    # if request.method == "POST":
        # check if username exists in db
        # existing_user = mongo.db.users.find_one(
        #     {"username": request.form.get("username").lower()})

        # if existing_user:
        #     # ensure hashed password matches user input
        #     if check_password_hash(
        #             existing_user["password"], request.form.get("password")):
        #         session["user"] = request.form.get("username").lower()
        #         flash("Welcome, {}".format(
        #             request.form.get("username")))
        #         return redirect(url_for(
        #             "play", username=session["user"]))
        #     else:
        #         # invalid password match
        #         flash("Incorrect Username and/or Password")
        #         return redirect(url_for("sign_in"))

        # else:
        #     # username doesn't exist
        #     flash("Incorrect Username and/or Password")
        #     return redirect(url_for("sign_in"))

    # return render_template("signin.html")


# @app.route("/sign_out")
# def sign_out():
#     # remove user from session cookie
#     flash("You have signed out")
#     session.pop("user")
#     return redirect(url_for("sign_in"))


# Edit a comment from the modal
# @app.route("/edit_comment/<comment_id>/<comment_date>",
#             methods=["GET", "POST"])
# def edit_comment(comment_id, comment_date):
#     if request.method == "POST":
#         # Take the editted version and put in object for DB
#         edited = {
#             "name": session["user"],
#             "message": request.form.get("edited_message"),
#             "date": comment_date,
#             "timestamp": datetime.now()
#         }
#         mongo.db.comments.update({"_id": ObjectId(comment_id)}, edited)
#         flash("Comment Successfully Edited")

#     return redirect(url_for("discussion"))


# Delete comment by comment id
# @app.route("/delete_comment/<comment_id>")
# def delete_comment(comment_id):
#     mongo.db.comments.remove({"_id": ObjectId(comment_id)})
#     flash("Comment Successfully Deleted")
#     return redirect(url_for("discussion"))


if __name__ == "__main__":
    app.run(
        host=os.environ.get("IP"),
        port=int(os.environ.get("PORT")),
        debug=False)
