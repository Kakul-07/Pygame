import pygame
pygame.init()

screen = pygame.display.set_mode((800, 500))
pygame.display.set_caption("Treasure Hunt")

clock = pygame.time.Clock()
player_sheet = pygame.image.load("assets/player_sheet.png")
frames = []
for i in range(4):
    frame = player_sheet.subsurface((i * 64, 0, 64, 64))
    frames.append(frame)
player = pygame.Rect(100, 200, 64, 64)

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
    screen.blit(frames[0], player)
    pygame.display.update()
    clock.tick(60)
pygame.quit()