import pygame, sys
from game import game
from title_screen import title_screen
from board import Block
from tools import load_image

def load_level(filename):
    fullname = 'levels/' + filename
    with open(fullname, 'r') as levelFile:
        file = levelFile.readlines()
        level_tools = list(map(lambda x : x.strip(), file[0].split(';')))
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

try_again, quit = True, False

level, level_walls = load_level('level1.txt'), load_level('level1_walls.txt')
level, level_walls = generate_level(level), generate_level(level_walls)

pygame.mixer.init()
pygame.mixer.music.load('music/menu_music.mp3')
pygame.mixer.music.set_volume(0.25)
pygame.mixer.music.play(-1)  

while not quit:
    pygame.mixer.music.play(-1)
    quit = title_screen()
    if not quit:
        pygame.mixer.music.stop()
        while try_again:
            try_again, quit = game(level, level_walls)
    try_again = True
pygame.quit()
sys.exit()