import json
import pygame
from pygame.locals import *
import time
import random

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

#------------json----------------
with open("scoreboard.json","r") as f:
    scoreboard = json.load(f)
#--------------const--------------
DISPLAYSURF = pygame.display.set_mode((960, 660))
#------------pygame----------------
pygame.init()
pygame.font.init()
pygame.mixer.init()
pygame.display.set_caption("snake")
#------------screen----------------
screen = pygame.display.set_mode((960, 660))
screen.fill(GREY)
#------------Menu_vars----------------
level_selection_pointer=-1
#------------music----------------
# select=pygame.mixer.Sound("tone1.mp3")
#------------SNAKE----------------
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

LEVEL_SETTINGS={
    -1: {
        'GRID_HEIGHT': 22,
         'GRID_WIDTH': 32,
         'INNER_GRID_HEIGHT': 20,
         'INNER_GRID_WIDTH': 30,
         'SPEED': 100
         },
    0: {
        'GRID_HEIGHT': 12,
         'GRID_WIDTH': 22,
         'INNER_GRID_HEIGHT': 10,
         'INNER_GRID_WIDTH': 20,
         'SPEED': 200
         },
    1: {
        'GRID_HEIGHT': 22,
         'GRID_WIDTH': 32,
         'INNER_GRID_HEIGHT': 20,
         'INNER_GRID_WIDTH': 30,
         'SPEED': 100
         },
}

TRANSLATE_POINTER = {
    -1: 'Hard',
    0: 'Medium',
    1: 'Easy'
}

class Food():
    def __init__(self):
        self.x = random.randint(1, LEVEL_SETTINGS[level_selection_pointer]['INNER_GRID_WIDTH'])
        self.y = random.randint(1, LEVEL_SETTINGS[level_selection_pointer]['INNER_GRID_HEIGHT'])
    def new_food(self):
        self.x = random.randint(1, LEVEL_SETTINGS[level_selection_pointer]['INNER_GRID_WIDTH'])
        self.y = random.randint(1, LEVEL_SETTINGS[level_selection_pointer]['INNER_GRID_HEIGHT'])

def reset():
    global snake
    global food
    snake = Snake()
    food = Food()

def button_swap(level_selection_pointer):
    passive_color=WHITE
    if level_selection_pointer == 1:
        DISPLAYSURF.blit(COMIC_SANS.render('-> Easy', False, GREEN),(400,350))
        DISPLAYSURF.blit(COMIC_SANS.render('Medium', False, passive_color),(400,400))
        DISPLAYSURF.blit(COMIC_SANS.render('Hard', False, passive_color),(400,450))
    elif level_selection_pointer == 0:
        DISPLAYSURF.blit(COMIC_SANS.render('Easy', False, passive_color),(400,350))
        DISPLAYSURF.blit(COMIC_SANS.render('-> Medium', False, YELLOW),(400,400))
        DISPLAYSURF.blit(COMIC_SANS.render('Hard', False, passive_color),(400,450))
    elif level_selection_pointer == -1:
        DISPLAYSURF.blit(COMIC_SANS.render('Easy', False, passive_color),(400,350))
        DISPLAYSURF.blit(COMIC_SANS.render('Medium', False, passive_color),(400,400))
        DISPLAYSURF.blit(COMIC_SANS.render('-> Hard', False, RED),(400,450))

if __name__ == "__main__":
    running=True
    cell_size=30
    snake=Snake()
    game_state='home'
    COMIC_SANS_SMOL = pygame.font.SysFont('Comic Sans MS', 20)
    COMIC_SANS = pygame.font.SysFont('Comic Sans MS', 30)
    COMIC_SANS_BIG = pygame.font.SysFont('Comic Sans MS', 50)
    limit_number = lambda n: max(min(n, 1), -1)
    while running:
        screen.fill(GREY)
        events = pygame.event.get()
        if game_state=='home':
            DISPLAYSURF.fill(BLACK)
            DISPLAYSURF.blit(COMIC_SANS.render('Select difficulty:', False, WHITE),(350,300))
            button_swap(level_selection_pointer)
            DISPLAYSURF.blit(COMIC_SANS_SMOL.render('Use your arrows to select', False, WHITE),(400,500))
            DISPLAYSURF.blit(COMIC_SANS_BIG.render('Welcome to snake', False, WHITE),(300,200))
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == K_UP:
                        level_selection_pointer=limit_number(level_selection_pointer+1)
                        button_swap(level_selection_pointer)
                    if event.key == K_DOWN:
                        level_selection_pointer=limit_number(level_selection_pointer-1)
                        button_swap(level_selection_pointer)
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    if event.key == pygame.K_SPACE:
                        game_state='game'
                        reset()
                        print(TRANSLATE_POINTER[level_selection_pointer])
                if event.type == pygame.QUIT:
                    running = False
            pygame.display.update()
        if game_state=='game':
            grid = [[0 for _ in range(LEVEL_SETTINGS[level_selection_pointer]['GRID_WIDTH'])] for _ in range(LEVEL_SETTINGS[level_selection_pointer]['GRID_HEIGHT'])]
            grid = [[1]+row[1:] for row in grid]
            grid = [row[:-1]+[1] for row in grid]
            grid[0]=[1 for _ in range(LEVEL_SETTINGS[level_selection_pointer]['GRID_WIDTH'])]
            grid[-1]=[1 for _ in range(LEVEL_SETTINGS[level_selection_pointer]['GRID_WIDTH'])]
            body = snake.body
            for pos_y in range(len(grid)):
                for pos_x in range(len(grid[pos_y])):
                    if grid[pos_y][pos_x]==0:
                        DISPLAYSURF.fill(WHITE, ((pos_x*cell_size),(pos_y*cell_size),cell_size-1,cell_size-1))
                    elif grid[pos_y][pos_x]==1:
                        DISPLAYSURF.fill(PINK, ((pos_x*cell_size),(pos_y*cell_size),cell_size-1,cell_size-1))
            for coords in range(len(body)):
                DISPLAYSURF.fill(GREEN, ((body[coords][0]*cell_size),(body[coords][1]*cell_size),cell_size-1,cell_size-1))
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
                    game_state='home'
            if snake.x < 1 or snake.x > LEVEL_SETTINGS[level_selection_pointer]['INNER_GRID_WIDTH'] or snake.y < 1 or snake.y > LEVEL_SETTINGS[level_selection_pointer]['INNER_GRID_HEIGHT']:
                game_state='home'
            if snake.x == food.x and snake.y == food.y:
                snake.eat()
                food.new_food()
            DISPLAYSURF.fill(RED, ((food.x*cell_size),(food.y*cell_size),cell_size-1,cell_size-1))
            snake.move()
            pygame.display.update()
            pygame.time.wait(LEVEL_SETTINGS[level_selection_pointer]['SPEED'])
pygame.quit()