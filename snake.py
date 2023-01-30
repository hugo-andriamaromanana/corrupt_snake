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
pygame.display.set_caption("snake")
screen = pygame.display.set_mode((960, 660))
screen.fill(GREY)
#------------SNAKE----------------
#Creating my snake
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
        self.x = random.randint(1, 30)
        self.y = random.randint(1, 20)
    def new_food(self):
        self.x = random.randint(1, 30)
        self.y = random.randint(1, 20)

if __name__ == "__main__":
        #------------GRID----------------
    grid = [[0 for _ in range(32)] for _ in range(22)]
    grid = [[1]+row[1:] for row in grid]
    grid = [row[:-1]+[1] for row in grid]
    grid[0]=[1 for _ in range(32)]
    grid[-1]=[1 for _ in range(32)]
    running=True
    cell_size=30
    food=Food()
    snake=Snake()
    while running:
        body = snake.body
        for pos_y in range(len(grid)):
            for pos_x in range(len(grid[pos_y])):
                if grid[pos_y][pos_x]==0:
                    DISPLAYSURF.fill(WHITE, ((pos_x*cell_size),(pos_y*cell_size),cell_size-1,cell_size-1))
                elif grid[pos_y][pos_x]==1:
                    DISPLAYSURF.fill(PINK, ((pos_x*cell_size),(pos_y*cell_size),cell_size-1,cell_size-1))
        #Save last direction to avoid backtracking
        events = pygame.event.get()
        for coords in range(len(body)):
            DISPLAYSURF.fill(GREEN, ((body[coords][0]*cell_size),(body[coords][1]*cell_size),cell_size-1,cell_size-1))
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
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
        if snake.x < 1 or snake.x > 30 or snake.y < 1 or snake.y > 20:
            running = False
            print("You lost!")
        if snake.x == food.x and snake.y == food.y:
            snake.eat()
            food.new_food()
        DISPLAYSURF.fill(RED, ((food.x*cell_size),(food.y*cell_size),cell_size-1,cell_size-1))
        snake.move()
        pygame.time.wait(100)
        pygame.display.update()
pygame.quit()