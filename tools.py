import os, random, pygame
from load_image import load_image
from player import Enemy
  
class Button(pygame.sprite.Sprite):
    def __init__(self, pos, image, text, color):
        super().__init__()
        self.frames = []
        self.cut_sheet(load_image(image),2,1)
        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.rect = self.rect.move(pos[0], pos[1])
        self.rect.center = self.rect.topleft
        self.clicking_sound = pygame.mixer.Sound('sound/buttonclick.wav') 
        self.text = text
        self.text_color = color
        pygame.font.init()
        self.font = pygame.font.Font('Pixeled.ttf', 16)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect. w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(frame_location,self.rect.size)))
            
    def click(self):
        self.clicking_sound.play()
        self.current_frame = 1
        self.image = self.frames[self.current_frame]
        if self.text_color[0] != 0:
            self.text_color[0] -= 32
        if self.text_color[1] != 0:
            self.text_color[1] -= 32
        if self.text_color[2] != 0:
            self.text_color[2] -= 32
    
    def unclick(self):
        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        if self.text_color[0] <= 223:
            self.text_color[0] += 32
        if self.text_color[1] <= 223:
            self.text_color[1] += 32
        if self.text_color[2] <= 223:
            self.text_color[2] += 32
        
    def draw_text(self,surface):
        self.rendered_text = self.font.render(self.text, 1, self.text_color)
        self.rendered_rect = self.rendered_text.get_rect(x = self.rect.x + 13, centery = self.rect.centery)
        surface.blit(self.rendered_text, self.rendered_rect)
    
class Enemy_Spawn(pygame.sprite.Group):
    def __init__(self, data):
        super().__init__()
        data = data.split("'")
        self.pos = (int(data[0]), int(data[1]))
        self.enemies_num = int(data[2])
    
    def spawn(self, group):
        if self.enemies_num != 0:
            group.add(Enemy(self.pos, "potato_enemy_01.png", 'explode1.wav', self))
            self.enemies_num -= 1
    def update(self, group):
        if len(self.sprites()) == 0:
            self.spawn(group)
        
    
class Bullet_Hole(pygame.sprite.Sprite):
    image = load_image('bullet_holes.png')
    def __init__(self, pos):
        super().__init__()
        self.frames = []
        self.cut_sheet(Bullet_Hole.image,4,1)
        self.current_frame = random.choice(range(4))
        self.image = self.frames[self.current_frame]
        self.rect = self.rect.move(pos[0] + random.choice(range(5)), pos[1] + random.choice(range(5)))
        self.rect.center = self.rect.topleft
        
    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect. w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(frame_location,self.rect.size)))

class Explosion(pygame.sprite.Sprite):
    def __init__(self, pos, image):
        super().__init__()
        self.frames = []
        self.cut_sheet(load_image(image), 10, 1)
        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.rect = self.rect.move(pos[0], pos[1])
        
    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // 10,
                                sheet.get_height())
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect. w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(frame_location,self.rect.size)))
                
    def update(self):
        if self.current_frame != 10:
            self.image = self.frames[self.current_frame]
            self.current_frame+=1
        else:
            self.kill()
    

class Particle(pygame.sprite.Sprite):
    gibs = load_image('gibs.png')
    def __init__(self, pos, dx, dy):
        super().__init__()
        self.frames = []
        self.cut_sheet(Particle.gibs,4,1)
        self.current_frame = random.choice(range(4))  
        self.image = self.frames[self.current_frame]
        self.rect = self.rect.move(pos[0] + random.choice(range(5)), pos[1] + random.choice(range(5)))
        self.v = [dx,dy]
        self.rect.x, self.rect.y = pos
        self.gravity = 1 
    
    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect. w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(frame_location,self.rect.size)))    
        
    def update(self, screen_rect):
        self.v[1] += self.gravity
        self.rect.x += self.v[0]
        self.rect.y += self.v[1]
        
        if not self.rect.colliderect(screen_rect):
            self.kill()

def create_particles(position, group):
    particles_count = 5
    numbers = range(-5, 6)
    for i in range(particles_count):
        group.add(Particle(position, random.choice(numbers), random.choice(numbers)))