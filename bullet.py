import pygame,os
from math import sqrt

def load_image(name, colorkey = None):
    fullname = os.path.join('resourses', name)
    try:
        return pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message) 

class Bullet(pygame.sprite.Sprite):
    def __init__(self,default_pos,pos):
        super().__init__()
        self.image = load_image('bullet1.png')
        self.rect = self.image.get_rect() 
        self.rect.x,self.rect.y = default_pos[0],default_pos[1]
        self.speed = 10
        self.x, self.y = default_pos[0],default_pos[1]
        dx = pos[0] - self.rect.center[0]
        dy = -(pos[1] - self.rect.center[1])
        dz = sqrt(dx**2 + dy**2)
        self.speedx = dx/dz * self.speed
        self.speedy = dy/dz * self.speed         
   
    def update(self,level):
        if 0 < self.rect.x-1 and self.rect.x+1 < 512 and 0 < self.rect.y-1 and self.rect.y+1 < 512:
            if not pygame.sprite.spritecollideany(self,level):
                self.rect.center = (self.rect.center[0] + self.speedx, self.rect.center[1] - self.speedy)
            else:
                self.kill()
        else:
            self.kill()                

class Bullet_Group(pygame.sprite.Group):
    def __init__(self):
        super().__init__()  
        self.damage = 10
    
    def update(self,level):
        for i in self.sprites():
            i.update(level)