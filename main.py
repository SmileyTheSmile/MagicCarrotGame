import pygame, sys
from game import game
from title_screen import title_screen

def terminate():
    pygame.quit()
    sys.exit()

def load_image(name, colorkey = None):
    fullname = os.path.join('resourses', name)
    try:
        return pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
title_screen()
game()
terminate()