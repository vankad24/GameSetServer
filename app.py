from flask import Flask, flash, request, redirect, url_for, render_template, g, make_response, session
from data.UserDataSource import UserDataSource
from dto.request.BaseRequest import BaseRequest
from dto.request.GameRequest import GameRequest
from dto.request.PickRequest import PickRequest
from dto.request.RegisterRequest import RegisterRequest
from dto.response.BaseResponse import BaseResponse
from dto.response.FindSetResponse import FindSetResponse
from dto.response.GameFieldResponse import GameFieldResponse
from dto.response.GameRoomResponse import GameRoomResponse
from dto.response.ErrorResponse import ErrorResponse
from dto.response.GameStatisticsResponse import CreateGameStatisticsResponse
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

userRep = UserRepository(UserDataSource())
gameRep = GameRepository()

def respond(response: BaseResponse):
    return response.to_dict()

@app.post("/")
def hello():
    req = BaseRequest.from_request()
    try:
        user = userRep.get_user_by_token(req.token)
        name = user.nickname
    except ApiException as e:
        name = "unknown user"
    return f"<h1>Hello, {name}!</h1>"

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
    req = RegisterRequest.from_request()
    try:
        user = userRep.login(req.nick, req.password)
        return respond(TokenResponse(user.token, user.nickname))
    except ApiException as e:
        return respond(ErrorResponse(e.msg))

@app.post("/set/room/create")
def create_game():
    req = GameRequest.from_request()
    try:
        user = userRep.get_user_by_token(req.token)
        game = gameRep.create_game(user.id)
        return respond(GameRoomResponse(game))
    except ApiException as e:
        return respond(ErrorResponse(e.msg))

@app.post("/set/room/enter")
def enter_game():
    req = GameRequest.from_request()
    try:
        uid = userRep.get_user_by_token(req.token).id
        game = gameRep.join_game(uid,req.game_id)
        return respond(GameRoomResponse(game))
    except ApiException as e:
        return respond(ErrorResponse(e.msg))

@app.post("/set/room/list")
def get_games():
    req = GameRequest.from_request()
    try:
        userRep.get_user_by_token(req.token)
        games = gameRep.get_games()
        return respond(ListOfGamesResponse(games))
    except ApiException as e:
        return respond(ErrorResponse(e.msg))

@app.post("/set/room/leave")
def leave_game():
    req = GameRequest.from_request()
    try:
        uid = userRep.get_user_by_token(req.token).id
        gameRep.leave_game(uid)
        return respond(BaseResponse())
    except ApiException as e:
        return respond(ErrorResponse(e.msg))

@app.post("/set/field")
def get_field():
    req = GameRequest.from_request()
    try:
        uid = userRep.get_user_by_token(req.token).id
        game = gameRep.get_game_by_uid(uid)
        score = game.get_score_by_id(uid)
        return respond(GameFieldResponse(score, game))
    except ApiException as e:
        return respond(ErrorResponse(e.msg))

@app.post("/set/pick")
def pick():
    req = PickRequest.from_request()
    try:
        uid = userRep.get_user_by_token(req.token).id
        is_set, game = gameRep.pick_cards(uid, req.cards_ids)
        score = game.get_score_by_id(uid)
        return respond(PickResponse(is_set, score, game))
    except ApiException as e:
        return respond(ErrorResponse(e.msg))

@app.post("/set/add")
def get_three_cards():
    req = GameRequest.from_request()
    try:
        uid = userRep.get_user_by_token(req.token).id
        gameRep.add_three_cards(uid)
        return get_field()
    except ApiException as e:
        return respond(ErrorResponse(e.msg))

@app.post("/set/stats")
def get_statistics():
    req = GameRequest.from_request()
    try:
        uid = userRep.get_user_by_token(req.token).id
        game = gameRep.get_game_by_uid(uid)
        score = game.get_score_by_id(uid)
        return respond(CreateGameStatisticsResponse(score, game))
    except ApiException as e:
        return respond(ErrorResponse(e.msg))

@app.post("/set/find")
def find_set():
    req = GameRequest.from_request()
    try:
        uid = userRep.get_user_by_token(req.token).id
        ids, game = gameRep.find_set(uid)
        score = game.get_score_by_id(uid)
        return respond(FindSetResponse(ids, score, game))
    except ApiException as e:
        return respond(ErrorResponse(e.msg))

if __name__ == "__main__":
    app.run(host="0.0.0.0",debug=True)