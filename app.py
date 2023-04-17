#cmd
#py -m pip install flask
# in the current directory
#py -m flask run
from flask import Flask, flash, request, redirect, url_for, render_template, g, make_response, session
from markupsafe import escape
from data.UserDataSource import UserDataSource
from dto.request.RegisterRequest import RegisterRequest
from dto.response.BaseResponse import BaseResponse
from dto.response.ErrorResponse import ErrorResponse
from dto.response.TokenResponse import TokenResponse
from repository.UserRepository import UserRepository

#pip install jsonpickle

app = Flask(__name__)
app.secret_key = '728fc787f7914b9684f4a7cefa7405c0'

# печать в консоль
def log(text):
    app.logger.info(text)

#redirect(url_for('index'))

# respond error
# endpoint
# repository

def init_session(nick):
    session["nickname"] = nick
    session["games"] = []
    session["current_game"] = -1


@app.route("/")
def hello_world():
    return "<h1>Game set</h1>"

#r = flask.Response()
#r.setcookie(...)
#return r

userRep = UserRepository(UserDataSource())

def respond(response: BaseResponse):
    return response.to_dict()

@app.post("/user/register")
def register():
    # received request
    req = RegisterRequest.from_request()
    try:
        token = userRep.register(req.nick, req.password)
        return respond(TokenResponse(req.nick, token))
    except Exception as e:
        return respond(ErrorResponse(e.args[0]))

@app.post("/user/login")
def login():
    # received request
    req = RegisterRequest.from_request()
    try:
        token = userRep.login(req.nick,req.password)
        return respond(TokenResponse(req.nick, token))
    except Exception as e:
        return respond(ErrorResponse(e.args[0]))

@app.post("/user/logout")
def logout():
    try:
        userRep.logout()
        return respond(BaseResponse())
    except Exception as e:
        return respond(ErrorResponse(e.args[0]))

@app.post("/user/token")
def get_token():
    try:
        token = userRep.get_token()
        nick = userRep.get_nick()
        return respond(TokenResponse(nick, token))
    except Exception as e:
        return respond(ErrorResponse(e.args[0]))

# @app.post("/set/room/create")
# def create_game():
#     if not is_logged_id():
#         return fail("You need to log in", 401)
#     try:
#         data = request.get_json()
#         token = data["accessToken"]
#         if not valid_token(token):
#             return fail("Invalid access token")
#         id = 0
#         if len(session["games"]) == 0:
#             session["games"] = [{"id":0}]
#         else:
#             #todo global games var, "cards", score
#             games = session["games"]
#             id = games[-1]["id"]+1
#             games.append({"id":id})
#             session["games"] = games
#         return success(gameId=id)
#     except:
#         return fail()
#
# @app.post("/set/room/list")
# def get_games():
#     if not is_logged_id():
#         return fail("You need to log in")
#     try:
#         data = request.get_json()
#         token = data["accessToken"]
#         if not valid_token(token):
#             return fail("Invalid access token")
#         arr = []
#         for game in session["games"]:
#             arr.append({"id":game["id"]})
#         return success(games=arr)
#     except:
#         return fail()
#
# @app.post("/set/room/list/enter")
# def enter_game():
#     if not is_logged_id():
#         return fail("You need to log in")
#     try:
#         data = request.get_json()
#         token = data["accessToken"]
#         if not valid_token(token):
#             return fail("Invalid access token")
#         game_id = data["gameId"]
#         for game in session["games"]:
#             if game["id"] == game_id:
#                 session["current_game"] = game_id
#                 return success(gameId=game_id)
#         return fail("Wrong game id")
#     except:
#         return fail()


if __name__ == "__main__":
    app.run(host="0.0.0.0",debug=True)