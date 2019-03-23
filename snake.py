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
image_point = pygame.image.load("IMAGES/point.bmp")
game_over = pygame.image.load("IMAGES/game_over.jpg")
spacebar = pygame.image.load("IMAGES/start.png")

def initBoard():
    FPS = 20
    dir = 'null'
    hit = False
    n = 50
    score = ""
    x,y = initRandom(n)
    if n == 100:
        delta = 0
    else:
        delta = ((100-n) // 2 )*10
    snakeSize = 20
    board = [[0]*n for i in range(n)]
    boardDtoH = [[0]*n for i in range(n)]
    m , l = n//2 , n//2
    board[m][l] = 1
    boardDtoH[m][l] = snakeSize
    board[x][y] = 3
    return board,dir,FPS,boardDtoH,snakeSize,n,delta,hit,score

def initRandom(n):
    x = random.randrange(0,n)
    y = random.randrange(0,n)
    return x,y

def drawBoard(mySurface,board,boardDtoH,n,delta):
    for j in range(n):
        for i in range(n):
            cell = board[j][i]
            if cell == 0:
                draw_vide(mySurface,board, i, j,delta)
            elif cell == 1 or cell == 2:
                if boardDtoH[j][i] != 0:
                    draw_Cell(mySurface,board, i, j,delta)
            elif cell == 3:
                draw_point(mySurface,board, i, j,delta)

def draw_vide(mySurface,board, x, y,delta):
    mySurface.blit(image_vide,(x * 10 + delta, y * 10 + delta))

def draw_Cell(mySurface,board, x, y,delta):
    mySurface.blit(image_Cell_1,(x * 10 + delta, y * 10 + delta))

def draw_point(mySurface,board, x, y,delta):
    mySurface.blit(image_point,(x * 10 + delta, y * 10 + delta))

def findHead(n):
    for i in range(n):
        for j in range(n):
            if board[i][j] == 1:
                return i,j

def moveOn(dir,board,n):
    x_head, y_head = findHead(n)
    if dir == 'up':
        board = getPoint(board,n,x_head-1,y_head)
        collision(board,n,x_head-1,y_head)
        board[x_head][y_head] = 2
        board[x_head-1][y_head] = 1
    if dir == 'down':
        if x_head == n-1:
            x_head = 0
            board[x_head-1][y_head] = 2
        collision(board,n,x_head+1,y_head)
        board = getPoint(board,n,x_head+1,y_head)
        board[x_head][y_head] = 2
        board[x_head+1][y_head] = 1
    if dir == 'left':
        board = getPoint(board,n,x_head,y_head-1)
        collision(board,n,x_head,y_head-1)
        board[x_head][y_head] = 2
        board[x_head][y_head-1] = 1
    if dir == 'right':
        if y_head == n-1:
            y_head = 0
            board[x_head][y_head-1] = 2
        board = getPoint(board,n,x_head,y_head+1)
        collision(board,n,x_head,y_head+1)
        board[x_head][y_head] = 2
        board[x_head][y_head+1] = 1
    return board

def collision(board,n,x_head,y_head):
    global hit
    if board[x_head][y_head] == 2:
        hit = True

def getPoint(board,n,x_head,y_head):
    global snakeSize
    for i in range(n):
        for j in range(n):
            if board[i][j] == 3:
                x_point,y_point = i,j
    if x_point == x_head:
        if y_point == y_head:
            snakeSize += 1
            x,y = initRandom(n)
            while board[x][y] != 0:
                x,y = initRandom(n)
            board[x][y] = 3
    return board

def displayToHide(board,boardDtoH,snakeSize,n):
    for x in range(n):
        for y in range(n):
            if board[x][y] == 2 or board[x][y] == 1:
                if boardDtoH[x][y] == 0:
                    boardDtoH[x][y] = snakeSize
                else:
                    boardDtoH[x][y] -= 1
    return boardDtoH

def joinBoards(board,boardDtoH,n):
    for i in range(n):
        for j in range(n):
            if boardDtoH[i][j] == 0:
                if not board[i][j] == 3:
                    board[i][j] = 0
    return board

def displayBoard(board):
    for lignes in board:
        for x in lignes:
            print(x,"  ",end="")
        print('\n')
    print('\n\n\n\n')

#boucle de jeu
Snake = True
board,dir,FPS,boardDtoH,snakeSize,n,delta,hit,score = initBoard()
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
                board,dir,FPS,boardDtoH,snakeSize,n,delta,hit,score = initBoard()
    #affichage
    mySurface.fill(BLACK)
    drawBoard(mySurface,board,boardDtoH,n,delta)
    if not dir=="null":
        if not hit:
            board = moveOn(dir,board,n)
            boardDtoH = displayToHide(board,boardDtoH,snakeSize,n)
            board = joinBoards(board,boardDtoH,n)
        if hit:
            mySurface.blit(game_over,(290,200))
            mySurface.blit(spacebar,(320,600))
    score = snakeSize - 20
    myfont = pygame.font.SysFont('freesansbold.ttf',100)
    score_display = myfont.render(str(score),True,RED,BLACK)
    score_rect = score_display.get_rect()
    score_rect.topleft = (500,100)
    mySurface.blit(score_display,score_rect)

    #rafraichissement de la surface
    pygame.display.update()
    fpsClock.tick(FPS)
pygame.quit()
