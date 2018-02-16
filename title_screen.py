import pygame
from title_screen_tools import Particle, create_particles

def title_screen():
    delay = 0
    pygame.init()
    size = width, height = 500, 350
    screen = pygame.display.set_mode(size)
    screen_rect = (0,0,width,height)
    clock = pygame.time.Clock()
    running = True
    all_sprites = pygame.sprite.Group()
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False       
            if event.type == pygame.MOUSEBUTTONDOWN:
                create_particles(event.pos,all_sprites)
        screen.fill(pygame.Color("white"))
        if delay == 3:
            for i in all_sprites.sprites():
                i.update(screen_rect)
            delay = 0
        else:
            delay+=1
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(100)
        print(clock.get_fps())