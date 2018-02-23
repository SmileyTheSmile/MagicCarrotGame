import pygame,os
from math import sqrt
from tools import load_image, Explosion, HEIGHT, WIDTH

class Bullet(pygame.sprite.Sprite):
    def __init__(self, default_pos, pos):
        super().__init__()
        self.image = load_image('bullet1.png')
        self.rect = self.image.get_rect() 
        self.rect.topleft = default_pos[0], default_pos[1]
        self.speed = 10
        self.x = default_pos[0]
        self.y = default_pos[1]
        dx = pos[0] - self.rect.center[0]
        dy = -(pos[1] - self.rect.center[1])
        dz = sqrt(dx ** 2 + dy ** 2)
        self.speedx = dx/dz * self.speed
        self.speedy = dy/dz * self.speed
        
    def update(self, level, player, fx_group):
        destroy = False
        if 0 < self.x - 1 and self.x + 1 < WIDTH and 0 < self.y - 1 and self.y + 1 < HEIGHT:
            collided_walls = pygame.sprite.spritecollide(self, level, False)
            if len(collided_walls) != 0:
                collided = False
                for i in collided_walls:
                    if self.rect.colliderect(i.additional_rect):
                        destroy = True
                        if i.square:
                            fx_group.add(Explosion(self.rect.topleft, 'hit01.png', 1, 1, 2))
                        break
                            
        else:
            destroy = True
        if destroy:
            self.kill()
        else:
            self.rect.center = (self.rect.center[0] + self.speedx, self.rect.center[1] - self.speedy)
    
class Bullet_Group(pygame.sprite.Group):
    def __init__(self):
        super().__init__()  
        self.damage = 1
    
    def update(self, level, player, fx_group):
        for i in self.sprites():
            i.update(level, player, fx_group)
