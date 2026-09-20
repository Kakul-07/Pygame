import pygame
import random
import math
pygame.init()
WIDTH=960
HEIGHT=600
WORLD_WIDTH=1800
WORLD_HEIGHT=1200
screen=pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Treasure Hunt")
clock=pygame.time.Clock()
background_sheet=pygame.image.load("assets/background.png").convert_alpha()
player_sheet=pygame.image.load("assets/character.png").convert_alpha()
font=pygame.font.Font(None,36)
class Camera:
    def __init__(self):
        self.x=0
        self.y=0
    def update(self,player):
        target_x=player.x+player.width//2-WIDTH//2
        target_y=player.y+player.height//2-HEIGHT//2
        self.x+=(target_x-self.x)*0.1
        self.y+=(target_y-self.y)*0.1
        self.x=max(0,min(self.x,WORLD_WIDTH-WIDTH))
        self.y=max(0,min(self.y,WORLD_HEIGHT-HEIGHT))
class Player:
    def __init__(self):
        self.x=WORLD_WIDTH//2
        self.y=WORLD_HEIGHT//2
        self.width=55
        self.height=73
        self.speed=5
        self.frames=[]
        for i in range(4):
            frame=player_sheet.subsurface((i*96,0,96,128))
            frame=pygame.transform.scale(frame,(self.width,self.height))
            self.frames.append(frame)
        self.current_frame=0
        self.animation_timer=0
        self.moving=False
        self.direction="right"
    def move(self):
        keys=pygame.key.get_pressed()
        self.moving=False
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.x-=self.speed
            self.moving=True
            self.direction="left"
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.x+=self.speed
            self.moving=True
            self.direction="right"
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.y-=self.speed
            self.moving=True
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.y+=self.speed
            self.moving=True
        self.x=max(0,min(self.x,WORLD_WIDTH-self.width))
        self.y=max(0,min(self.y,WORLD_HEIGHT-self.height))
    def animate(self):
        if self.moving:
            self.animation_timer+=1
            if self.animation_timer>=8:
                self.current_frame+=1
                if self.current_frame>=len(self.frames):
                    self.current_frame=0
                self.animation_timer=0
        else:
            self.current_frame=0
    def draw(self,camera):
        image=self.frames[self.current_frame]
        if self.direction=="left":
            image=pygame.transform.flip(image, True, False)
        screen.blit(image, (self.x-camera.x, self.y-camera.y))
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
class Coin(pygame.sprite.Sprite):
    def __init__(self,pos):
        super().__init__()
        self.center=pygame.Vector2(pos)
        self.rect=pygame.Rect(0,0,34,34)
        self.rect.center=pos
        self.angle=random.uniform(0,6.28)
        self.image=pygame.Surface((44,44), pygame.SRCALPHA)
    def update(self):
        self.angle+=0.08
        width=int(10+abs(math.sin(self.angle))*20)
        self.image.fill((0,0,0,0))
        pygame.draw.ellipse(self.image, (255,190,30), ( 22-width//2, 7, width, 30))
        pygame.draw.ellipse(self.image, (255,235,100), (22-width//2+3, 10, max(3,width-6), 24))
    def draw(self,camera):
        screen.blit(self.image, (self.rect.x-camera.x-5, self.rect.y-camera.y-5))
class World:
    def __init__(self):
        self.tree_image=self.load_tree()
        self.water_image=self.load_water()
        self.crate_image=self.load_crate()
        self.trees=[
            (70,80),
            (180,160),
            (420,90),
            (760,80),
            (1100,70),
            (1500,100),
            (1640,240),
            (120,500),
            (300,680),
            (90,930),
            (450,1030),
            (800,950),
            (1100,1050),
            (1500,980),
            (1650,760),
            (1420,570)
        ]
        self.crates=[
            (260,300),
            (580,180),
            (1180,320),
            (1450,430),
            (400,820),
            (1000,720),
            (1550,850)
        ]
        self.water=[
            pygame.Rect(1250,90,300,190),
            pygame.Rect(180,760,280,190),
            pygame.Rect(1300,650,300,180)
        ]
    def load_tree(self):
        image=background_sheet.subsurface((0,460,76,230)).copy()
        return pygame.transform.scale(image, (70,115))
    def load_water(self):
        image=background_sheet.subsurface((764,0,228,228)).copy()
        return pygame.transform.scale(image, (150,150))
    def load_crate(self):
        image=background_sheet.subsurface((620,705,50,50)).copy()
        return pygame.transform.scale(image, (55,55))
    def draw_ground(self,camera):
        screen.fill((105,165,75))
        path_color=(211,180,125)
        path_edge=(183,148,96)
        pygame.draw.rect(screen, path_color, (-camera.x, 510-camera.y, WORLD_WIDTH, 140))
        pygame.draw.rect(screen, path_color,(830-camera.x, -camera.y, 140, WORLD_HEIGHT))
        pygame.draw.line(screen, path_edge, (-camera.x, 510-camera.y), (WORLD_WIDTH-camera.x, 510-camera.y), 5)
        pygame.draw.line(screen, path_edge(-camera.x, 650-camera.y), (WORLD_WIDTH-camera.x, 650-camera.y), 5)
        pygame.draw.line(screen, path_edge(830-camera.x, -camera.y), (830-camera.x, WORLD_WIDTH-camera.y), 5)
        pygame.draw.line(screen, path_edge(970-camera.x, -camera.y), (970-camera.x, WORLD_WIDTH-camera.y), 5)
    def draw_water(self,camera):
        for area in self.water:
            x=area.x
            while x<area.right:
                y=area.y
                while y<area.bottom:
                    screen.blit(self.water_image, (x-camera.x, y-camera.y))
                    y+=150
                x+=150
            pygame.draw.rect(screen, (90,135,85),(area.x-camera.x, area.y-camera.y, area.width, area.height), 6)
    def draw_objects(self,camera):
        for x,y in self.trees:
            screen.blit(self.tree_image,(x-camera.x, y-camera.y))
        for x,y in self.crates:
            screen.blit(self.crate_image, (x-camera.x, y-camera.y))
    def draw(self,camera):
        self.draw_ground(camera)
        self.draw_water(camera)
        self.draw_objects(camera)
def create_coins():
    coins=pygame.sprite.Group()
    positions=[]
    while len(positions)<15:
        x=random.randint(100, WORLD_WIDTH-100)

        y=random.randint(100, WORLD_HEIGHT-100)
        position=pygame.Vector2(x,y)
        if position.distance_to(pygame.Vector2(WORLD_WIDTH//2, WORLD_HEIGHT//2))<180:
            continue
        if any(position.distance_to(pygame.Vector2(px,py))<100 for px,py in positions):
            continue
        positions.append((x,y))
    for position in positions:
        coin=Coin(position)
        coins.add(coin)
    return coins
player=Player()
world=World()
camera=Camera()
coins=create_coins()
score=0
running=True
while running:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
    player.move()
    player.animate()
    coins.update()
    player_rect=player.get_rect()
    collected=[]
    for coin in coins:
        if player_rect.colliderect(coin.rect):
            collected.append(coin)
    for coin in collected:
        coin.kill()
        score+=1
    camera.update(player)
    world.draw(camera)
    for coin in coins:
        coin.draw(camera)
    player.draw(camera)
    score_text=font.render("Coins: "+str(score), True, (255,255,255))
    screen.blit(score_text, (25,25))
    pygame.display.update()
    clock.tick(60)
pygame.quit()