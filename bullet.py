import pygame,os
from math import sqrt
from tools import load_image, Explosion

class Bullet(pygame.sprite.Sprite):
    def __init__(self, default_pos, pos):
        super().__init__()
        self.image = load_image('bullet1.png')
        self.rect = self.image.get_rect() 
        self.rect.topleft = default_pos[0], default_pos[1]
        self.speed = 10
        self.x, self.y = default_pos[0], default_pos[1]
        dx, dy = pos[0] - self.rect.center[0], -(pos[1] - self.rect.center[1])
        dz = sqrt(dx ** 2 + dy ** 2)
        self.speedx, self.speedy = dx/dz * self.speed, dy/dz * self.speed
        
    def update(self, level, player, fx_group):
        destroy = False
        if 0 < self.x - 1 and self.x + 1 < 512 and 0 < self.y-1 and self.y + 1 < 512:
            collided_walls = pygame.sprite.spritecollide(self, level, False)
            if len(collided_walls) != 0:
                collided = False
                for i in collided_walls:
                    if self.rect.colliderect(i.rect):
                        collided = True
                        break
                if collided:
                    if not pygame.sprite.collide_rect(player, collided_walls[0]):
                        fx_group.add(Explosion(self.rect.topleft, 'hit01.png', 1, 1, 2))
                        destroy = True
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
