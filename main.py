import pygame
pygame.init()

screen = pygame.display.set_mode((1000, 600))
pygame.display.set_caption("Treasure Hunt")

player_image = pygame.image.load("assets/player.png")
player_image = pygame.transform.scale(player_image, (50, 50))
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

    screen.blit(player_image, player)

    pygame.display.update()

pygame.quit()