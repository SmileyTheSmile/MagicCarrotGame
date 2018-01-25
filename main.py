import pygame
from math import atan2, degrees, pi

class Board:
    def __init__(self, width, height, tiles=[]):
        self.width = width
        self.height = height
        self.cell_size = 32
        self.board = [[Block((i,j),(0,200,0),0) for i in range(width)] for j in range(height)]
        for i in range(self.width):
            for j in range(self.height):
                for m in tiles:
                    if m.pos == (i,j):
                        self.board[i][j]=m
    
    def get_cell(self, w, h):
        if 0 < w < width and 0 < h < height:
            return (w//self.cell_size, h//self.cell_size )
        else:
            return None
    
    def check_collision(self,p1,p2):
        p=self.get_cell(p1,p2)
        if p!= None:
            if self.board[p[0]][p[1]].collision==0:
                return True
        return False
    
    def render(self):
        for i in range(self.width):
            for j in range(self.height):
                pygame.draw.rect(screen, self.board[i][j].type, (self.cell_size * i, self.cell_size * j, self.cell_size, self.cell_size), 0)


class Block:
    def __init__(self, pos, type, collision):
        self.pos = pos
        self.type = type
        self.collision = collision

class Player:
    def __init__(self, pos):
        self.pos = pos
        self.rot = 0
        self.screen = pygame.display.set_mode(size)
        
    def move(self):
        n1, n2 = self.pos[0], self.pos[1]
        if keys['up'] and not keys['down']:
            if n2 - 1 > 0:
                if board.check_collision(n1,n2-1) and board.check_collision(n1+16,n2-1):
                    self.pos[1]-=1
        if keys['left'] and not keys['right']:
            if n1 - 1 > 0:
                if board.check_collision(n1-1,n2) and board.check_collision(n1-1,n2+16):
                    self.pos[0]-=1 
        if keys['down'] and not keys['up']:
            if n2 + 1 < height:
                if board.check_collision(n1,n2+17) and board.check_collision(n1+16,n2+17):
                    self.pos[1]+=1
        if keys['right'] and not keys['left']:
            if n1 + 1 < width:
                if board.check_collision(n1+17,n2) and board.check_collision(n1+17,n2+16):
                    self.pos[0]+=1
    
    def render(self):
        pygame.draw.rect(self.screen, (255,0,0), (self.pos[0],self.pos[1],16,16), 0)
        screen.blit(self.screen,(0,0))
        
class Bullet:
    def __init__(self):
        self.shot = False
        self.pos = [0,0]
        self.moving_dir = 3
        self.screen = pygame.display.set_mode(size)
    
    def change_default_pos(self,pos):
        self.pos = [pos[0]+8,pos[1]+8]
    def shoot(self):
        self.shot = True
        self.x = 0
        self.y = 0
        if keys['right']:
            self.x+=2
        if keys['down']:
            self.y+=2  
        if keys['left']:
            self.x-=2
        if keys['up']:
            self.y-=2
    
    def move(self):
        self.pos[0]+=self.x
        self.pos[1]+=self.y
            
    def render(self):
        pygame.draw.circle(self.screen, pygame.Color('yellow'), self.pos, 4)


#---------------------------------

clock=pygame.time.Clock()
pygame.init()
size = width, height = 512, 512
screen = pygame.display.set_mode(size)
running = True
keys = {'right':False, 'up':False, 'left':False, 'down':False}
bullets1=[Bullet() for i in range(32)]
board = Board(16, 16,
              [Block((7,7),pygame.Color('green'),1)])
player = Player([257,257])
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key==119:
                keys['up']=True
            if event.key==97:
                keys['left']=True   
            if event.key==115:
                keys['down']=True
            if event.key==100:
                keys['right']=True  
            if event.key == 109:
                for i in bullets1:
                    if not i.shot:
                        i.shoot()     
                        break                    
        if event.type == pygame.KEYUP:
            if event.key==119:
                keys['up']=False
            if event.key==97:
                keys['left']=False   
            if event.key==115:
                keys['down']=False
            if event.key==100:
                keys['right']=False          
    player.move()
    screen.fill((0, 0, 200))
    board.render()
    player.render()
    for i in bullets1:
        if i.shot:  
            if 0 < i.pos[0]-1 and i.pos[0]+1 < height and 0 < i.pos[1]-1 and i.pos[1]+1 < height:
                i.move()
                i.render()
            else:       
                i.shot = False
        else:
            i.change_default_pos(player.pos)         
    clock.tick(100)
    pygame.display.flip()
pygame.quit()