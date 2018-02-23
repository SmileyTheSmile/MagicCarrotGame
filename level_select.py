import pygame, os, random
from tools import load_image, Particle, create_particles, Bullet_Hole, Button, SIZE, HEIGHT, WIDTH

def level_select():
    running = True 
    quit_game = False
    clicked = False
    
    level = None
    level_walls = None
    
    quit_delay = 0
    gibs_delay = 0

    pygame.init()
    screen = pygame.display.set_mode(SIZE)
    screen_rect = (0, 0, WIDTH, HEIGHT)
    clock = pygame.time.Clock()
    
    gun_shot = pygame.mixer.Sound('sound/pistol_shoot.wav')
    gun_shot.set_volume(0.5)
    
    background = pygame.sprite.GroupSingle()
    background_sprite = pygame.sprite.Sprite(background)
    background_sprite.image = load_image("level_menu.png")
    background_sprite.rect = background_sprite.image.get_rect()
    
    bullet_holes = pygame.sprite.Group()
    max_bullet_holes = 16
    
    gibs_sprites = pygame.sprite.Group()
    
    buttons = pygame.sprite.Group()
    level1_button = Button((256,148), 'button.png', '1 Уровень', [255, 255, 255])
    level2_button = Button((256,196), 'button.png', '2 Уровень', [255, 255, 255])
    level3_button = Button((256,244), 'button.png', '3 Уровень', [255, 255, 255])
    level4_button = Button((256,292), 'button.png', '4 Уровень', [255, 255, 255])    
    buttons.add(level1_button, level2_button, level3_button, level4_button)
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                quit_game = True     
            if event.type == pygame.MOUSEBUTTONDOWN:
                if level1_button.rect.collidepoint(event.pos):
                    level1_button.click()
                    clicked = True
                    level = 'level1.txt'
                    level_walls = 'level1_walls.txt'
                elif level2_button.rect.collidepoint(event.pos):
                    level2_button.click()
                elif level3_button.rect.collidepoint(event.pos):
                    level3_button.click()    
                elif level4_button.rect.collidepoint(event.pos):
                    level4_button.click()
                else:
                    if len(bullet_holes.sprites()) == max_bullet_holes:
                        bullet_holes.sprites()[random.choice(range(max_bullet_holes))].kill()                
                    bullet_holes.add(Bullet_Hole(event.pos))
                    gun_shot.play()
                    create_particles(event.pos, gibs_sprites, random.choice(range(4, 7)))
            if event.type == pygame.MOUSEBUTTONUP:
                if level1_button.rect.collidepoint(event.pos):
                    level1_button.click()
                elif level2_button.rect.collidepoint(event.pos):  
                    level2_button.click()
                elif level3_button.rect.collidepoint(event.pos):  
                    level3_button.click() 
                elif level4_button.rect.collidepoint(event.pos):  
                    level4_button.click()
        background.draw(screen)
        if gibs_delay == 2:
            for i in gibs_sprites.sprites():
                i.update(screen_rect)
            gibs_delay = 0
        else:
            gibs_delay += 1
        if clicked:
            if quit_delay == 10:
                running = False
            else:
                quit_delay += 1
        bullet_holes.draw(screen)
        buttons.draw(screen)
        level1_button.draw_text(screen)
        level2_button.draw_text(screen)
        level3_button.draw_text(screen)
        level4_button.draw_text(screen)        
        gibs_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(60)
        #print(clock.get_fps())
        gun_shot.stop
    pygame.mixer.music.stop()
    return quit_game, level, level_walls