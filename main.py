import pygame
pygame.init()

screen = pygame.display.set_mode((800, 500))
pygame.display.set_caption("Treasure Hunt")

clock = pygame.time.Clock()

class Player:
    def __init__(self):
        self.image = pygame.image.load("assets/player_sheet.png")
        self.frames = []
        for i in range(4):
            frame = self.image.subsurface((i * 64, 0, 64, 64))
            self.frames.append(frame)
        self.rect = pygame.Rect(100, 200, 64, 64)
        self.current_frame = 0
        self.last_update = 0
        self.animation_speed = 150
    def move(self, obstacles):
        keys = pygame.key.get_pressed()
        self.moving = False
        old_x = self.rect.x
        old_y = self.rect.y
        if keys[pygame.K_RIGHT]:
            self.rect.x += 5
            self.moving = True
        if keys[pygame.K_LEFT]:
            self.rect.x -= 5
            self.moving = True
        if keys[pygame.K_UP]:
            self.rect.y -= 5
            self.moving = True
        if keys[pygame.K_DOWN]:
           self.rect.y += 5
           self.moving = True
        for obstacle in obstacles:
          if self.rect.colliderect(obstacle.rect):
            self.rect.x = old_x
            self.rect.y = old_y
    def animate(self):
        if self.moving:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_update >= self.animation_speed:
                 self.current_frame += 1
                 if self.current_frame >= 4:
                     self.current_frame = 0
                 self.last_update = current_time
        else:
            self.current_frame = 0         
    def draw(self):
        screen.blit(self.frames[self.current_frame], self.rect)
class Coin:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 30, 30)
        self.collected = False
    def collect(self, player_rect):
        if self.rect.colliderect(player_rect):
            self.collected = True    
    def draw(self):
        if not self.collected:
            pygame.draw.circle(screen, (255, 200, 0), self.rect.center, 15)

class Obstacle:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
    def draw(self):
        pygame.draw.rect(screen, (100, 100, 100), self.rect)            

player = Player()
coin = Coin(500, 250)
obstacles = [
    Obstacle(300, 150, 150, 40),
    Obstacle(200, 350, 40, 100),
    Obstacle(600, 100, 40, 150)
]
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    player.move(obstacles)
    player.animate()
    coin.collect(player.rect)
    screen.fill((30, 30, 40))
    player.draw()
    coin.draw()
    for obstacle in obstacles:
        obstacle.draw()
    pygame.display.update()
    clock.tick(60)
pygame.quit()