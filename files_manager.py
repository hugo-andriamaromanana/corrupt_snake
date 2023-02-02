import json
import hashlib

TRANSLATE_POINTER = {
    2: 'Hard',
    1: 'Medium',
    0: 'Easy'
}

#------------json----------------
with open("users.json","r") as f:
    users = json.load(f)
with open("history.json","r") as f:
    history = json.load(f)
            
#-------------json dumpers----------------
def users_dumper(users):
    with open('users.json', 'w') as f:
        json.dump(users, f, indent=4)

def history_dumper(history):
    with open('history.json', 'w') as f:
        json.dump(history, f, indent=4)

#------------functions for Json----------------
def hash_pass(password):
    return hashlib.sha256(password.encode()).hexdigest()

def initialize_new_user_history(username,history):
    history[username]={}
    for i in range(3):
        history[username][TRANSLATE_POINTER[i]]=[]
    history_dumper(history)

def user_check(username):
    if username in users:
            return True
    return False

def TRUE_login(username,password):
    if users[username]==hash_pass(password):
        return True
    return False

#------------functions for scoreboard----------------

def update_scoreboard(history, scoreboard):
    for user, scores in history.items():
        for difficulty, points in scores.items():
            if difficulty not in scoreboard:
                scoreboard[difficulty] = []
            for point in points:
                scoreboard[difficulty].append([user, point])
                scoreboard[difficulty].sort(key=lambda x: x[1], reverse=True)
                scoreboard[difficulty] = scoreboard[difficulty][:5]
    return scoreboard
