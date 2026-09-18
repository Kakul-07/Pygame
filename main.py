import pygame
pygame.init()
screen = pygame.display.set_mode((1000, 600))
pygame.display.set_caption("Treasure Hunt")
player = pygame.Rect(100, 200, 50, 50)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
      player.x += 5
    if keys[pygame.K_LEFT]:
      player.x -= 5
    if keys[pygame.K_UP]:
      player.y -= 5
    if keys[pygame.K_DOWN]:
      player.y += 5 

    screen.fill((30, 30, 40))
    pygame.draw.rect(screen, (50, 200, 100), player)
    pygame.display.update()
pygame.quit()