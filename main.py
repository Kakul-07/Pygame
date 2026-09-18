import pygame
pygame.init()
screen = pygame.display.set_mode((800, 500))
pygame.display.set_caption("Treasure Hunt")
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((30, 30, 40))
    pygame.display.update()
pygame.quit()