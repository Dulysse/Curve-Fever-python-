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

#coordonnées
j1 = (1,2)
j2 = (4,5)


#Images
image_Cell_1 = pygame.image.load("IMAGES/cell_1.bmp")
image_Cell_2 = pygame.image.load("IMAGES/cell_2.bmp")
image_vide = pygame.image.load("IMAGES/vide.bmp")
image_Fruit = pygame.image.load("IMAGES/fruit.bmp")
game_over = pygame.image.load("IMAGES/game_over.jpg")
spacebar = pygame.image.load("IMAGES/start.png")
player1win = pygame.image.load("IMAGES/player1win.png")
player2win = pygame.image.load("IMAGES/player2win.png")
zqsd = pygame.image.load("IMAGES/zqsd.jpg")
fleches = pygame.image.load("IMAGES/fleches.jpg")

def malusreload():
    malus = "null"
    setTime = 20*8
    return malus,setTime

def initBoard():
    tps = 0
    hitj1 = False
    hitj2 = False
    FPS = 20
    dirj1 = 'up'
    dirj2 = 'down'
    n = 100
    board = [[0]*n for i in range(n)]
    i,j = fruitNewPosition(board)
    board[i][j] = 3
    m , l = 30 , 30
    o , p = 70 , 70
    board[m][l] = 4
    board[o][p] = 1
    return board,hitj1,hitj2,dirj1,dirj2,FPS,tps

def fruitNewPosition(board):
    x_fruit,y_fruit = aleatPos(),aleatPos()
    while board[x_fruit][y_fruit] != 0:
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
                draw_Cell_1(mySurface,board, i, j)
            elif cell == 4 or cell == 5:
                draw_Cell_2(mySurface,board, i, j)
            elif cell == 3:
                draw_Fruit(mySurface,board, i, j)

def draw_vide(mySurface,board, x, y):
    mySurface.blit(image_vide,(x * 10, y * 10))

def draw_Cell_1(mySurface,board, x, y):
    mySurface.blit(image_Cell_1,(x * 10, y * 10))

def draw_Cell_2(mySurface,board, x, y):
    mySurface.blit(image_Cell_2,(x * 10, y * 10))

def draw_Fruit(mySurface,board, x, y):
    mySurface.blit(image_Fruit,(x * 10, y * 10))

def findHead(joueur):
    for i in range(100):
        for j in range(100):
            if board[i][j] == joueur[0]:
                return i,j

def moveOn(dir,board,joueur):
    x_head, y_head = findHead(joueur)
    if dir == 'up':
        if board[x_head-1][y_head] == 3:
            board = getFruit(board,x_head,y_head,joueur)
        elif (board[x_head-1][y_head] != 0 and board[x_head-1][y_head] != 3) or x_head == 1:
            board = collide(joueur)
        board[x_head][y_head] = joueur[1]
        board[x_head-1][y_head] = joueur[0]
    if dir == 'down':
        if board[x_head+1][y_head] == 3:
            board = getFruit(board,x_head,y_head,joueur)
        elif (board[x_head+1][y_head] != 0 and board[x_head+1][y_head] != 3) or x_head == 98:
            board = collide(joueur)
        board[x_head][y_head] = joueur[1]
        board[x_head+1][y_head] = joueur[0]
    if dir == 'left':
        if board[x_head][y_head-1] == 3:
            board = getFruit(board,x_head,y_head,joueur)
        elif (board[x_head][y_head-1] != 0 and board[x_head][y_head-1] != 3) or y_head == 1:
            board = collide(joueur)
        board[x_head][y_head] = joueur[1]
        board[x_head][y_head-1] = joueur[0]
    if dir == 'right':
        if board[x_head][y_head+1] == 3:
            board = getFruit(board,x_head,y_head,joueur)
        elif (board[x_head][y_head+1] != 0 and board[x_head][y_head+1] != 3) or y_head == 98:
            board = collide(joueur)
        board[x_head][y_head] = joueur[1]
        board[x_head][y_head+1] = joueur[0]
    return board

def getFruit(board,x_head,y_head,joueur):
    global malus
    x_fruit, y_fruit = fruitNewPosition(board)
    board[x_fruit][y_fruit] = 3
    if joueur[0] == 1:
        malus = "j2"
    else:
        malus = "j1"
    return board

def collide(joueur):
    global hitj1,hitj2
    if joueur[0] == 1:
        hitj1 = True
    else:
        hitj2 = True
    return board

#boucle de jeu
Snake = True
malus,setTime = malusreload()
board,hitj1,hitj2,dirj1,dirj2,FPS,tps = initBoard()
while Snake:
    #gestion des events
    for event in pygame.event.get():
        if event.type == QUIT:
            Snake = False
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                Snake = False
            if event.key == K_UP:
                if dirj1 != 'down':
                    dirj1 = 'up'
            if event.key == K_DOWN:
                if dirj1 != 'up':
                    dirj1 = 'down'
            if event.key == K_LEFT:
                if dirj1 != 'right':
                    dirj1 = 'left'
            if event.key == K_RIGHT:
                if dirj1 != 'left':
                    dirj1 = 'right'
            if event.key == K_w:
                if dirj2 != 'down':
                    dirj2 = 'up'
            if event.key == K_s:
                if dirj2 != 'up':
                    dirj2 = 'down'
            if event.key == K_a:
                if dirj2 != 'right':
                    dirj2 = 'left'
            if event.key == K_d:
                if dirj2 != 'left':
                    dirj2 = 'right'
            if event.key == K_SPACE:
                if hitj1 or hitj2:
                    malus,setTime = malusreload()
                    board,hitj1,hitj2,dirj1,dirj2,FPS,tps = initBoard()
    #affichage
    drawBoard(mySurface,board)
    if not (hitj1 or hitj2):
        if malus == "j1":
            if setTime >= 0:
                setTime -= 1
                if setTime % 3 == 0:
                    board = moveOn(dirj1,board,j1)
            else:
                malus,setTime = malusreload()
        if malus == "j2":
            if setTime >= 0:
                setTime -= 1
                if setTime % 3 == 0:
                    board = moveOn(dirj2,board,j2)
            else:
                malus,setTime = malusreload()
        if malus != "j1":
            board = moveOn(dirj1,board,j1)
        if malus != "j2":
            board = moveOn(dirj2,board,j2)

    if hitj1 or hitj2:
        mySurface.blit(game_over,(280,200))
        mySurface.blit(spacebar,(300,600))
    if hitj1:
        mySurface.blit(player2win,(400,100))
    if hitj2:
        mySurface.blit(player1win,(400,100))
    if tps < 20:
        mySurface.blit(fleches,(650,750))
        mySurface.blit(zqsd,(250,150))
        tps += 1


    #rafraichissement de la surface
    pygame.display.update()
    fpsClock.tick(FPS)
pygame.quit()
