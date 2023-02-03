import json
import hashlib
TRANSLATE_POINTER = {
    0: 'Easy',
    1: 'Medium',
    2: 'Hard'
}
def adjust_settings(dic,TRANSLATE_POINTER):
    empty_dic = {}
    for i, level in enumerate(TRANSLATE_POINTER.values()):
        empty_dic[i] = dic[level]
    return empty_dic
#------------Json----------------
with open('json/users.json') as f:
    users = json.load(f)
with open('json/history.json') as f:
    history = json.load(f)
with open('json/settings.json') as f:
    LEVEL_SETTINGS = adjust_settings(json.load(f),TRANSLATE_POINTER)
#-----------Json dump----------
def users_dumper(data):
    with open('json/users.json', 'w') as f:
        json.dump(data, f,indent=4)
def history_dumper(data):
    with open('json/history.json', 'w') as f:
        json.dump(data, f,indent=4)
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