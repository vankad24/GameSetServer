from flask import Flask, flash, request, redirect, url_for, render_template, g, make_response, session
from markupsafe import escape
from data.UserDataSource import UserDataSource
from dto.request.GameRequest import GameRequest
from dto.request.PickRequest import PickRequest
from dto.request.RegisterRequest import RegisterRequest
from dto.response.BaseResponse import BaseResponse
from dto.response.GameFieldResponse import GameFieldResponse
from dto.response.GameResponse import GameResponse
from dto.response.ErrorResponse import ErrorResponse
from dto.response.ListOfGamesResponse import ListOfGamesResponse
from dto.response.PickResponse import PickResponse
from dto.response.TokenResponse import TokenResponse
from repository.ApiException import ApiException
from repository.GameRepository import GameRepository
from repository.UserRepository import UserRepository

app = Flask(__name__)
app.secret_key = '728fc787f7914b9684f4a7cefa7405c0'

# печать в консоль
def log(text):
    app.logger.info(text)

#redirect(url_for('index'))
#r = flask.Response()
#r.setcookie(...)
#return r

source = UserDataSource()
userRep = UserRepository(source)
gameRep = GameRepository(source)

def respond(response: BaseResponse):
    return response.to_dict()

@app.route("/")
def hello_world():
    return userRep.main()

@app.post("/user/register")
def register():
    # received request
    req = RegisterRequest.from_request()
    try:
        user = userRep.register(req.nick, req.password)
        return respond(TokenResponse(user.token, user.nickname))
    except ApiException as e:
        return respond(ErrorResponse(e.msg))

@app.post("/user/login")
def login():
    # received request
    req = RegisterRequest.from_request()
    try:
        user = userRep.login(req.nick, req.password)
        return respond(TokenResponse(user.token, user.nickname))
    except ApiException as e:
        return respond(ErrorResponse(e.msg))

@app.post("/user/logout")
def logout():
    try:
        userRep.logout()
        return respond(BaseResponse())
    except ApiException as e:
        return respond(ErrorResponse(e.msg))

@app.post("/set/room/create")
def create_game():
    req = GameRequest.from_request()
    try:
        game_id = gameRep.create(req.token)
        return respond(GameResponse(game_id))
    except ApiException as e:
        return respond(ErrorResponse(e.msg))

@app.post("/set/room/list")
def get_games():
    req = GameRequest.from_request()
    try:
        ids = gameRep.get_games_ids(req.token)
        return respond(ListOfGamesResponse(ids))
    except ApiException as e:
        return respond(ErrorResponse(e.msg))

@app.post("/set/room/enter")
def enter_game():
    req = GameRequest.from_request()
    try:
        gameRep.join_game(req.token,req.game_id)
        return respond(GameResponse(req.game_id))
    except ApiException as e:
        return respond(ErrorResponse(e.msg))

@app.post("/set/room/leave")
def leave_game():
    req = GameRequest.from_request()
    try:
        game_id = gameRep.leave_game(req.token)
        return respond(GameResponse(game_id))
    except ApiException as e:
        return respond(ErrorResponse(e.msg))

@app.post("/set/field")
def get_field():
    req = GameRequest.from_request()
    try:
        game = gameRep.get_current_game(req.token)
        uid = UserRepository.get_user_id()
        score = game.get_score_by_id(uid)
        return respond(GameFieldResponse(game.field,score))
    except ApiException as e:
        return respond(ErrorResponse(e.msg))

@app.post("/set/pick")
def pick():
    req = PickRequest.from_request()
    try:
        is_set, score = gameRep.pick_cards(req.token, req.cards_ids)
        return respond(PickResponse(is_set, score))
    except ApiException as e:
        return respond(ErrorResponse(e.msg))

@app.post("/set/get")
def get_three_cards():
    ...

if __name__ == "__main__":
    app.run(host="0.0.0.0",debug=True)