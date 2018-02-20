import pygame,os
from tools import load_image
    
class Board:
    def __init__(self, tiles_size, size, tile_size, default_tile, tiles, spawns = None):
        self.tiles_w, self.tiles_h = tiles_size[0], tiles_size[1]
        self.width, self.height = size[0], size[1]
        self.board, self.cell_size = default_tile, tile_size
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                for m in tiles:
                    if (i, j) == m[0]:
                        self.board[j][i] = m[1]
                if isinstance(self.board[j][i],Block):
                    self.board[j][i].update_pos((j, i)) 
                                              
                        
    def check_collision(self, p1, p2, enemy = False):
        coords = self.get_cell(p1, p2)
        if coords != None:
            if self.board[int(coords[0])][int(coords[1])] == None:
                return True
        elif coords == None and enemy:
            return True
        return False
    
    def get_cell(self, w, h):
        if 0 < w < self.width and 0 < h < self.height:
            return (w // self.cell_size, h // self.cell_size)
    
    def load(self, group):
        for i in self.board:
            for j in i:
                if j != None:
                    group.add(j)


class Block(pygame.sprite.Sprite):
    def __init__(self, type, pos = (0, 0)):
        super().__init__()
        self.image = load_image(type)
        self.rect = self.image.get_rect()
        self.square = True
        if self.rect.height != self.rect.width:
            self.square = False
        self.rect.topleft = pos[0] * self.rect.width, pos[1] * self.rect.height    
        
    def update_pos(self, pos):
        self.rect.topleft = pos[0] * self.rect.width, pos[1] * self.rect.height  
        if self.rect.height > self.rect.width:
            self.rect.y = pos[1] * self.rect.width - self.rect.height + self.rect.width
        else:
            self.rect.y = pos[1] * self.rect.height