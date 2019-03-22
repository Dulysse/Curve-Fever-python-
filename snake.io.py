import pygame, sys
from pygame.locals import *
import random

#initialisation de la surface Pygame
pygame.init()

#nom/FPS de la fenetre définis
fpsClock = pygame.time.Clock()
pygame.display.set_caption('Snake.io')
mySurface = pygame.display.set_mode((1000,1000))

#COLOR
BLACK = (0,0,0)
RED = (255,0,0)

#Images
image_Cell_1 = pygame.image.load("IMAGES/cell_1.bmp")
image_vide = pygame.image.load("IMAGES/vide.bmp")
image_Fruit = pygame.image.load("IMAGES/fruit.bmp")
game_over = pygame.image.load("IMAGES/game_over.jpg")
spacebar = pygame.image.load("IMAGES/start.png")

def initBoard():
    hit = False
    score = 0
    FPS = 20
    dir = 'null'
    n = 100
    board = [[0]*n for i in range(n)]
    i,j = fruitNewPosition()
    board[i][j] = 3
    m , l = 50 , 50
    board[m][l] = 1
    return board,hit,score,dir,FPS

def fruitNewPosition():
    x_fruit,y_fruit = aleatPos(),aleatPos()
    return x_fruit,y_fruit

def aleatPos():
    x = random.randrange(10,90)
    return x

def drawBoard(mySurface,board):
    for j in range(100):
        for i in range(100):
            cell = board[j][i]
            if cell == 0:
                draw_vide(mySurface,board, i, j)
            elif cell == 1 or cell == 2:
                draw_Cell(mySurface,board, i, j)
            elif cell == 3:
                draw_Fruit(mySurface,board, i, j)

def draw_vide(mySurface,board, x, y):
    mySurface.blit(image_vide,(x * 10, y * 10))

def draw_Cell(mySurface,board, x, y):
    mySurface.blit(image_Cell_1,(x * 10, y * 10))

def draw_Fruit(mySurface,board, x, y):
    mySurface.blit(image_Fruit,(x * 10, y * 10))

def findHead():
    for i in range(100):
        for j in range(100):
            if board[i][j] == 1:
                return i,j

def moveOn(dir,board):
    x_head, y_head = findHead()
    if dir == 'up':
        if board[x_head-1][y_head] == 3:
            board = getFruit(board,x_head,y_head)
        elif board[x_head-1][y_head] == 2 or x_head == 1:
            board = collide()

        board[x_head][y_head] = 2
        board[x_head-1][y_head] = 1
    if dir == 'down':
        if board[x_head+1][y_head] == 3:
            board = getFruit(board,x_head,y_head)
        elif board[x_head+1][y_head] == 2 or x_head == 98:
            board = collide()
        board[x_head][y_head] = 2
        board[x_head+1][y_head] = 1
    if dir == 'left':
        if board[x_head][y_head-1] == 3:
            board = getFruit(board,x_head,y_head)
        elif board[x_head][y_head-1] == 2 or y_head == 1:
            board = collide()
        board[x_head][y_head] = 2
        board[x_head][y_head-1] = 1
    if dir == 'right':
        if board[x_head][y_head+1] == 3:
            board = getFruit(board,x_head,y_head)
        elif board[x_head][y_head+1] == 2 or y_head == 98:
            board = collide()
        board[x_head][y_head] = 2
        board[x_head][y_head+1] = 1
    return board

def getFruit(board,x_head,y_head):
    global score,FPS
    x_fruit, y_fruit = fruitNewPosition()
    for x in range(100):
        for y in range(100):
            board[x][y] = 0
    board[x_head][y_head] = 1
    board[x_fruit][y_fruit] = 3
    score += 1
    FPS += score
    return board

def collide():
    global hit
    hit = True
    return board

#boucle de jeu
Snake = True
board,hit,score,dir,FPS = initBoard()
while Snake:
    #gestion des events
    for event in pygame.event.get():
        if event.type == QUIT:
            Snake = False
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                Snake = False
            if event.key == K_UP:
                if dir != 'down':
                    dir = 'up'
            if event.key == K_DOWN:
                if dir != 'up':
                    dir = 'down'
            if event.key == K_LEFT:
                if dir != 'right':
                    dir = 'left'
            if event.key == K_RIGHT:
                if dir != 'left':
                    dir = 'right'
            if event.key == K_SPACE:
                board,hit,score,dir,FPS = initBoard()
    #affichage
    drawBoard(mySurface,board)
    if not dir=="null":
        if not hit:
            board = moveOn(dir,board)
    if hit:
        mySurface.blit(game_over,(280,200))
        mySurface.blit(spacebar,(300,600))
    myfont = pygame.font.SysFont('freesansbold.ttf',100)
    score_display = myfont.render(str(score),True,RED,BLACK)
    score_rect = score_display.get_rect()
    score_rect.topleft = (500,0)
    mySurface.blit(score_display,score_rect)
    #rafraichissement de la surface
    pygame.display.update()
    fpsClock.tick(FPS)
pygame.quit()
