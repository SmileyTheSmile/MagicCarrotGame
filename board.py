import pygame,os
def load_image(name, colorkey = None):
    fullname = os.path.join('resourses', name)
    try:
        return pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message) 
    
class Board:
    def __init__(self, tiles_size, size, tile_size, tiles=[]):
        self.tiles_w = tiles_size[0]
        self.tiles_h = tiles_size[1]
        self.width = size[0]
        self.height = size[1]
        self.cell_size = tile_size
        self.board = [[Block((i,j),'grass1.png',0) for i in range(self.tiles_w)] for j in range(self.tiles_h)]
        for i in range(self.tiles_w):
            for j in range(self.tiles_h):
                for m in tiles:
                    if m.pos == (i,j):
                        self.board[i][j]=m
                        
    def check_collision(self,p1,p2):
        p=self.get_cell(p1,p2)
        if p!= None:
            if self.board[p[0]][p[1]].collision==0:
                return True
        return False    
    
    def get_cell(self, w, h):
        if 0 < w < self.width and 0 < h < self.height:
            return (w//self.cell_size, h//self.cell_size )
    
    def load(self, group):
        for i in range(self.tiles_w):
            for j in range(self.tiles_h):
                if self.board[i][j]!=None:
                    group.add(self.board[i][j])


class Block(pygame.sprite.Sprite):
    def __init__(self,pos,type,collision):
        super().__init__()
        self.image = load_image(type)
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]*self.rect.width
        self.rect.y = pos[1]*self.rect.height
        self.pos = pos
        self.collision = collision