import pygame,os,math
from bullet import Bullet
def load_image(name, colorkey = None):
    fullname = os.path.join('resourses', name)
    try:
        return pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)  

def calc_angle(mypos,pos):
    myX,myY,targetX,targetY = mypos[0],mypos[1],pos[0],pos[1]
    if(myX > targetX):
        dx = myX - targetX
    else:
        dx = targetX - myX 
    if(myY > targetY):
        dy = myY - targetY
    else:
        dy = targetY - myY

    if(dy == 0):
        dy = 1
    if(dx == 0):
        dx = 1

    #Calc Movement
    if(dx > dy):
        Speedy = dy/dx 
        Speedx = 1
    if(dx < dy):
        Speedy = 1
        Speedx = dx/dy
    elif(dx == dy):
        Speedx = 1
        Speedy = 1

    if(myX > targetX):
        Speedx = Speedx * -1
    if(myY > targetY):
        Speedy = Speedy * -1


    return Speedx,Speedy

class Player(pygame.sprite.Sprite):
    image = load_image("player01.png")
    def __init__(self, pos):
        super().__init__()
        self.image = Player.image
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.shooting = False 
        self.key = {'right':False, 'up':False, 'left':False, 'down':False}
        self.w,self.h=self.rect.width,self.rect.height
        
    def move(self,level):
        n1, n2 = self.rect.x, self.rect.y
        order = True
        u1, u2, l1, d1, d2, r1=level.check_collision(n1,n2+self.h-2), level.check_collision(n1+self.w,n2+self.h-2),level.check_collision(n1-2,n2+self.h), level.check_collision(n1,n2+self.h+2),level.check_collision(n1+self.w,n2+2+self.h), level.check_collision(n1+self.w+2,n2+self.h)
        if self.key['up'] and not self.key['down']:
            if n2 - 2 > 0:
                if u1 and u2:
                    self.rect.y-=2
        if self.key['left'] and not self.key['right']:
            if n1 - 2 > 0:
                if l1:
                    self.rect.x-=2 
        if self.key['down'] and not self.key['up']:
            if n2 + 2 < level.height:
                if d1 and d2:
                    self.rect.y+=2         
        if self.key['right'] and not self.key['left']:
            if n1 + 2 < level.width:
                if r1:
                    self.rect.x+=2 
        player_pos = level.get_cell(n1, n2+self.rect.height) 
        l1, u1, r1 = player_pos[0]-1, player_pos[1]-1, player_pos[0]+1
        if r1+1<=len(level.board[0]) and l1+1<=len(level.board[0]):
            if level.board[l1][u1]!=None or level.board[r1][u1]!=None or level.board[player_pos[0]][u1]!=None:
                order = False
        return order
    #def animate(self):
        #self.
    
class Gun(pygame.sprite.Sprite):
    image_gun = load_image("ak43.png")
    def __init__(self,pos):
        super().__init__()
        self.image = Gun.image_gun
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.angle = 0
        self.rect.y = pos[1]        
    def get_angle(self, destination):
        x_dist = destination[0] - self.rect.center[0]
        y_dist = destination[1] - self.rect.center[1]
        return atan2(-y_dist, x_dist) % (2 * pi)   
    def update(self,pos,player):
        self.image = pygame.transform.rotate(self.image,self.get_angle(pos))
        self.rect.center = player.rect.center[0], player.rect.center[1]

class UI_Element(pygame.sprite.Sprite):
    def __init__(self, pos, image):
        super().__init__()
        self.image = load_image(image)
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]   
          

class Player_UI(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.health = 3
        self.ammo = 50         
    
    def update(self,health,ammo):
        self.health = health
        self.ammo = ammo     
    
    def draw_values(self,screen):
        pass
               
class Enemies(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.health = 3
        self.ammo = 50         
    
    def update(self,player_pos):
        for i in self.sprites():
            i.move(player_pos)

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos,image):
        super().__init__()
        self.image = load_image(image)
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.speed = 10
        self.shooting = False 
        self.key = {'right':False, 'up':False, 'left':False, 'down':False}
        self.w,self.h=self.rect.width,self.rect.height     
        
    def move(self,player_pos):
        speedx,speedy = calc_angle(self.rect.center,player_pos)
        self.rect.center = (self.rect.center[0] + speedx, self.rect.center[1] + speedy)         