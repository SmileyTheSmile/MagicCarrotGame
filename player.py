import pygame,os,math
from bullet import Bullet
from load_image import load_image
from pygame.math import Vector2

class Player(pygame.sprite.Sprite):
    image = load_image("player_sprites.png")
    def __init__(self, pos):
        super().__init__()
        self.frames = {'right' : [], 'left' : [], 'down' : [], 'up' : []}
        self.cut_sheet(Player.image, 9, 4)        
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.current_frame = 0
        self.health = 3
        self.shooting = False         
        self.death_sound = pygame.mixer.Sound('sound/damage_player01.wav')       
        self.image = self.frames['right'][self.current_frame]
        self.rect = self.rect.move(20,38)
        self.current_dir = 'right'
        self.key = {'right':False, 'up':False, 'left':False, 'down':False}
        self.w, self.h = self.rect.width, self.rect.height
        
    def move(self, level):
        order = False
        n1, n2 = self.rect.x, self.rect.y
        if not self.key['up'] and not self.key['down'] and not self.key['right'] and not self.key['left']:
            self.current_frame = -1
        else:
            up1 = level.check_collision(n1,n2+self.h-2)
            up2 = level.check_collision(n1+self.w,n2+self.h-2)
            left1 = level.check_collision(n1-2,n2+self.h)
            down1 = level.check_collision(n1,n2+self.h+2)
            down2 = level.check_collision(n1+self.w,n2+2+self.h)
            right1 = level.check_collision(n1+self.w+2,n2+self.h)            
            if self.key['up'] and not self.key['down']:
                if n2 - 2 > 0:
                    if up1 and up2:
                        self.rect.y -= 2
                self.current_dir = 'up'
            if self.key['left'] and not self.key['right']:
                if n1 - 2 > 0:
                    if left1:
                        self.rect.x -= 2 
                self.current_dir = 'left'
            if self.key['down'] and not self.key['up']:
                if n2 + 2 < level.height:
                    if down1 and down2:
                        self.rect.y += 2    
                self.current_dir = 'down'
            if self.key['right'] and not self.key['left']:
                if n1 + 2 < level.width:
                    if right1:
                        self.rect.x += 2 
                self.current_dir = 'right'
            player_pos = level.get_cell(n1, n2+self.h) 
        player_pos = level.get_cell(n1, n2 + self.h) 
        up1 = player_pos[1] - 1
        up2 = player_pos[1] - 2
        right1 = player_pos[0] + 1
        right2 = player_pos[0] + 2
        left1 = player_pos[0] - 1
        left2 = player_pos[0] - 2

        if right2 + 1 <= len(level.board[0]) and left2 + 1 <= len(level.board[0]) and up2 + 1 <= len(level.board[1]):
            if level.board[player_pos[0]][up1] == None and level.board[player_pos[0]][up2] == None and level.board[right1][up1] == None and level.board[right2][up2] == None and level.board[left1][up1] == None and level.board[left2][up2] == None:
                order = True
            else:
                if level.board[right1][player_pos[1]] != None:
                    if level.board[right1][player_pos[1]].square and level.board[player_pos[0]][player_pos[1] + 1] != None:
                        order = True                    
                elif level.board[left1][player_pos[1]] != None:
                    if level.board[left1][player_pos[1]].square and level.board[player_pos[0]][player_pos[1] + 1] != None:
                        if level.board[player_pos[0]][player_pos[1] + 1].square:
                            order = True
        return order        
    
    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
        sheet.get_height() // rows)
        keys = ['right', 'left', 'down', 'up']
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect. w * i, self.rect.h * j)
                self.frames[keys[j]].append(sheet.subsurface(pygame.Rect(frame_location,self.rect.size)))  
                
    def update(self, key):
        self.current_frame = (self.current_frame + 1) % len(self.frames[key])
        self.image = self.frames[key][self.current_frame]    
    
