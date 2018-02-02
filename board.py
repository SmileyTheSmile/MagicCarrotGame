import pygame,os
def load_image(name, colorkey = None):
    fullname = os.path.join('resourses', name)
    try:
        return pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message) 
    
class Board:
    def __init__(self, tiles_size, size, tile_size, default_tile, tiles, collision = True):
        self.tiles_w = tiles_size[0]
        self.tiles_h = tiles_size[1]
        self.width = size[0]
        self.height = size[1]
        self.cell_size = tile_size
        self.collision = collision
        self.board = default_tile
        for i in range(self.tiles_w):
            for j in range(self.tiles_h):
                for m in tiles:
                    if (i,j)==m[0]:
                        self.board[i][j] = m[1]
                if isinstance(self.board[i][j],Block):
                    self.board[i][j].update_pos((i,j)) 
        print(self.board)
                                              
                        
    def check_collision(self,p1,p2):
        coords = self.get_cell(p1, p2)
        if coords!=None:
            if self.board[coords[0]][coords[1]]==None:
                return True
        return False
    
    def get_cell(self, w, h):
        if 0 < w < self.width and 0 < h < self.height:
            return (w//self.cell_size, h//self.cell_size )
    
    def load(self, group):
        for i in self.board:
            for j in i:
                if j!=None:
                    group.add(j)


class Block(pygame.sprite.Sprite):
    def __init__(self,type,pos=(0,0)):
        super().__init__()
        self.image = load_image(type)
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]*self.rect.width
        self.rect.y = pos[1]*self.rect.height 
        self.pos = pos
    def update_pos(self,pos):
        self.pos = pos
        self.rect.x = pos[0]*self.rect.width
        self.rect.y = pos[1]*self.rect.height  
        if self.rect.height>self.rect.width:
            self.rect.y = pos[1]*self.rect.width-self.rect.height+self.rect.width
        else:
            self.rect.y = pos[1]*self.rect.height     