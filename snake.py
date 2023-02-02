import pygame
import random
from files_manager import *
from display_manager import *

#------------pygame----------------
pygame.init()
pygame.display.set_caption("snake")

#------------screen----------------
screen = pygame.display.set_mode((960, 660))
screen.fill(GREY)

#------------functions----------------
def reset_pointers():
    global level_selection_pointer
    global login_selection_pointer
    global menu_selection_pointer
    level_selection_pointer=0
    login_selection_pointer=-1
    menu_selection_pointer=-1

#------------Objects----------------
class Snake():
    def __init__(self):
        self.x = 2
        self.y = 1
        self.length = 2
        self.body =[[self.x, self.y], [self.x-1, self.y]]
        self.direction = "right"
        self.score = 0
    def move(self):
        if self.direction == "right":
            self.x += 1
        if self.direction == "left":
            self.x -= 1
        if self.direction == "up":
            self.y -= 1
        if self.direction == "down":
            self.y += 1
        self.body.insert(0, [self.x, self.y])
        if len(self.body) > self.length:
            self.body.pop()
    def eat(self):
        self.length += 1
        self.score += 1

class Food():
    def __init__(self):
        possible_food_locations = []
        for i in range(1,LEVEL_SETTINGS[level_selection_pointer]['INNER_GRID_WIDTH']+1):
            for j in range(1,LEVEL_SETTINGS[level_selection_pointer]['INNER_GRID_HEIGHT']+1):
                possible_food_locations.append([i,j])
        for i in snake.body:
            possible_food_locations.remove(i)
        self.x,self.y = random.choice(possible_food_locations)
    def new_food(self):
        possible_food_locations = []
        for i in range(1,LEVEL_SETTINGS[level_selection_pointer]['INNER_GRID_WIDTH']+1):
            for j in range(1,LEVEL_SETTINGS[level_selection_pointer]['INNER_GRID_HEIGHT']+1):
                possible_food_locations.append([i,j])
        for i in snake.body:
            possible_food_locations.remove(i)
        self.x,self.y = random.choice(possible_food_locations)

#-------------reset_game----------------
def reset_game():
    global snake
    global food
    global game_over
    snake = Snake()
    food = Food()
    game_over = False

#-------------intern display----------------
def display_welcome_message(true_false):
    if true_false:
        DISPLAYSURF.blit(COMIC_SANS.render(f'New user created! Best of luck! {username}', False, GREEN),(200,550))
    if not true_false:
        DISPLAYSURF.blit(COMIC_SANS.render(f'Welcome back {username}!', False, PURPLE),(250,500))

def display_game():
    screen.fill(GREY)
    grid = [[0 for _ in range(LEVEL_SETTINGS[level_selection_pointer]['GRID_WIDTH'])] for _ in range(LEVEL_SETTINGS[level_selection_pointer]['GRID_HEIGHT'])]
    grid = [[1]+row[1:] for row in grid]
    grid = [row[:-1]+[1] for row in grid]
    grid[0]=[1 for _ in range(LEVEL_SETTINGS[level_selection_pointer]['GRID_WIDTH'])]
    grid[-1]=[1 for _ in range(LEVEL_SETTINGS[level_selection_pointer]['GRID_WIDTH'])]
    body = snake.body
    for pos_y in range(len(grid)):
        for pos_x in range(len(grid[pos_y])):
            if grid[pos_y][pos_x]==0:
                DISPLAYSURF.fill(WHITE,((pos_x*LEVEL_SETTINGS[level_selection_pointer]['CELL_SIZE']),(pos_y*LEVEL_SETTINGS[level_selection_pointer]['CELL_SIZE']),LEVEL_SETTINGS[level_selection_pointer]['CELL_SIZE']-1,LEVEL_SETTINGS[level_selection_pointer]['CELL_SIZE']-1))
            elif grid[pos_y][pos_x]==1:
                DISPLAYSURF.fill(PINK,((pos_x*LEVEL_SETTINGS[level_selection_pointer]['CELL_SIZE']),(pos_y*LEVEL_SETTINGS[level_selection_pointer]['CELL_SIZE']),LEVEL_SETTINGS[level_selection_pointer]['CELL_SIZE']-1,LEVEL_SETTINGS[level_selection_pointer]['CELL_SIZE']-1))
    for coords in range(len(body)):
                DISPLAYSURF.fill(GREEN, ((body[coords][0]*LEVEL_SETTINGS[level_selection_pointer]['CELL_SIZE']),(body[coords][1]*LEVEL_SETTINGS[level_selection_pointer]['CELL_SIZE']),LEVEL_SETTINGS[level_selection_pointer]['CELL_SIZE']-1,LEVEL_SETTINGS[level_selection_pointer]['CELL_SIZE']-1))

