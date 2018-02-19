import pygame, sys
from game import game
from title_screen import title_screen
from board import Block
from load_image import load_image

def terminate():
    pygame.quit()
    sys.exit()

def load_level(filename):
    fullname = 'levels/' + filename
    with open(fullname, 'r') as levelFile:
        file = levelFile.readlines()
        level_tools = list(map(lambda x:x.strip(), file[0].split(';')))
        level_map = list(map(lambda x : x.strip().split(), file[1:]))
    return level_tools, level_map[1:]

def generate_level(level):
    if level[0][0] != 'None':
        tools = level[0]
        tiles = [[tools[0], tools[1], list(map(lambda x:x.strip(), tools[2].split(',')))], []]
    else:
        tiles = [[None], []]
    level = level[1]
    for i in range(len(level)):
        for j in range(len(level[i])):
            if level[i][j] != 'def':
                if level[i][j] != 'None':
                    tiles[1].append(((i, j), Block(level[i][j])))
                else:
                    tiles[1].append(((i, j), None))
    return tiles

try_again = True
quit = title_screen()
level = load_level('level1.txt')
level_walls = load_level('level1_walls.txt')

level = generate_level(level)
level_walls = generate_level(level_walls)

if not quit:
    while try_again:
        try_again = game(level, level_walls)
terminate()