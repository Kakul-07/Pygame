import pygame,random,math
pygame.init()
pygame.mixer.init()
WIDTH,HEIGHT=960,600
WORLD_WIDTH,WORLD_HEIGHT=3000,2000
FPS=60
screen=pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Treasure Hunt")
clock=pygame.time.Clock()
font=pygame.font.Font(None,36)
small_font=pygame.font.Font(None,26)
big_font=pygame.font.Font(None,70)
background=pygame.image.load("assets/background.png").convert_alpha()
player_sheet=pygame.image.load("assets/character.png").convert_alpha()
enemy_sheet=pygame.image.load("assets/enemy.png").convert_alpha()
def load_image(path,size):
    image=pygame.image.load(path).convert()
    return pygame.transform.scale(image,size)
def remove_background(image,tolerance=25):
    image=image.convert_alpha()
    pixels=pygame.PixelArray(image)
    r0,g0,b0,_=image.get_at((0,0))
    for x in range(image.get_width()):
        for y in range(image.get_height()):
            r,g,b,a=image.get_at((x,y))
            if abs(r-r0)<tolerance and abs(g-g0)<tolerance and abs(b-b0)<tolerance:
                pixels[x,y]=0
    del pixels
    return image
coin_image=remove_background(load_image("assets/coin.jpg",(45,45)),20)
key_image=remove_background(load_image("assets/key.png",(55,70)),25)
shield_image=load_image("assets/sheild.png",(65,70))
ground=pygame.transform.scale(background.subsurface((0,0,384,384)),(192,192))
tree_image=pygame.transform.scale(background.subsurface((0,1180,150,360)),(75,180))
crate_image=pygame.transform.scale(background.subsurface((1020,1160,180,160)),(90,80))
gate_image=pygame.transform.scale(background.subsurface((1760,1280,150,120)),(120,100))
enemy_rects=[(0,0,68,94),(69,0,68,94),(0,97,68,94),(69,97,68,94),(0,194,68,94),
             (69,194,68,94),(137,194,62,94),(0,291,68,94),(69,291,68,94),(0,388,68,82),(69,388,68,94)]
enemy_frames=[]
for x,y,w,h in enemy_rects:
    frame=enemy_sheet.subsurface((x,y,w,h)).copy()
    enemy_frames.append(pygame.transform.scale(frame,(60,80)))
win_music=pygame.mixer.Sound("assets/music.mp3")
collect_sound=pygame.mixer.Sound("assets/music3.mp3")
win_music.set_volume(0.7)
collect_sound.set_volume(0.7)
try:
    with open("highscore.txt","r") as file:
        high_score=int(file.read())
except:
    high_score=0
class Camera:
    def __init__(self):
        self.x=0
        self.y=0
    def update(self,p):
        tx=p.rect.centerx-WIDTH//2
        ty=p.rect.centery-HEIGHT//2
        self.x+=(tx-self.x)*0.1
        self.y+=(ty-self.y)*0.1
        self.x=max(0,min(self.x,WORLD_WIDTH-WIDTH))
        self.y=max(0,min(self.y,WORLD_HEIGHT-HEIGHT))
class Player:
    def __init__(self):
        self.image=pygame.transform.scale(player_sheet.subsurface((0,0,96,128)),(60,80))
        self.rect=self.image.get_rect(center=(150,300))
        self.speed=5
        self.lives=3
        self.keys=0
        self.coins=0
        self.shield=0
        self.invincible=0
    def move(self,k,obstacles):
        dx=0
        dy=0
        if  k[pygame.K_LEFT]:
            dx=-self.speed
        if  k[pygame.K_RIGHT]:
            dx=self.speed
        if k[pygame.K_UP]:
            dy=-self.speed
        if k[pygame.K_DOWN]:
            dy=self.speed
        self.rect.x+=dx
        for obstacle in obstacles:
            if self.rect.colliderect(obstacle.rect):
                if dx>0:
                    self.rect.right=obstacle.rect.left
                elif dx<0:
                    self.rect.left=obstacle.rect.right
        self.rect.y+=dy
        for obstacle in obstacles:
            if self.rect.colliderect(obstacle.rect):
                if dy>0:
                    self.rect.bottom=obstacle.rect.top
                elif dy<0:
                    self.rect.top=obstacle.rect.bottom
        self.rect.left=max(0,self.rect.left)
        self.rect.right=min(WORLD_WIDTH,self.rect.right)
        self.rect.top=max(0,self.rect.top)
        self.rect.bottom=min(WORLD_HEIGHT,self.rect.bottom)
        if self.invincible>0:
            self.invincible-=1
    def hit(self):
        if self.invincible>0:
            return
        if self.shield:
            self.shield=0
            self.invincible=60
        else:
            self.lives-=1
            self.invincible=120
