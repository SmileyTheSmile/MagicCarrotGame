import os, random, pygame

def load_image(name, colorkey = None):
    fullname = os.path.join('resourses', name)
    try:
        return pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)

class Particle(pygame.sprite.Sprite):
    fire = [load_image('bullet1.png')]
    for scale in range(10):
        fire.append(pygame.transform.scale(fire[0], (scale, scale)))
    fire = fire[1:]
    def __init__(self, pos, dx, dy):
        super().__init__()
        self.image = random.choice(Particle.fire)
        self.rect = self.image.get_rect()
        self.v = [dx,dy]
        self.rect.x, self.rect.y = pos
        self.gravity = 1
        
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