#---------------main----------------
if __name__ == "__main__":
    #-------------default states----------------
    game_state='login_screen'
    new_user=False
    wrong_password=False
    game_over=False
    menu=False
    difficulty_lookup=False
    history_lookup=False
    scoreboard_lookup=False
    are_you_sure=False
    running=True
    new_high_score=False
    #------------login_screen----------------
    username_display=['_']*6
    username=''
    password_display=['_']*4
    password=''
    #------------scoreboard-----------------
    scoreboard={}
    scoreboard=update_scoreboard(history,scoreboard)
    #Initialise game objects
    snake=Snake()
    food=Food()
    while running:
        events = pygame.event.get()

#-----------------------------NEW USER: Tutorial--------------------------------------------
        if new_user:
            menu=False
            users[username]=hash_pass(password)
            users_dumper(users)
            initialize_new_user_history(username,history)
            history_dumper(history)
            display_tutorial(username)
            for event in events:
                if event.type == pygame.KEYDOWN:
                    new_user=False
                    game_state='home'
                    menu=True
                    reset_pointers()
#-----------------------------ARE YOU SURE--------------------------------------------
        if are_you_sure:
            game_state='are_you_sure'
            are_you_sure_swap(are_you_sure_pointer)
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        are_you_sure_pointer = limit_number_for_2(are_you_sure_pointer - 1)
                    if event.key == pygame.K_DOWN:
                        are_you_sure_pointer = limit_number_for_2(are_you_sure_pointer + 1)
                    if event.key == pygame.K_RETURN:
                        if are_you_sure_pointer==0:
                            running=False
                        elif are_you_sure_pointer==1:
                            are_you_sure=False
                            reset_pointers()
                            game_state=last_game_state
                    if event.key == pygame.K_ESCAPE:
                        running=False
            pygame.display.update()
#-----------------------------SCOREBOARD--------------------------------------------
        if scoreboard_lookup:
            game_state='scoreboard'
            display_scoreboard(scoreboard)
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        scoreboard_lookup=False
                        reset_pointers()
                        menu=True
                        game_state=last_game_state
            pygame.display.update()
#-----------------------------HISTORY--------------------------------------------
        if history_lookup:
            game_state='history'
            display_history(username,history)
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        history_lookup=False
                        reset_pointers()
                        menu=True
                        game_state=last_game_state
            pygame.display.update()
#-----------------------------LOGIN SCREEN--------------------------------------------
        if game_state=='login_screen':
            login_swap(login_selection_pointer)
            display_username(username_display)
            display_password(password_display)
            if wrong_password:
                display_wrong_password(wrong_password)
                wrong_password=False
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == K_UP:
                        login_selection_pointer=limit_number(login_selection_pointer-1)
                        login_swap(login_selection_pointer)
                    if event.key == K_DOWN:
                        login_selection_pointer=limit_number(login_selection_pointer+1)
                        login_swap(login_selection_pointer)
                    if event.key == K_ESCAPE:
                        last_game_state=game_state
                        are_you_sure=True
                    if login_selection_pointer==0:
                        if event.key == K_BACKSPACE and len(username)>0:
                            username=username[:-1]
                            username_display[len(username)]='_'
                        if event.unicode in AUTHORIZED_LETTERS and len(username)<6 and event.key not in KEYS:
                            username+=event.unicode
                            username_display[len(username)-1]=event.unicode
                    if login_selection_pointer==1:
                        if event.key == K_BACKSPACE and len(password)>0:
                            password=password[:-1]
                            password_display[len(password)]='_'
                        if event.unicode in AUTHORIZED_LETTERS and len(password)<4 and event.key not in KEYS:
                            password+=event.unicode
                            password_display[len(password)-1]=event.unicode
                    if login_selection_pointer==2:
                        if event.key == K_RETURN:
                            if username=='' or password=='':
                                continue
                            if user_check(username):
                                if TRUE_login(username,password):
                                    menu=True
                                    game_state='home'
                                if not TRUE_login(username,password):
                                    wrong_password=True
                                    login_selection_pointer=1
                                    password_display=['_']*4
                                    password=''
                            elif not user_check(username):
                                game_state='new_user'
                                new_user=True
            
            pygame.display.update()


#-----------------------------HOME SCREEN---------------------------------------
        if game_state=='home':
            DISPLAYSURF.fill(BLACK)
            if new_high_score:
                display_NEW_HIGH_SCORE()
                new_high_score=False
            if menu:
                menu_swap(menu_selection_pointer)
            if difficulty_lookup:
                DISPLAYSURF.blit(COMIC_SANS.render('Select difficulty:', False, WHITE),(350,200))
                level_swap(level_selection_pointer)
            display_welcome_message(new_user)
            DISPLAYSURF.blit(COMIC_SANS_SMOL.render('SPACE: play, ENTER: select, BACKSPACE: return, ESC: quit', False, GREY),(200,600))
            DISPLAYSURF.blit(COMIC_SANS_BIG.render(f'Welcome to Snake {username}', False, WHITE),(200,75))
            for event in events:
                if event.type == pygame.KEYDOWN:

                    
