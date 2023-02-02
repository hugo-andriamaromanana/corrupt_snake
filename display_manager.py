import pygame
from pygame.locals import *
from colors import *
from fonts import *

#------------pygame----------------
DISPLAYSURF = pygame.display.set_mode((960, 660))

#------------constants----------------
AUTHORIZED_LETTERS='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
KEYS = [K_UP, K_DOWN, K_LEFT, K_RIGHT, K_RETURN, K_ESCAPE, K_BACKSPACE, K_TAB, K_SPACE,K_LSHIFT,K_LCTRL,K_RSHIFT,K_RCTRL,K_CAPSLOCK,K_LALT,K_RALT,K_LMETA,K_RMETA,K_LSUPER,K_RSUPER,K_MODE,K_HELP,K_PRINT,K_SYSREQ,K_BREAK,K_MENU,K_POWER,K_EURO]

#------------index/pointer___init___----------------
level_selection_pointer=0
login_selection_pointer=-1
menu_selection_pointer=-1
are_you_sure_pointer=0

#------------functions----------------
limit_number = lambda n: max(min(n, 2), 0)
limit_number_for_2 = lambda n: max(min(n, 1), 0)

#Dislay Manager
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
    DISPLAYSURF.fill(BLACK)
    DISPLAYSURF.blit(COMIC_SANS_BIG.render('Welcome to Snake', False, WHITE),(250,100))
    DISPLAYSURF.blit(COMIC_SANS.render('Please login !', False, WHITE),(250,250))
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
    quit_popup=pygame.Surface((800,400))
    quit_popup.fill(GREY)
    DISPLAYSURF.blit(quit_popup,(50,100))
    are_you_sure_pointer = limit_number_for_2(are_you_sure_pointer)
    DISPLAYSURF.blit(COMIC_SANS_BIG.render('Are you sure you want to quit?', False, WHITE),(100,150))
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

def display_scoreboard(scoreboard):
    scoreboard_surface = pygame.Surface((800, 400))
    scoreboard_surface.fill(GREY)
    DISPLAYSURF.blit(scoreboard_surface, (50, 100))
    DISPLAYSURF.blit(COMIC_SANS_BIG.render('Scoreboard', False, BLUE), (300, 100))
    DISPLAYSURF.blit(COMIC_SANS_SMOL.render('Press SPACE to return', False, WHITE), (100, 550))
    level_colors = {'Easy': GREEN, 'Medium': ORANGE, 'Hard': RED}
    x=150
    y=175
    for level, scores in scoreboard.items():
        DISPLAYSURF.blit(COMIC_SANS.render(level, False, level_colors[level]), (x, y))
        y+=50
        for name, score in scores:
            DISPLAYSURF.blit(COMIC_SANS.render(f"{name}-{score}", False, WHITE), (x, y))
            y+=50
        x+=200
        y=175
    pygame.display.update()

def display_wrong_password(wrong_password):
    if wrong_password:
        DISPLAYSURF.blit(COMIC_SANS_BIG.render('Wrong Password', False, RED), (500, 500))
        pygame.display.update()
        pygame.time.wait(1000)
        DISPLAYSURF.blit(COMIC_SANS_BIG.render('Wrong Password', False, BLACK), (500, 500))
        pygame.display.update()

def display_history(history):
    history_surface = pygame.Surface((800, 400))
    history_surface.fill(GREY)
    DISPLAYSURF.blit(history_surface, (50, 100))
    DISPLAYSURF.blit(COMIC_SANS_BIG.render('Game History', False, BLUE), (300, 100))
    DISPLAYSURF.blit(COMIC_SANS_SMOL.render('Press SPACE to return', False, WHITE), (100, 550))
    level_colors = {'Easy': GREEN, 'Medium': ORANGE, 'Hard': RED}
    x=150
    y=175
    for level, scores in history.items():
        DISPLAYSURF.blit(COMIC_SANS.render(level, False, level_colors[level]), (x, y))
        y+=50
        for score in scores:
            DISPLAYSURF.blit(COMIC_SANS.render(str(score), False, WHITE), (x, y))
            y+=50
        x+=200
        y=175
    pygame.display.update()

