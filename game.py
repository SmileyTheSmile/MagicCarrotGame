import pygame, os
from player import Player, Gun, Player_UI,UI_Element, Enemy, Enemies
from bullet import Bullet, Bullet_Group
from board import Board, Block
from tools import Explosion, Button, Enemy_Spawn
from load_image import load_image


def game(level, level_walls):
    clock = pygame.time.Clock()
    pygame.init()
    SIZE = WIDTH, HEIGHT = 512, 512
    screen = pygame.display.set_mode(SIZE)
    running = True
    frame_delay = 3
    level_spawns = []
    for i in level[0][2]:
        level_spawns.append(Enemy_Spawn(i))
    max_delay = 3
    tile_size = 32
    tile_number_w = int(WIDTH / tile_size)
    tile_number_h = int(HEIGHT / tile_size)
    try_again = True
    first_win = True
    pygame.mixer.init()  
    pygame.mixer.set_num_channels(24)
    
    pygame.mixer.music.load('music/gameplay_music.mp3')
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1) 
    
    end_screen_loss_sound = pygame.mixer.Sound('sound/loss.wav')
    end_screen_victory_sound = pygame.mixer.Sound('sound/victory.wav')
    
    gun_shot = pygame.mixer.Sound('sound/ak_shoot.wav')
    gun_shot.set_volume(0.75)    
    
    board = Board((tile_number_w, tile_number_h), SIZE, tile_size, [[Block(level[0][0], (i, j)) for i in range(tile_number_h)] for j in range(tile_number_w)], level[1], level[1])
    
    board_collision = Board((tile_number_w, tile_number_h), SIZE, tile_size,[[None for i in range(tile_number_h)] for j in range(tile_number_w)],level_walls[1])
    
    #Игрок
    player_default_pos = list(map(int, level[0][1].split("'")))
    player = Player(player_default_pos)
    player_sprites = pygame.sprite.GroupSingle()
    player_gun_sprite = Gun(player_default_pos)
    player_gun = pygame.sprite.GroupSingle()
    player_gun.add(player_gun_sprite) 
    player_sprites.add(player)
    player_first_death = True
    
    #Меню игрока
    player_ui = pygame.sprite.GroupSingle()
    player_health = Player_UI()
    player_ui.add(UI_Element((0,0),'ui_frame.png'))    
    
    #Уровень
    level_tiles_sprites = pygame.sprite.Group()
    level_walls = pygame.sprite.Group()
    board.load(level_tiles_sprites)
    board_collision.load(level_walls)    
    fx_sprites = pygame.sprite.Group()
    
    bullet_sprites = Bullet_Group()
    
    #Враги
    enemies = Enemies()
    
    end_screen = pygame.sprite.GroupSingle()
    end_sprite = pygame.sprite.Sprite(end_screen)
    end_sprite.image = load_image("end_screen.png")
    end_sprite.rect = end_sprite.image.get_rect()  
    end_sprite.rect.x = end_sprite.rect.x + (WIDTH // 2) - (end_sprite.rect.width // 2)
    game_over = False
    
    victory_screen = pygame.sprite.GroupSingle()
    victory_sprite = pygame.sprite.Sprite(victory_screen)
    victory_sprite.image = load_image("victory_screen.png")
    victory_sprite.rect = victory_sprite.image.get_rect()  
    victory_sprite.rect.topleft = (victory_sprite.rect.x + (WIDTH // 2) - (victory_sprite.rect.width // 2),victory_sprite.rect.y) 
    victory = False
    
    finale_buttons = pygame.sprite.Group()
    yes_button = Button((WIDTH // 2, 320), 'button.png', 'Дааааааа', [255, 255, 255])
    no_button = Button((WIDTH // 2, 416), 'button.png', 'Не,мне лень', [255, 255, 255])
    finale_buttons.add(yes_button, no_button)
            
    click_pos = (0,0)
    looking_pos = (0,0)
    
    def draw_everything():
        level_tiles_sprites.draw(screen)
        fx_sprites.draw(screen)
        if render_order:
            player_sprites.draw(screen)
            bullet_sprites.draw(screen)
            player_gun.draw(screen)
            level_walls.draw(screen)
        else:
            level_walls.draw(screen)  
            player_sprites.draw(screen) 
            bullet_sprites.draw(screen)
            player_gun.draw(screen)
        enemies.draw(screen)
        player_ui.draw(screen)
        player_health.draw(screen)  
    
    for i in level_spawns:
        i.spawn(enemies)    
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                try_again = False
            if event.type == pygame.KEYDOWN:
                if event.key == 119:
                    player.key['up'] = True
                if event.key == 97:
                    player.key['left'] = True   
                if event.key == 115:
                    player.key['down'] = True
                if event.key == 100:
                    player.key['right'] = True               
            if event.type == pygame.KEYUP:
                if event.key == 119:
                    player.key['up'] = False
                if event.key == 97:
                    player.key['left'] = False   
                if event.key == 115:
                    player.key['down'] = False
                if event.key == 100:
                    player.key['right'] = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if victory or game_over:
                    if yes_button.rect.collidepoint(event.pos):
                        yes_button.click()
                        end_screen_victory_sound.stop()
                        end_screen_loss_sound.stop()
                        running = False
                    elif no_button.rect.collidepoint(event.pos):
                        no_button.click()
                        try_again = False
                        end_screen_victory_sound.stop()
                        end_screen_loss_sound.stop()
                        running = False
                    
                else:
                    player.shooting = True
                    click_pos = event.pos                        
            if event.type == pygame.MOUSEMOTION:
                if player.shooting:
                    click_pos = event.pos
                looking_pos = event.pos
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                player.shooting = False                  
        
        if player.health != 0 and len(enemies.sprites()) != 0:
            if player.shooting:
                bullet_sprites.add(Bullet((player_gun_sprite.rect.center[0], player_gun_sprite.rect.center[1] - 4), click_pos)) 
                gun_shot.play()
            render_order = player.move(board_collision)
            if frame_delay == max_delay:
                player.update(player.current_dir)
                frame_delay = 0
            else:
                frame_delay += 1
            enemies.update(player.rect.center, level_walls, bullet_sprites, player)
            player_health.get_stats(player)
            player_gun.sprite.update(looking_pos, player)
            for i in enemies.sprites():
                if i.killed:
                    fx_sprites.add(Explosion(i.rect.topleft, 'explosion02.png'))
                    i.kill()
            for i in level_spawns:
                i.update(enemies)
        else:
            if player.health == 0:
                if player_first_death:
                    game_over = True
                    fx_sprites.add(Explosion(player.rect.topleft, 'explosion01.png'))
                    player.kill()
                    player_gun_sprite.kill()
                    player_first_death = False
                    for i in enemies.sprites():
                        fx_sprites.add(Explosion(i.rect.topleft, 'explosion02.png'))
                        i.kill()    
                    pygame.mixer.music.stop()
                    end_screen_loss_sound.play()  
            elif len(enemies.sprites()) == 0:
                if first_win:
                    victory = True
                    pygame.mixer.music.stop()
                    end_screen_victory_sound.play() 
                    first_win = False
        bullet_sprites.update(level_walls, player)
        fx_sprites.update()
            
        draw_everything()
        if game_over or victory:
            if game_over:
                end_screen.draw(screen)
            if victory:
                victory_screen.draw(screen)
            finale_buttons.draw(screen)
            yes_button.draw_text(screen)
            no_button.draw_text(screen)
            
        clock.tick(30)
        #print(clock.get_fps())
        pygame.display.flip()
    pygame.mixer.music.stop()
    return try_again
