#cmd
#py -m pip install flask
# in the current directory
#py -m flask run
from flask import Flask, flash, request, redirect, url_for, render_template, g, make_response, session
from markupsafe import escape
from uuid import uuid4
#pip install jsonpickle

app = Flask(__name__)
app.secret_key = '728fc787f7914b9684f4a7cefa7405c0'

# печать в консоль
def log(text):
    app.logger.info(text)

registered_users = {}
users_data = {} #data of loged in users
#redirect(url_for('index'))

def init():
    with open("users.csv") as f:
        f.readline()
        for line in f:
            line = line.strip(" \t\n")
            if line != "":
                t = line.split(",")
                registered_users[t[0]] = t[1]

def add_user(nick, password):
    registered_users[nick] = password
    with open("users.csv","a") as f:
        f.write(nick+" "+password+"\n")

def success(**kwargs):
    kwargs["success"] = True
    return kwargs

def fail(msg="error", code = 400):
    return {"success":False, "message":msg}, code

def valid_token(token):
    return ("token" in session) and (session["token"] == token)

# respond error
# endpoint
# repository

def is_logged_id():
    return "nickname" in session

def init_session(nick):
    session["nickname"] = nick
    session["games"] = []
    session["current_game"] = -1


def use_post_method():
    return "Http POST method required"

@app.route("/")
def hello_world():
    return "<h1>Game set</h1>"

@app.route("/user/token")
def get_token():
    if not is_logged_id():
        return fail("You need to log in", 401)
    token = uuid4().hex
    session["token"] = token
    return success(nickname=session["nickname"], accessToken=token)

#r = flask.Response()
#r.setcookie(...)
#return r

@app.post("/user/register")
def register_post():
    if is_logged_id():
        return fail("You are logged in")
    try:
        data = request.get_json()
        nick = data["nickname"]
        if nick in registered_users:
            return fail("User alerady exist")
        else:
            add_user(nick, data["password"])
            init_session(nick)
            return get_token()
    except:
        log(data)
        return fail()

@app.post("/user/login")
def login_post():
    if is_logged_id():
        return fail("You are logged in")
    try:
        data = request.get_json()
        nick = data["nickname"]
        if nick not in registered_users:
            log(registered_users)
            return fail(f"The nickname '{nick}' is not registered")
        elif registered_users[nick] != data["password"]:
            return fail("Wrong password")
        else:
            init_session(nick)
            return get_token()
    except:
        log(data)
        return fail()

# @app.get("/user/login")
# def login_get():
#     return "<form>Здесь должна быть форма</form>"

@app.route("/user/logout", methods=['GET', 'POST'])
def logout():
    session.clear()
    return success()

@app.post("/set/room/create")
def create_game():
    if not is_logged_id():
        return fail("You need to log in", 401)
    try:
        data = request.get_json()
        token = data["accessToken"]
        if not valid_token(token):
            return fail("Invalid access token")
        id = 0
        if len(session["games"]) == 0:
            session["games"] = [{"id":0}]
        else:
            #todo global games var, "cards", score
            games = session["games"]
            id = games[-1]["id"]+1
            games.append({"id":id})
            session["games"] = games
        return success(gameId=id)
    except:
        return fail()

@app.post("/set/room/list")
def get_games():
    if not is_logged_id():
        return fail("You need to log in")
    try:
        data = request.get_json()
        token = data["accessToken"]
        if not valid_token(token):
            return fail("Invalid access token")
        arr = []
        for game in session["games"]:
            arr.append({"id":game["id"]})
        return success(games=arr)
    except:
        return fail()

@app.post("/set/room/list/enter")
def enter_game():
    if not is_logged_id():
        return fail("You need to log in")
    try:
        data = request.get_json()
        token = data["accessToken"]
        if not valid_token(token):
            return fail("Invalid access token")
        game_id = data["gameId"]
        for game in session["games"]:
            if game["id"] == game_id:
                session["current_game"] = game_id
                return success(gameId=game_id)
        return fail("Wrong game id")
    except:
        return fail()


if __name__ == "__main__":
    init()
    app.run(host="0.0.0.0",debug=True)