import pygame, os
from player import Player, Gun, Player_UI,UI_Element, Enemy, Enemies, Enemy_Spawn
from bullet import Bullet, Bullet_Group
from board import Board, Block
from tools import load_image, Explosion, Button, SIZE, HEIGHT, WIDTH

def game(level, level_walls_group):
    clock = pygame.time.Clock()
    pygame.init()
    screen = pygame.display.set_mode(SIZE)
    
    frame_delay = 3
    max_delay = 3
    tile_size = 32
    tile_number_w = int(WIDTH / tile_size)
    tile_number_h = int(HEIGHT / tile_size)
    
    try_again = True
    first_win = True
    quit =  False
    running = True

    pygame.mixer.init()  
    pygame.mixer.set_num_channels(60)
    
    pygame.mixer.music.load('music/gameplay_music.mp3')
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1) 
    
    end_screen_loss_sound = pygame.mixer.Sound('sound/loss.wav')
    end_screen_victory_sound = pygame.mixer.Sound('sound/victory.wav')
    
    gun_shot = pygame.mixer.Sound('sound/ak_shoot.wav')
    gun_shot.set_volume(0.75)    
    
    board = Board((tile_number_w, tile_number_h), SIZE, tile_size, [[Block(level[0][0], (i, j)) for i in range(tile_number_h)] for j in range(tile_number_w)], level[1], level[1])
    
    board_collision = Board((tile_number_w, tile_number_h), SIZE, tile_size,[[None for i in range(tile_number_h)] for j in range(tile_number_w)],level_walls_group[1])
    
    #Игрок
    player_default_pos = list(map(int, level[0][1].split("'")))
    player = Player(player_default_pos, load_image("player_sprites.png"), 'player_death.wav', 'damage_player01.wav', 4, 9, 3, 2)
    player_sprites = pygame.sprite.GroupSingle()
    player_gun_sprite = Gun(player_default_pos)
    player_gun = pygame.sprite.GroupSingle()
    player_gun.add(player_gun_sprite) 
    player_sprites.add(player)
    player_first_death = True
    
    player_ui = pygame.sprite.GroupSingle()
    player_health = Player_UI()
    player_ui.add(UI_Element((0,0),'ui_frame.png'))    
    
    level_tiles_sprites = pygame.sprite.Group()
    level_walls_group = pygame.sprite.Group()
    board.load(level_tiles_sprites)
    board_collision.load(level_walls_group)    
    fx_sprites = pygame.sprite.Group()
    
    bullet_sprites = Bullet_Group()
    
    level_spawns = []
    enemies = Enemies()
    for i in level[0][2]:
        level_spawns.append(Enemy_Spawn(i))  
    for i in level_spawns:
        i.spawn(enemies)    
    
    end_screen = pygame.sprite.GroupSingle()
    end_sprite = pygame.sprite.Sprite(end_screen)
    end_sprite.image = load_image("end_screen.png")
    end_sprite.rect = end_sprite.image.get_rect()  
    end_sprite.rect.x = end_sprite.rect.x + (WIDTH // 2) - (end_sprite.rect.width // 2)
    
    victory_screen = pygame.sprite.GroupSingle()
    victory_sprite = pygame.sprite.Sprite(victory_screen)
    victory_sprite.image = load_image("victory_screen.png")
    victory_sprite.rect = victory_sprite.image.get_rect()  
    victory_sprite.rect.topleft = (victory_sprite.rect.x + (WIDTH // 2) - (victory_sprite.rect.width // 2),victory_sprite.rect.y) 
    
    victory = False
    game_over = False
    
    finale_buttons = pygame.sprite.Group()
    yes_button = Button((WIDTH // 2, 320), 'button.png', 'Дааааааа', [255, 255, 255])
    no_button = Button((WIDTH // 2, 376), 'button.png', 'Не,мне лень', [255, 255, 255])
    finale_buttons.add(yes_button, no_button)
            
    click_pos = (0,0)
    looking_pos = (0,0)
    
    def draw_everything():
        level_tiles_sprites.draw(screen)
        if render_order:
            bullet_sprites.draw(screen)
            player_sprites.draw(screen)
            player_gun.draw(screen)
            level_walls_group.draw(screen)
        else:
            bullet_sprites.draw(screen)
            level_walls_group.draw(screen)  
            player_sprites.draw(screen) 
            player_gun.draw(screen)
        enemies.draw(screen)
        fx_sprites.draw(screen)
        player_ui.draw(screen)
        player_health.draw(screen)   
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                try_again = False
                quit = True
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
            enemies.update(player.rect.center, level_walls_group, bullet_sprites, player)
            player_health.get_stats(player)
            player_gun.sprite.update(looking_pos, player)
            for i in enemies.sprites():
                if i.killed:
                    fx_sprites.add(Explosion(i.rect.topleft, 'explosion02.png', 1, 10))
                    i.kill()                
                elif i.hit:
                    fx_sprites.add(Explosion(i.hitpoint, 'hit02.png', 1, 1, 2))
                    i.hit = False
            for i in level_spawns:
                i.update(enemies)
        else:
            if player.health == 0:
                if player_first_death:
                    game_over = True
                    player_first_death = False
                    player.death_sound.play()
                    fx_sprites.add(Explosion(player.rect.topleft, 'explosion01.png', 1, 10))
                    player.kill()
                    player_gun_sprite.kill()
                    for i in enemies.sprites():
                        fx_sprites.add(Explosion(i.rect.topleft, 'explosion02.png', 1, 10))
                        i.kill()    
                    pygame.mixer.music.stop()
                    end_screen_loss_sound.play()  
            elif len(enemies.sprites()) == 0:
                if first_win:
                    victory, first_win  = True, False
                    pygame.mixer.music.stop()
                    end_screen_victory_sound.play() 
        bullet_sprites.update(level_walls_group, player, fx_sprites)
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
    return try_again, quit
