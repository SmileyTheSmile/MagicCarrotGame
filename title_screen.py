import pygame, os, random
from tools import Particle, create_particles, Bullet_Hole, Button
from load_image import load_image


def title_screen():
    delay = 0
    pygame.init()
    size = width, height = 512, 512
    screen = pygame.display.set_mode(size)
    screen_rect = (0,0,width,height)
    clock = pygame.time.Clock()
    quit_game = False
    clicked = False
    quit_delay = 0
    running = True
    
    pygame.mixer.music.load('music/menu_music.mp3')
    pygame.mixer.music.set_volume(0.25)
    pygame.mixer.music.play(-1)  
    
    gun_shot = pygame.mixer.Sound('sound/pistol_shoot.wav')
    gun_shot.set_volume(0.5)
    
    background = pygame.sprite.GroupSingle()
    background_sprite = pygame.sprite.Sprite(background)
    background_sprite.image = load_image("main_menu.png")
    background_sprite.rect = background_sprite.image.get_rect()
    
    bullet_holes = pygame.sprite.Group()
    max_bullet_holes = 16
    
    gibs_sprites = pygame.sprite.Group()
    
    buttons = pygame.sprite.Group()
    start_game_button = Button((256,320), 'button.png', 'Начать игру', [255, 255, 255])
    quit_button = Button((256,448), 'button.png', 'Выйти', [240, 0, 0])
    buttons.add(start_game_button, quit_button)
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                quit_game = True     
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_game_button.rect.collidepoint(event.pos):
                    start_game_button.click()
                    clicked = True
                elif quit_button.rect.collidepoint(event.pos):
                    quit_button.click()
                    clicked = True
                    quit_game = True
                else:
                    if len(bullet_holes.sprites()) == max_bullet_holes:
                        bullet_holes.sprites()[random.choice(range(max_bullet_holes))].kill()                
                    bullet_holes.add(Bullet_Hole(event.pos))
                    gun_shot.play()
                    create_particles(event.pos,gibs_sprites)
            if event.type == pygame.MOUSEBUTTONUP:
                if start_game_button.rect.collidepoint(event.pos):
                    start_game_button.unclick()
                elif quit_button.rect.collidepoint(event.pos):  
                    quit_button.unclick()
        background.draw(screen)
        if delay == 2:
            for i in gibs_sprites.sprites():
                i.update(screen_rect)
            delay = 0
        else:
            delay += 1
        if clicked:
            if quit_delay == 10:
                running = False
            else:
                quit_delay += 1
        bullet_holes.draw(screen)
        buttons.draw(screen)
        start_game_button.draw_text(screen)
        quit_button.draw_text(screen)
        gibs_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(60)
        #print(clock.get_fps())
        gun_shot.stop
    pygame.mixer.music.stop()
    return quit_game