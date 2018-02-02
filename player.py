import pygame,os

def load_image(name, colorkey = None):
    fullname = os.path.join('resourses', name)
    try:
        return pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)  
    
class Player(pygame.sprite.Sprite):
    image = load_image("player_standing01.png")
    def __init__(self, pos):
        super().__init__()
        self.image = Player.image
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[0]
        self.shooting = False 
        self.key = {'right':False, 'up':False, 'left':False, 'down':False}
        self.w,self.h=self.rect.width,self.rect.height
        
    def move(self,level):
        n1, n2 = self.rect.x, self.rect.y
        u1, u2, l1, l2, d1, d2, r1, r2=level.check_collision(n1,n2-2), level.check_collision(n1+self.w,n2-2), level.check_collision(n1-2,n2), level.check_collision(n1-2,n2+self.h), level.check_collision(n1,n2+self.h+2), level.check_collision(n1+self.w,n2+2+self.h), level.check_collision(n1+self.w+2,n2), level.check_collision(n1+self.w+2,n2+self.h)
        if self.key['up'] and not self.key['down']:
            if n2 - 2 > 0:
                if u1 and u2:
                    self.rect.y-=2
        if self.key['left'] and not self.key['right']:
            if n1 - 2 > 0:
                if l1 and l2:
                    self.rect.x-=2 
        if self.key['down'] and not self.key['up']:
            if n2 + 2 < level.height:
                if d1 and d2:
                    self.rect.y+=2
        if self.key['right'] and not self.key['left']:
            if n1 + 2 < level.width:
                if r1 and r2:
                    self.rect.x+=2 
        
        def move_b(self,level):
            n1, n2 = self.rect.x, self.rect.y
            if not pygame.sprite.spritecollideany(self, level):
                if self.key['up'] and not self.key['down']:
                    if n2 - 2 > 0:
                        self.rect.y-=2
                if self.key['left'] and not self.key['right']:
                    if n1 - 2 > 0:
                        self.rect.x-=2 
                if self.key['down'] and not self.key['up']:
                    if n2 + 2 < 512:
                        self.rect.y+=2
                if self.key['right'] and not self.key['left']:
                    if n1 + 2 < 512:
                        self.rect.x+=2         