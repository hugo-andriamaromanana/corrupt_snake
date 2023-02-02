import json
import hashlib
import pygame
from pygame.locals import *

#------------colors----------------
BLACK=(0,0,0)
WHITE=(255,255,255)
RED=(255,0,0)
GREEN=(0,255,0)
BLUE=(0,0,255)
YELLOW=(255,255,0)
ORANGE=(255,165,0)
PURPLE=(128,0,128)
PINK=(255,192,203)
LIGHT_BLUE=(173,216,230)
CLEAR_BLUE=(0,191,255)
GREY=(128,128,128)

#------------pygame----------------
pygame.init()
pygame.font.init()

#------------font----------------
COMIC_SANS_SMOL = pygame.font.SysFont('Comic Sans MS', 20)
COMIC_SANS = pygame.font.SysFont('Comic Sans MS', 30)
COMIC_SANS_BIG = pygame.font.SysFont('Comic Sans MS', 50)

#------------constants----------------
AUTHORIZED_LETTERS='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
KEYS = [K_UP, K_DOWN, K_LEFT, K_RIGHT, K_RETURN, K_ESCAPE, K_BACKSPACE, K_TAB, K_SPACE,K_LSHIFT,K_LCTRL,K_RSHIFT,K_RCTRL,K_CAPSLOCK,K_LALT,K_RALT,K_LMETA,K_RMETA,K_LSUPER,K_RSUPER,K_MODE,K_HELP,K_PRINT,K_SYSREQ,K_BREAK,K_MENU,K_POWER,K_EURO]
TRANSLATE_POINTER = {
    2: 'Hard',
    1: 'Medium',
    0: 'Easy'
}

#------------json----------------
with open("scoreboard.json","r") as f:
    scoreboard = json.load(f)
with open("users.json","r") as f:
    users = json.load(f)
with open("history.json","r") as f:
    history = json.load(f)

#------------pygame----------------
DISPLAYSURF = pygame.display.set_mode((960, 660))

#------------functions for Json----------------
def hash_pass(password):
    return hashlib.sha256(password.encode()).hexdigest()

def initialize_new_user_history(username,history):
    history[username]={}
    for i in range(3):
        history[username][TRANSLATE_POINTER[i]]=[]
    with open("history.json","w") as f:
        json.dump(history,f,indent=4)

def user_check(username):
    if username in users:
            return True
    return False

def TRUE_login(username,password):
    if users[username]==hash_pass(password):
        return True
    return False

#-------------json dumpers----------------
def users_dumper(users):
    with open('users.json', 'w') as f:
        json.dump(users, f, indent=4)

def scoreboard_dumper(scoreboard):
    with open('scoreboard.json', 'w') as f:
        json.dump(scoreboard, f, indent=4)

def history_dumper(history):
    with open('history.json', 'w') as f:
        json.dump(history, f, indent=4)

#------------swappers----------------
def menu_swap(menu_selection_pointer):
    menu_options = [("PLAY", GREEN), ("Scoreboard", YELLOW), ("Game History", PINK)]
    passive_color = WHITE
    arrow = "-> "
    for i, (text, color) in enumerate(menu_options):
        if i == menu_selection_pointer:
            text = arrow + text
            blit_color = color
        else:
            blit_color = passive_color
        DISPLAYSURF.blit(COMIC_SANS_BIG.render(text, False, blit_color), (350, 200 + 100*i))

def level_swap(level_selection_pointer):
    level_options=[("Easy", GREEN), ("Medium", YELLOW), ("Hard", RED)]
    passive_color=WHITE
    arrow='-> '
    for i, (text, color) in enumerate(level_options):
        if i == level_selection_pointer:
            text=arrow+text
            blit_color=color
        else:
            blit_color=passive_color
        DISPLAYSURF.blit(COMIC_SANS.render(text, False, blit_color), (400, 250 + 50*i))

def login_swap(login_selection_pointer):
    login_options=[('Username:',GREEN),( 'Password:',YELLOW),('Login',PINK)]
    passive_color=WHITE
    arrow='-> '
    for i, (text, color) in enumerate(login_options):
        if i == login_selection_pointer:
            text=arrow+text
            blit_color=color
        else:
            blit_color=passive_color
        DISPLAYSURF.blit(COMIC_SANS.render(text, False, blit_color), (250, 300 + 50*i))

def are_you_sure_swap(are_you_sure_pointer):
    are_you_sure_options=[("Yes", RED), ("No", GREEN)]
    passive_color=WHITE
    arrow='-> '
    for i, (text, color) in enumerate(are_you_sure_options):
        if i == are_you_sure_pointer:
            text = arrow + text
            blit_color = color
        else:
            blit_color = passive_color
        DISPLAYSURF.blit(COMIC_SANS_BIG.render(text, False, blit_color), (350, 250 + 100*i))

#------------display functions----------------

def display_username(username_display):
    DISPLAYSURF.blit(COMIC_SANS.render(' '.join(username_display), False, WHITE),(450,300))

def display_password(password_display):
    DISPLAYSURF.blit(COMIC_SANS.render(' '.join(password_display), False, WHITE),(450,350))