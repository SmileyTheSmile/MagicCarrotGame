import pygame,os,math
from bullet import Bullet

def load_image(name, colorkey = None):
    fullname = os.path.join('resourses', name)
    try:
        return pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)  

class Player(pygame.sprite.Sprite):
    image = load_image("player_sprites.png")
    def __init__(self, pos):
        super().__init__()
        self.frames = {'right':[], 'left':[], 'down':[], 'up':[]}
        self.cut_sheet(Player.image, 9, 4)        
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.current_frame = 0
        self.health = 3
        self.shooting = False         
        self.image = self.frames['right'][self.current_frame]
        self.rect = self.rect.move(20,38)
        self.current_dir = 'right'
        self.key = {'right':False, 'up':False, 'left':False, 'down':False}
        self.w,self.h=self.rect.width,self.rect.height
        
    def move(self,level):
        order = True
        n1, n2 = self.rect.x, self.rect.y
        if not self.key['up'] and not self.key['down'] and not self.key['right'] and not self.key['left']:
            self.current_frame = -1
        else:
            u1, u2, l1, d1, d2, r1=level.check_collision(n1,n2+self.h-2), level.check_collision(n1+self.w,n2+self.h-2),level.check_collision(n1-2,n2+self.h), level.check_collision(n1,n2+self.h+2),level.check_collision(n1+self.w,n2+2+self.h), level.check_collision(n1+self.w+2,n2+self.h)            
            if self.key['up'] and not self.key['down']:
                if n2 - 2 > 0:
                    if u1 and u2:
                        self.rect.y-=2
                self.current_dir = 'up'
            if self.key['left'] and not self.key['right']:
                if n1 - 2 > 0:
                    if l1:
                        self.rect.x-=2 
                self.current_dir = 'left'
            if self.key['down'] and not self.key['up']:
                if n2 + 2 < level.height:
                    if d1 and d2:
                        self.rect.y+=2    
                self.current_dir = 'down'
            if self.key['right'] and not self.key['left']:
                if n1 + 2 < level.width:
                    if r1:
                        self.rect.x+=2 
                self.current_dir = 'right'
        
        player_pos = level.get_cell(n1, n2+self.h) 
        l1, u1, r1, l2, u2, r2 = player_pos[0]-1, player_pos[1]-1, player_pos[0]+1, player_pos[0]-2, player_pos[1]-2, player_pos[0]+2
        if r1+1<=len(level.board[0]) and l1+1<=len(level.board[0]) and r2+1<=len(level.board[0]) and l2+1<=len(level.board[0]):
            if level.board[l1][u1]!=None or level.board[r1][u1]!=None or level.board[player_pos[0]][u1]!=None or level.board[l2][u2]!=None or level.board[r2][u2]!=None or level.board[player_pos[0]][u2]!=None:
                order = False
        return order
    
    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
        sheet.get_height() // rows)
        keys = ['right','left','down','up']
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect. w* i, self.rect.h * j)
                self.frames[keys[j]].append(sheet.subsurface(pygame.Rect(frame_location,self.rect.size)))  
                
    def update(self, key):
        self.current_frame = (self.current_frame + 1) % len(self.frames[key])
        self.image = self.frames[key][self.current_frame]    
    
class Gun(pygame.sprite.Sprite):
    image_gun = load_image("ak43.png")
    def __init__(self,pos):
        super().__init__()
        self.image = Gun.image_gun
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.angle = 0
        self.rect.y = pos[1]        
    def get_angle(self, destination):
        x_dist = destination[0] - self.rect.center[0]
        y_dist = destination[1] - self.rect.center[1]
        return math.atan2(-y_dist, x_dist) % (2 * math.pi)   
    def update(self,pos,player):
        self.rect = self.image.get_rect()
        self.rect.center = player.rect.center[0], player.rect.center[1]+10

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
        self.health = [UI_Element((30,28),'player_heart.png'),
                       UI_Element((50,28),'player_heart.png'),
                       UI_Element((70,28),'player_heart.png')]
    
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
    
    def update(self,player_pos,level,bullets,player):
        for i in self.sprites():
            i.move(player_pos,level,bullets,player)

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos,image):
        super().__init__()
        self.image = load_image(image)
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.speed = 1
        self.health = 100
        self.k = 0
        self.shooting = False 
        self.key = {'right':False, 'up':False, 'left':False, 'down':False}
        self.w,self.h=self.rect.width,self.rect.height     

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
        
    def move(self,player_pos,level,bullets,player):
        speedx,speedy = self.calc_angle(self.rect.center,player_pos)
        if pygame.sprite.spritecollideany(self,bullets):
            col_list = pygame.sprite.spritecollide(self,bullets,False)
            if self.health - bullets.damage <= 0:
                self.kill()
                for i in col_list:
                    i.kill()                
                return             
            else:
                self.health -= bullets.damage
                for i in col_list:
                    i.kill()                
            
        if pygame.sprite.spritecollideany(self,player):
            player.sprites()[0].health -= 1
            self.kill()
            return            
        d1 = level.check_collision(self.rect.x + self.k, self.rect.y + self.rect.height + 1 + self.k,True)
        d2 = level.check_collision(self.rect.x + self.rect.width + self.k, self.rect.y + self.rect.height + 1 + self.k,True)
        
        dul = level.check_collision(self.rect.x - 1 - self.k, self.rect.y + self.rect.height - 1 - self.k,True) 
        dur = level.check_collision(self.rect.x + self.rect.width + 1 + self.k, self.rect.y + self.rect.height-1 + self.k,True)
        
        u1 = level.check_collision(self.rect.x + self.k, self.rect.y + self.rect.height - 1 - self.k,True)
        u2 = level.check_collision(self.rect.x + self.rect.width + self.k, self.rect.y + self.rect.height - 1 - self.k,True)
        
        r1 = level.check_collision(self.rect.x + self.rect.width + 1 + self.k, self.rect.y + self.rect.height + self.k,True)
        
        l1 = level.check_collision(self.rect.x - 1 - self.k,self.rect.y + self.rect.height + self.k,True)
        
        ddl = level.check_collision(self.rect.x - 1 - self.k, self.rect.y+self.rect.height + 1 + self.k,True)
        ddr = level.check_collision(self.rect.x + self.rect.width + 1 + self.k, self.rect.y + self.rect.height + 1 + self.k,True)
        
        #col_list = pygame.sprite.spritecollide(self,self.groups()[0],False)
        
        if u1 and u2 and d1 and d2 and r1 and l1 and dul and dur and ddl and ddr:
            self.rect.x, self.rect.y = self.rect.x + speedx, self.rect.y + speedy
        else:
            if not u1 or not u2:
                self.rect.x = self.rect.x + self.speed        
            elif not d1 or not d2:
                self.rect.x = self.rect.x + self.speed
            elif not ddl:
                self.rect.x, self.rect.y = self.rect.x + (self.speed * 2),self.rect.y + self.speed
            elif not ddr:
                self.rect.x, self.rect.y = self.rect.x - (self.speed * 2),self.rect.y + self.speed
            elif not dul:
                self.rect.x, self.rect.y = self.rect.x + (self.speed * 2),self.rect.y - self.speed
            elif not dur:
                self.rect.x, self.rect.y = self.rect.x - (self.speed * 2),self.rect.y - self.speed
            elif not l1:
                if not dul:
                    self.rect.y = self.rect.y - self.speed     
                elif not ddl:
                    self.rect.y = self.rect.y + self.speed   
            elif not r1:
                if not dur:
                    self.rect.y = self.rect.y - self.speed     
                elif not ddr:
                    self.rect.y = self.rect.y + self.speed              