class Gun(pygame.sprite.Sprite):
    image_gun = load_image("ak43.png")
    def __init__(self, pos):
        super().__init__()
        self.frames = []
        self.cut_sheet(Gun.image_gun,10,1)
        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.rect = self.rect.move(pos[0], pos[1])
        self.rect.center = self.rect.topleft
        
    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect. w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(frame_location,self.rect.size)))
    
    def get_angle(self, destination):
        side = destination[1] - self.rect.center[1]
        bottom = destination[0] - self.rect.center[0]     
        hypotenuse = (bottom ** 2 + side ** 2) ** (1/2)
        if hypotenuse != 0:
            angle =  180 * math.asin(side / hypotenuse) / math.pi
        else:
            angle = 0
        return angle, bottom
    
    def update(self, pos, player):
        angle, bottom = self.get_angle(pos)
        if 90 >= angle > 69:
            if bottom <= 0:
                self.current_frame = 7   
            else:
                self.current_frame = 8  
        elif 69 >= angle > 22:
            if bottom <= 0:
                self.current_frame = 6   
            else:
                self.current_frame = 9         
        elif 22 >= angle > -22:
            if bottom <= 0:
                self.current_frame = 5   
            else:
                self.current_frame = 0 
        elif -22 >= angle > -69:
            if bottom <= 0:
                self.current_frame = 4   
            else:
                self.current_frame = 1        
        elif -69 >= angle > -90:
            if bottom <= 0:
                self.current_frame = 3   
            else:
                self.current_frame = 2       
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect()
        self.rect.center = player.rect.center[0], player.rect.center[1] + 10

class UI_Element(pygame.sprite.Sprite):
    def __init__(self, pos, image):
        super().__init__()
        self.image = load_image(image)
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]   
          

class Player_UI(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.health = [UI_Element((30,28), 'player_heart.png'),
                       UI_Element((50,28), 'player_heart.png'),
                       UI_Element((70,28), 'player_heart.png')]
    
    def get_stats(self, player):
        for i in self.sprites():
            i.kill()         
        if player.health == 3:
            for i in self.health:
                self.add(i)                            
        if player.health == 2:
            for i in self.health[:2]:
                self.add(i)
        elif player.health == 1:
            self.add(self.health[:1]) 
            
               
class Enemies(pygame.sprite.Group):
    def __init__(self):
        super().__init__()    
    
    def update(self, player_pos, level, bullets, player):
        for i in self.sprites():
            i.move(player_pos, level, bullets, player)

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, image, death_sound, group):
        super().__init__(group)
        self.frames = []
        self.cut_sheet(load_image(image),9,2)
        self.current_frame = 0
        self.current_row = 0
        self.image = self.frames[self.current_row][self.current_frame]
        self.rect = self.rect.move(pos[0], pos[1])        
        self.speed = 1
        self.health = 100
        self.k = 0
        self.killed = False
        self.shooting = False 
        self.death_sound = pygame.mixer.Sound('sound/' + death_sound)
        self.death_sound.set_volume(0.5) 
        self.delay = 0
        self.key = {'right' : False, 'up' : False, 'left' : False, 'down' : False}
        self.w, self.h = self.rect.width, self.rect.height     
    
    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns, sheet.get_height() // rows)
        for j in range(rows):
            self.frames.append([])
            for i in range(columns):
                frame_location = (self.rect. w * i, self.rect.h * j)
                self.frames[j].append(sheet.subsurface(pygame.Rect(frame_location,self.rect.size)))      
    
    def calc_angle(self,mypos,pos):
        myX,myY,targetX,targetY = mypos[0],mypos[1],pos[0],pos[1]
        if(myX > targetX):
            dx = myX - targetX
        else:
            dx = targetX - myX 
        if(myY > targetY):
            dy = myY - targetY
        else:
            dy = targetY - myY
    
        if(dy == 0):
            dy = 1
        if(dx == 0):
            dx = 1
    
        if(dx > dy):
            Speedy = dy/dx 
            Speedx = self.speed
        if(dx < dy):
            Speedy = 1
            Speedx = dx/dy
        elif(dx == dy):
            Speedx = self.speed
            Speedy = self.speed
    
        if(myX > targetX):
            Speedx = Speedx * -1
        if(myY > targetY):
            Speedy = Speedy * -1

        return Speedx,Speedy
        
    def move(self, player_pos, level, bullets, player):
        speedx,speedy = self.calc_angle(self.rect.center,player_pos)
        if pygame.sprite.spritecollideany(self, bullets):
            col_list = pygame.sprite.spritecollide(self, bullets, False)
            if self.health - bullets.damage <= 0:
                for i in col_list:
                    i.kill() 
                    self.death_sound.play()
                self.killed = True
                return             
            else:
                self.health -= bullets.damage
                for i in col_list:
                    i.kill()                
            
        if pygame.sprite.collide_mask(self, player):
            player.health -= 1
            self.killed = True
            self.death_sound.play()
            player.death_sound.play()
            return    
        
        if pygame.sprite.spritecollideany(self, level):
            self.current_row = 1
        else:
            self.current_row = 0
        self.rect.topleft = self.rect.x + speedx, self.rect.y + speedy
        self.update()
        
    def update(self):
        if self.delay == 5:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_row][self.current_frame]  
            self.delay = 0
        else:
            self.delay += 1  
        