class Key:
    def __init__(self,x,y):
        self.image=key_image
        self.rect=self.image.get_rect(center=(x,y))
        self.angle=random.random()*6.28
        self.collected=False
    def update(self):
        self.angle+=0.08
    def draw(self,s,c):
        if self.collected:
            return
        y=self.rect.y+int(math.sin(self.angle)*5)
        s.blit(self.image,(self.rect.x-c.x,y-c.y))
class Coin:
    def __init__(self,x,y):
        self.image=coin_image
        self.rect=self.image.get_rect(center=(x,y))
        self.angle=random.random()*6.28
    def update(self):
        self.angle+=0.08
    def draw(self,s,c):
        y=self.rect.y+int(math.sin(self.angle)*5)
        s.blit(self.image,(self.rect.x-c.x,y-c.y))
class Obstacle:
    def __init__(self,x,y,kind):
        self.x=x
        self.y=y
        if kind=="tree":
            self.image=tree_image
            self.rect=pygame.Rect(x+15,y+75,45,95)
        else:
            self.image=crate_image
            self.rect=self.image.get_rect(topleft=(x,y))
    def draw(self,s,c):
        s.blit(self.image,(self.x-c.x,self.y-c.y))
class Enemy:
    def __init__(self,x,y,speed):
        self.frames=enemy_frames
        self.frame=0
        self.timer=0
        self.animation_speed=6
        self.speed=speed
        self.x=float(x)
        self.y=float(y)
        self.image=self.frames[0]
        self.rect=self.image.get_rect(topleft=(x,y))
    def update(self,p):
        if self.x<p.rect.x:
            self.x+=self.speed
        elif self.x>p.rect.x:
            self.x-=self.speed
        if self.y<p.rect.y:
            self.y+=self.speed
        elif self.y>p.rect.y:
            self.y-=self.speed
        self.rect.x=int(self.x)
        self.rect.y=int(self.y)
        self.timer+=1
        if self.timer>=self.animation_speed:
            self.timer=0
            self.frame=(self.frame+1)%len(self.frames)
            center=self.rect.center
            self.image=self.frames[self.frame]
            self.rect=self.image.get_rect(center=center)
    def draw(self,s,c):
        s.blit(self.image,(self.rect.x-c.x,self.rect.y-c.y))
class PowerUp:
    def __init__(self,x,y):
        self.image=shield_image
        self.rect=self.image.get_rect(center=(x,y))
        self.angle=random.random()*6.28
    def update(self):
        self.angle+=0.08
    def draw(self,s,c):
        y=self.rect.y+int(math.sin(self.angle)*5)
        s.blit(self.image,(self.rect.x-c.x,y-c.y))
class Gate:
    def __init__(self,x,y):
        self.image=gate_image
        self.rect=self.image.get_rect(topleft=(x,y))
    def draw(self,s,c):
        s.blit(self.image,(self.rect.x-c.x,self.rect.y-c.y))
class Treasure:
    def __init__(self,x,y):
        self.image=crate_image
        self.rect=self.image.get_rect(topleft=(x,y))
        self.angle=0
    def update(self):
        self.angle+=0.05
    def draw(self,s,c):
        y=self.rect.y+int(math.sin(self.angle)*4)
        s.blit(self.image,(self.rect.x-c.x,y-c.y))
