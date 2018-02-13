import pygame
from player import Player,Gun,Player_UI,UI_Element,Enemy,Enemies
from bullet import Bullet,Bullet_group
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
bullet_delay = 10

board = Board((16, 16), SIZE, 32, [[Block('grass1.png',(i,j)) for i in range(16)] for j in range(16)],
              [((2,4),None),((2,3),None),((2,2),None),((2,1),None),
               ((1,4),None),((1,3),None),((1,2),None),((1,1),None)])

board_collision = Board((16, 16), SIZE, 32,[[None for i in range(16)] for j in range(16)],
                        [((1,4),Block('stone2.png')),((2,4),Block('stone2.png')),((3,4),Block('barn_wood_01.png')),((2,9),Block('stone2.png'))])
player_default_pos=(260,260)

player = Player(player_default_pos)
level_tiles_sprites=pygame.sprite.Group()
level_walls = pygame.sprite.Group()
player_sprites=pygame.sprite.GroupSingle()
bullet_sprites=Bullet_group(32)
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
enemies.add(Enemy((100,100),"potato_enemy_01.png"))
enemies.add(Enemy((400,400),"potato_enemy_01.png"))
enemies.add(Enemy((200,200),"potato_enemy_01.png"))

for i in range(32):
    bullet_sprites.add(Bullet((260,260)))
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
        for i in bullet_sprites:
            if not i.shot:  
                i.shoot(click_pos)
                bullet_delay = 0
                break       
    bullet_sprites.update(player,level_walls,click_pos)     
    render_order = player.move(board_collision)
    enemies.update(player.rect.center)
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
    #player_gun.draw(screen)
    player_ui.draw(screen)
    player_health_and_ammo.draw(screen)
    clock.tick(100)
    print(clock.get_fps())
    pygame.display.flip()
pygame.quit()

#https://gamedev.stackexchange.com/questions/75530/how-do-i-make-a-sprite-move-to-another-position-using-vectors