#-----------------------------MENU----------------------------------------------
                    if menu:
                        difficulty_lookup=False
                        history_lookup=False
                        scoreboard_lookup=False
                        if event.key == K_UP:
                            menu_selection_pointer=limit_number(menu_selection_pointer-1)
                            menu_swap(menu_selection_pointer)
                        if event.key == K_DOWN:
                            menu_selection_pointer=limit_number(menu_selection_pointer+1)
                            menu_swap(menu_selection_pointer)
                        if event.key == pygame.K_RETURN:
                            if menu_selection_pointer==0:
                                reset_pointers()
                                difficulty_lookup=True
                            if menu_selection_pointer==1:
                                reset_pointers()
                                last_game_state=game_state
                                scoreboard_lookup=True
                            if menu_selection_pointer==2:
                                reset_pointers()
                                last_game_state=game_state
                                history_lookup=True
                        if event.key==pygame.K_BACKSPACE:
                            reset_pointers()
                            menu=False
                            game_state='login_screen'
                            username=''
                            password=''
                            username_display=['_']*6
                            password_display=['_']*4


#-----------------------------DIFFICULTY-------------------------------------------
                    if difficulty_lookup:
                        menu=False
                        if event.key == K_UP:
                            level_selection_pointer=limit_number(level_selection_pointer-1)
                            level_swap(level_selection_pointer)
                        if event.key == K_DOWN:
                            level_selection_pointer=limit_number(level_selection_pointer+1)
                            level_swap(level_selection_pointer)
                        if event.key == pygame.K_SPACE:
                            reset_game()
                            game_state='game'
                        if event.key==pygame.K_BACKSPACE:
                            menu=True
                            difficulty_lookup=False
                            reset_pointers()
#-----------------------------HISTORY-------------------------------------------
                    if history_lookup:
                        menu=False
                        if event.key==pygame.K_BACKSPACE:
                            reset_pointers()
                            menu=True
                            history_lookup=False
#-----------------------------SCOREBOARD-------------------------------------------
                    if scoreboard_lookup:
                        menu=False
                        if event.key==pygame.K_BACKSPACE:
                            reset_pointers()
                            menu=True
                            scoreboard_lookup=False
                    if event.key == pygame.K_ESCAPE:
                        last_game_state=game_state
                        are_you_sure=True
                if event.type == pygame.QUIT:
                    running = False
            pygame.display.update()


#-----------------------------GAME SCREEN---------------------------------------
        if game_state=='game':
            # update_scoreboard(history,scoreboard)
            display_game()
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        game_state='home'
                    last_direction = snake.direction
                    if event.type == KEYDOWN:
                        if event.key == K_LEFT and last_direction != "right":
                            snake.direction = "left"
                        if event.key == K_RIGHT and last_direction != "left":
                            snake.direction = "right"
                        if event.key == K_UP and last_direction != "down":
                            snake.direction = "up"
                        if event.key == K_DOWN and last_direction != "up":
                            snake.direction = "down"
                if event.type == pygame.QUIT:
                    running = False
            for i in range(1, len(snake.body)):
                if snake.body[0] == snake.body[i]:
                    game_over=True
            if snake.x < 1 or snake.x > LEVEL_SETTINGS[level_selection_pointer]['INNER_GRID_WIDTH'] or snake.y < 1 or snake.y > LEVEL_SETTINGS[level_selection_pointer]['INNER_GRID_HEIGHT']:
                game_over=True
            if game_over:
                if snake.score >1:
                    history[username][TRANSLATE_POINTER[level_selection_pointer]]=history[username][TRANSLATE_POINTER[level_selection_pointer]]+[snake.score]
                history_dumper(history)
                last_scoreboard=scoreboard
                scoreboard={}
                scoreboard=update_scoreboard(history,scoreboard)
                if scoreboard!=last_scoreboard:
                    new_high_score=True
                    difficulty_lookup=False
                    game_state='home'
                    menu=True
                game_state='home'
                game_over=False
            if snake.x == food.x and snake.y == food.y:
                snake.eat()
                food.new_food()
            DISPLAYSURF.fill(RED,((food.x*LEVEL_SETTINGS[level_selection_pointer]['CELL_SIZE']),(food.y*LEVEL_SETTINGS[level_selection_pointer]['CELL_SIZE']),LEVEL_SETTINGS[level_selection_pointer]['CELL_SIZE']-1,LEVEL_SETTINGS[level_selection_pointer]['CELL_SIZE']-1))
            snake.move()
            pygame.display.update()
            pygame.time.wait(LEVEL_SETTINGS[level_selection_pointer]['SPEED'])
pygame.quit()