class World:
    def __init__(self,difficulty):
        self.difficulty=difficulty
        self.obstacles=[]
        self.enemies=[]
        self.keys=[]
        self.coins=[]
        self.powerups=[]
        key_count=min(1+difficulty//3,4)
        enemy_count=min(2+difficulty*2,12)
        obstacle_count=min(10+difficulty*5,45)
        safe=[(150,300)]
        for i in range(key_count):
            pos=self.position(safe)
            safe.append(pos)
            self.keys.append(Key(*pos))
        gate_pos=self.position(safe)
        safe.append(gate_pos)
        random.seed()
        for _ in range(obstacle_count):
            x=random.randint(350,2600)
            y=random.randint(150,1700)
            if all(math.hypot(x-a,y-b)>150 for a,b in safe):
                self.obstacles.append(Obstacle(x,y,random.choice(["tree","tree","crate"])))
        for _ in range(enemy_count):
            x=random.randint(700,2700)
            y=random.randint(300,1700)
            self.enemies.append(Enemy(x,y,1+difficulty*0.15))
        for _ in range(10+difficulty*3):
            x=random.randint(350,2700)
            y=random.randint(150,1700)
            self.coins.append(Coin(x,y))
        self.powerups.append(PowerUp(random.randint(300,700),random.randint(350,700)))
        self.gate=Gate(*gate_pos)
        self.treasure=Treasure(gate_pos[0]+20,gate_pos[1]+105)
    def position(self,safe):
        while True:
            x=random.randint(500,2600)
            y=random.randint(200,1600)
            if all(math.hypot(x-a,y-b)>180 for a,b in safe):
                return x,y
    def update(self,p):
        for key in self.keys:
            key.update()
        for coin in self.coins:
            coin.update()
        for enemy in self.enemies:
            enemy.update(p)
        for power in self.powerups:
            power.update()
        self.treasure.update()
def draw_world(s,c,w):
    for x in range(0,WORLD_WIDTH,192):
        for y in range(0,WORLD_HEIGHT,192):
            s.blit(ground,(x-c.x,y-c.y))
    for obstacle in w.obstacles:
        obstacle.draw(s,c)
    for coin in w.coins:
        coin.draw(s,c)
    for key in w.keys:
        key.draw(s,c)
    for power in w.powerups:
        power.draw(s,c)
    for enemy in w.enemies:
        enemy.draw(s,c)
    w.gate.draw(s,c)
    if all(key.collected for key in w.keys):
        w.treasure.draw(s,c)
def draw_hud(p,score,difficulty,w):
    text=small_font.render(f"Danger {difficulty}   Lives: {p.lives}   Keys: {p.keys}/{len(w.keys)}   Coins: {p.coins}   Score: {score}   High: {high_score}",True,(255,255,255))
    screen.blit(text,(15,15))
    if p.shield:
        screen.blit(small_font.render("SHIELD ACTIVE",True,(220,240,255)),(15,45))
def draw_marker(p,w):
    target=None
    for key in w.keys:
        if not key.collected:
            target=key
            break
    if target:
        distance=int(math.hypot(target.rect.centerx-p.rect.centerx,target.rect.centery-p.rect.centery))
        text=small_font.render(f"KEY -> {distance}",True,(255,230,60))
    else:
        distance=int(math.hypot(w.gate.rect.centerx-p.rect.centerx,w.gate.rect.centery-p.rect.centery))
        text=small_font.render(f"GATE -> {distance}",True,(255,215,0))
    screen.blit(text,(WIDTH-190,85))
def menu_background():
    for x in range(0,WIDTH,192):
        for y in range(0,HEIGHT,192):
            screen.blit(ground,(x,y))
def start_screen():
    menu_background()
    text=big_font.render("TREASURE HUNT",True,(255,215,0))
    screen.blit(text,(WIDTH//2-text.get_width()//2,70))
    lines=["Collect the keys -> reach the gate -> find the treasure.","Collect coins for extra score.","Use the shield to survive an enemy hit.","Arrow Keys = Move","P = Pause","SPACE = Start"]
    y=160
    for line in lines:
        text=small_font.render(line,True,(255,255,255))
        screen.blit(text,(WIDTH//2-text.get_width()//2,y))
        y+=40
    pygame.display.flip()
def game_over_screen(score):
    menu_background()
    text=big_font.render("GAME OVER",True,(255,80,80))
    screen.blit(text,(WIDTH//2-text.get_width()//2,130))
    text=font.render(f"Score: {score}   High Score: {high_score}",True,(255,255,255))
    screen.blit(text,(WIDTH//2-text.get_width()//2,240))
    text=font.render("Press R to Restart",True,(255,215,0))
    screen.blit(text,(WIDTH//2-text.get_width()//2,330))
    pygame.display.flip()
def treasure_screen(score,difficulty):
    menu_background()
    text=big_font.render("TREASURE FOUND!",True,(255,215,0))
    screen.blit(text,(WIDTH//2-text.get_width()//2,120))
    text=font.render(f"Score: {score}   Danger: {difficulty}",True,(255,255,255))
    screen.blit(text,(WIDTH//2-text.get_width()//2,230))
    text=font.render("Press SPACE for the next hunt",True,(255,215,0))
    screen.blit(text,(WIDTH//2-text.get_width()//2,330))
    pygame.display.flip()
def new_hunt(difficulty):
    return Player(),World(difficulty),Camera()
difficulty=1
player,world,camera=new_hunt(difficulty)
start=True
treasure_found=False
game_over=False
paused=False
score=0
running=True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            if score>high_score:
                high_score=score
            with open("highscore.txt","w") as file:
                file.write(str(high_score))
            running=False
        if event.type==pygame.KEYDOWN:
            if start and event.key in (pygame.K_SPACE,pygame.K_RETURN):
                start=False
            elif treasure_found and event.key==pygame.K_SPACE:
                difficulty+=1
                player,world,camera=new_hunt(difficulty)
                treasure_found=False
            elif game_over and event.key==pygame.K_r:
                difficulty=1
                score=0
                player,world,camera=new_hunt(difficulty)
                game_over=False
                paused=False
            elif not start and not treasure_found and not game_over and event.key==pygame.K_p:
                paused=not paused
    if start:
        start_screen()
        continue
    if treasure_found:
        treasure_screen(score,difficulty)
        continue
    if game_over:
        game_over_screen(score)
        continue
    if not paused:
        keys=pygame.key.get_pressed()
        player.move(keys,world.obstacles)
        world.update(player)
        for key in world.keys:
            if not key.collected and player.rect.colliderect(key.rect):
                key.collected=True
                player.keys+=1
                score+=100
                collect_sound.play()
        for coin in world.coins[:]:
            if player.rect.colliderect(coin.rect):
                world.coins.remove(coin)
                player.coins+=1
                score+=10
                collect_sound.play()
        for power in world.powerups[:]:
            if player.rect.colliderect(power.rect):
                player.shield=1
                world.powerups.remove(power)
                score+=25
                collect_sound.play()
        for enemy in world.enemies:
            if player.rect.colliderect(enemy.rect):
                player.hit()
        if player.lives<=0:
            game_over=True
        if all(key.collected for key in world.keys):
            if player.rect.colliderect(world.gate.rect) and player.rect.colliderect(world.treasure.rect):
                score+=500
                win_music.play()
                treasure_found=True
        if score>high_score:
            high_score=score
        camera.update(player)
    draw_world(screen,camera,world)
    if player.invincible%10<5:
        screen.blit(player.image,(player.rect.x-camera.x,player.rect.y-camera.y))
    draw_hud(player,score,difficulty,world)
    draw_marker(player,world)
    if paused:
        text=big_font.render("PAUSED",True,(255,255,255))
        screen.blit(text,(WIDTH//2-text.get_width()//2,HEIGHT//2-40))
    pygame.display.flip()
pygame.quit()