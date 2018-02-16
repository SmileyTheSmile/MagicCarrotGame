import pygame
from player import Player,Gun,Player_UI,UI_Element,Enemy,Enemies
from bullet import Bullet,Bullet_Group
from board import Board, Block

def load_image(name, colorkey = None):
    fullname = os.path.join('resourses', name)
    try:
        return pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    
clock = pygame.time.Clock()
pygame.init()
SIZE = WIDTH, HEIGHT = 512, 512
screen = pygame.display.set_mode(SIZE)
running = True
frame_delay = 2
max_delay = 2

board = Board((16, 16), SIZE, 32, [[Block('grass1.png',(i,j)) for i in range(16)] for j in range(16)],
              [((0,3),None),
               ((1,3),None),
               ((2,3),None),
               ((4,3),None),
               ((5,3),None),
               ((6,3),None),
               ((7,3),None),
               ((0,5),None),
               ((1,5),None),
               ((2,5),None),
               ((4,5),None),
               ((5,5),None),
               ((6,5),None),
               ((7,5),None)])

board_collision = Board((16, 16), SIZE, 32,[[None for i in range(16)] for j in range(16)],
                        [((0,3),Block('barn_wood_01.png')),
                         ((1,3),Block('barn_wood_01.png')),
                         ((2,3),Block('barn_wood_01.png')),
                         ((4,3),Block('barn_wood_01.png')),
                         ((5,3),Block('barn_wood_01.png')),
                         ((6,3),Block('barn_wood_01.png')),
                         ((7,3),Block('barn_wood_01.png')),
                         ((0,5),Block('barn_wood_01.png')),
                         ((1,5),Block('barn_wood_01.png')),
                         ((2,5),Block('barn_wood_01.png')),
                         ((4,5),Block('barn_wood_01.png')),
                         ((5,5),Block('barn_wood_01.png')),
                         ((6,5),Block('barn_wood_01.png')),
                         ((7,5),Block('barn_wood_01.png'))])
player_default_pos=(200,200)

player = Player(player_default_pos)
level_tiles_sprites=pygame.sprite.Group()
level_walls = pygame.sprite.Group()
player_sprites=pygame.sprite.GroupSingle()
bullet_sprites=Bullet_Group()
player_gun = pygame.sprite.GroupSingle()
player_gun.add(Gun(player_default_pos))

player_ui = Player_UI()
player_health_and_ammo = Player_UI()
player_heart1 = UI_Element((30,28),'player_heart.png')
player_heart2 = UI_Element((50,28),'player_heart.png')
player_heart3 = UI_Element((70,28),'player_heart.png')
player_ui_sprite = UI_Element((0,0),'ui_frame.png')
player_health_and_ammo.add(player_heart1)
player_health_and_ammo.add(player_heart2)
player_health_and_ammo.add(player_heart3)
player_ui.add(player_ui_sprite)

enemies=Enemies()
enemies.add(Enemy((200,200),"potato_enemy_02.png"))

player_sprites.add(player)
board.load(level_tiles_sprites)
board_collision.load(level_walls)
click_pos = (0,0)
looking_pos = (0,0)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key==119:
                player.key['up']=True
            if event.key==97:
                player.key['left']=True   
            if event.key==115:
                player.key['down']=True
            if event.key==100:
                player.key['right']=True               
        if event.type == pygame.KEYUP:
            if event.key==119:
                player.key['up']=False
            if event.key==97:
                player.key['left']=False   
            if event.key==115:
                player.key['down']=False
            if event.key==100:
                player.key['right']=False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            player.shooting = True
            click_pos = event.pos
        if event.type == pygame.MOUSEMOTION:
            if player.shooting:
                click_pos = event.pos
            looking_pos = event.pos
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            player.shooting = False  
    if player.shooting:
        bullet_sprites.add(Bullet(player.rect.center,click_pos))      
    bullet_sprites.update(level_walls) 
    render_order = player.move(board_collision)
    if frame_delay == max_delay:
        player.update(player.current_dir)
        frame_delay = 0
    else:
        frame_delay += 1
    enemies.update(player.rect.center,board_collision,bullet_sprites)
    #player_gun.sprite.update(looking_pos,player)
    level_tiles_sprites.draw(screen)
    bullet_sprites.draw(screen)
    if render_order:
        player_sprites.draw(screen)
        level_walls.draw(screen)
    else:
        level_walls.draw(screen)  
        player_sprites.draw(screen)  
    enemies.draw(screen)
    player_gun.draw(screen)
    player_ui.draw(screen)
    player_health_and_ammo.draw(screen)
    clock.tick(100)
    print(clock.get_fps())
    pygame.display.flip()
pygame.quit()

#https://gamedev.stackexchange.com/questions/75530/how-do-i-make-a-sprite-move-to-another-position-using-vectors
#https://stackoverflow.com/questions/46697502/how-to-move-a-sprite-according-to-an-angle-in-pygame