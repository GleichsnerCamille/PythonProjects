import pygame
import random
import tkinter as tk
from tkinter import messagebox

pygame.font.init()

screenWidth = 600
screenHeight = 700
boardWidth = 300
boardHeight = 600
blockSize = 30
upperLeftX = (screenWidth - boardWidth) / 2
upperLeftY = screenHeight - boardHeight

S = [['.....',
      '.....',
      '..00.',
      '.00..',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

shapes = [S, Z, I, O, J, L, T]
colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]
score = 0


class Piece(object):
    rows = 20
    columns = 10  # x

    def __init__(self, column, row, shape):
        self.x = column
        self.y = row
        self.shape = shape
        self.color = colors[shapes.index(shape)]
        self.rotation = 0


# Board
def makeBoard(posLock={}):
    grid = [[(0, 0, 0) for x in range(10)] for x in range(20)]

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j, i) in posLock:
                c = posLock[(j, i)]
                grid[i][j] = c
    return grid


def drawBoard(surface, row, col):
    sx = upperLeftX - 45
    sy = upperLeftY - 45
    for i in range(row):
        pygame.draw.line(surface, (128, 128, 128), (sx, sy + i * 30),
                         (sx + boardWidth, sy + i * 30))
        for j in range(col):
            pygame.draw.line(surface, (128, 128, 128), (sx + j * 30, sy),
                             (sx + j * 30, sy + boardHeight))


# Shape
def formatShape(shape):
    positions = []
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                positions.append((shape.x + j, shape.y + i))

    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)

    return positions


def getShape():
    global shapes, colors

    return Piece(5, 0, random.choice(shapes))


def drawShape(shape, surface):
    font = pygame.font.SysFont('georgia', 30)
    label = font.render('Next Shape: ', 1, (255, 255, 255))

    sx = upperLeftX + boardWidth - 22
    sy = upperLeftY + boardHeight / 2 - 250

    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, shape.color, (sx + j * 30, sy + i * 30, 30, 30), 0)

    surface.blit(label, (sx + 10, sy - 10))


# Mechanics
def valid(shape, grid):
    accept = [[(j, i) for j in range(10) if grid[i][j] == (0, 0, 0)] for i in range(20)]
    accept = [j for sub in accept for j in sub]
    formatted = formatShape(shape)

    for pos in formatted:
        if pos not in accept:
            if pos[1] > -1:
                return False

    return True


def clearRow(grid, locked):
    inc = 0
    for i in range(len(grid) - 1, -1, -1):
        row = grid[i]
        if (0, 0, 0) not in row:
            inc += 1
            ind = i
            for j in range(len(row)):
                try:
                    del locked[(j, i)]

                except:
                    continue
    if inc > 0:
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                newKey = (x, y + inc)
                locked[newKey] = locked.pop(key)


def Lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True
    return False


# Score
# def scoreUp(score):
#    score = score + 1
#    print(score)
#    return score

# def draw_score(score, surface):
# font = pygame.font.SysFont('comicsans', 40)
# global scoreLabel
# scoreLabel = font.render('Score: {}'.format(score), 1, (255, 255, 255))
# sx = (upperLeftX + boardWidth - 5)
# sy =(upperLeftY + boardHeight / 2 + 40)
# #todo fix


# Main Draws
def drawWindow(surface):
    surface.fill((0, 0, 0))

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], (upperLeftX - 45 + j * 30, upperLeftY - 45 + i * 30, 30, 30), 0)

    drawBoard(surface, 20, 10)
    pygame.draw.rect(surface, (128, 128, 128), (upperLeftX - 45, upperLeftY - 45, boardWidth, boardHeight), 3)


def messageBox(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass


def main():
    global grid

    posLock = {}
    grid = makeBoard(posLock)

    changePiece = False
    run = True
    piece = getShape()
    nextPiece = getShape()
    clock = pygame.time.Clock()
    time = 1

    while run:
        speed = 0.28
        grid = makeBoard(posLock)
        time += clock.get_rawtime()
        clock.tick()

        # fall
        if time / 1000 >= speed:
            time = 0
            piece.y += 1
            if not (valid(piece, grid)) and piece.y > 0:
                piece.y -= 1
                changePiece = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    piece.x -= 1
                    if not valid(piece, grid):
                        piece.x += 1

                elif event.key == pygame.K_RIGHT:
                    piece.x += 1
                    if not valid(piece, grid):
                        piece.x -= 1
                elif event.key == pygame.K_UP:
                    piece.rotation = piece.rotation + 1 % len(piece.shape)
                    if not valid(piece, grid):
                        piece.rotation = piece.rotation - 1 % len(piece.shape)

                if event.key == pygame.K_SPACE:
                    while valid(piece, grid):
                        piece.y += 1
                    piece.y -= 1

        shapePos = formatShape(piece)

        # prepare piece
        for i in range(len(shapePos)):
            x, y = shapePos[i]
            if y > -1:
                grid[y][x] = piece.color

        # Piece collides
        if changePiece:
            for pos in shapePos:
                p = (pos[0], pos[1])
                posLock[p] = piece.color
            piece = nextPiece
            nextPiece = getShape()
            changePiece = False
            clearRow(grid, posLock)

        drawWindow(win)
        drawShape(nextPiece, win)
        pygame.display.update()

        if Lost(posLock):
            run = False

    messageBox('Game Over', 'Play again?')
    main()
    pygame.display.update()
    pygame.time.delay(1000)


win = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption('Tetris')

main()
