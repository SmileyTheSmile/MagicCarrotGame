import os, random, pygame

SIZE = WIDTH, HEIGHT = 512, 512

def load_image(name, colorkey = None):
    fullname = os.path.join('resourses', name)
    try:
        return pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    
class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, pos, player, current_frame =  0):
        super().__init__()
        if player != True:
            if rows != 1 or columns != 1:
                self.oneframe = False
                self.frames = []
                self.rows = rows
                self.cols = columns
                self.current_frame = current_frame
                self.cut_sheet(sheet, columns, rows)
                if player != None:
                    self.image = self.frames[self.current_frame]
                else:
                    self.current_row = 0
                    self.image = self.frames[self.current_row][self.current_frame] 
                self.rect = self.rect.move(pos[0], pos[1])
            else: self.oneframe = True
                         
        else:
            self.current_frame = current_frame
            self.frames = {'right' : [], 'left' : [], 'down' : [], 'up' : []}
            self.cut_sheet(sheet, columns, rows)
            self.image = self.frames['right'][current_frame]    
            self.rect = self.rect.move(pos[0], pos[1])
        
    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect. w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(frame_location,self.rect.size)))

class Vegetable(AnimatedSprite):
    def __init__(self, pos, image, death_sound, hit_sound, rows, cols, health, speed, player):
        super().__init__(image, cols, rows, pos, player)
        self.w = self.rect.width
        self.h =  self.rect.height  
        self.death_sound = pygame.mixer.Sound('sound/' + death_sound)
        self.hit_sound = pygame.mixer.Sound('sound/' + hit_sound)
        self.health = health
        self.speed = speed

class Button(AnimatedSprite):
    def __init__(self, pos, image, text, color):
        super().__init__(load_image(image), 2, 1, pos, False)
        self.rect.center = self.rect.topleft
        self.clicking_sound = pygame.mixer.Sound('sound/buttonclick.wav') 
        self.text = text
        self.text_color = color
        pygame.font.init()
        self.font = pygame.font.Font('Pixeled.ttf', 16)
            
    def click(self):
        if self.current_frame == 0:
            self.clicking_sound.play()
            self.current_frame = 1
            if self.text_color[0] != 0:
                self.text_color[0] -= 32
        else:
            self.current_frame = 0
            if self.text_color[0] <= 223:
                self.text_color[0] += 32
        self.image = self.frames[self.current_frame]
        
    def draw_text(self, surface):
        self.rendered_text = self.font.render(self.text, 1, self.text_color)
        self.rendered_rect = self.rendered_text.get_rect(centerx = self.rect.centerx, centery = self.rect.centery - (self.rect.height // 8))
        surface.blit(self.rendered_text, self.rendered_rect)
        
    
class Bullet_Hole(AnimatedSprite):
    image = load_image('bullet_holes.png')
    def __init__(self, pos):
        super().__init__(Bullet_Hole.image, 4, 1, pos, False, random.choice(range(4)))
        self.rect.center = pos[0] + random.choice(range(5)), pos[1] + random.choice(range(5))

class Explosion(AnimatedSprite):
    def __init__(self, pos, image, rows, cols, delay = 0):
        super().__init__(load_image(image), cols, rows, pos, False)
        self.delay = 0
        self.maxdelay =  delay
        self.image = load_image(image)
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
                
    def update(self):
        if not self.oneframe:
            if self.current_frame != self.cols:
                self.image = self.frames[self.current_frame]
                self.current_frame += 1
            else:
                self.kill()
        else:
            if self.delay == self.maxdelay:
                self.kill()
            else:
                self.delay += 1
    

class Particle(AnimatedSprite):
    gibs = load_image('gibs.png')
    def __init__(self, pos, dx, dy):
        super().__init__(Particle.gibs, 4, 1, pos, False, random.choice(range(4)))
        self.v = [dx,dy]
        self.gravity = 1
        random_x = random.choice(range(5))
        random_y = random.choice(range(5))
        self.rect = self.rect.move(pos[0] + random_x, pos[1] + random_y)
        self.rect.topleft = pos
        
    def update(self, screen_rect):
        self.v[1] += self.gravity
        self.rect.topleft = self.rect.x + self.v[0], self.rect.y + self.v[1]
        if not self.rect.colliderect(screen_rect):
            self.kill()

def create_particles(position, group, particles_count):
    for i in range(particles_count):
        group.add(Particle(position, random.choice(range(-5, 6)), random.choice(range(-5,5))))