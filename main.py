import pygame
pygame.init()

screen=pygame.display.set_mode((800,500))
pygame.display.set_caption("Treasure Hunt")

clock=pygame.time.Clock()

background_sheet=pygame.image.load("assets/background.png").convert_alpha()
player_sheet=pygame.image.load("assets/character.png").convert_alpha()

grass=background_sheet.subsurface((0,0,228,228))
grass=pygame.transform.scale(grass,(100,100))
tree=background_sheet.subsurface((0,460,76,230))
tree=pygame.transform.scale(tree,(60,100))
player_frames=[]
for i in range(4):
    frame=player_sheet.subsurface((i*96,0,96,128))
    frame=pygame.transform.scale(frame,(60,80))
    player_frames.append(frame)
current_frame=0
animation_timer=0

player=pygame.Rect(370,210,60,80)
trees=[
    pygame.Rect(200,100,60,100),
    pygame.Rect(500,100,60,100),
    pygame.Rect(650,300,60,100)
]

speed=5
running=True
while running:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False

    keys=pygame.key.get_pressed()
    moving=False
    if keys[pygame.K_RIGHT]:
        player.x+=speed
    if keys[pygame.K_LEFT]:
        player.x-=speed
    if keys[pygame.K_UP]:
        player.y-=speed
    if keys[pygame.K_DOWN]:
        player.y+=speed
    for tree_rect in trees:
        if player.colliderect(tree_rect):
            if keys[pygame.K_RIGHT]:
                 player.x-=speed
            if keys[pygame.K_LEFT]:
                player.x+=speed
            if keys[pygame.K_UP]:
                player.y+=speed
            if keys[pygame.K_DOWN]:
                player.y-=speed    
    if keys[pygame.K_RIGHT] or keys[pygame.K_LEFT] or keys[pygame.K_UP] or keys[pygame.K_DOWN]:
        moving=True
    if moving:
        animation_timer+=1
        if animation_timer>=8:
            current_frame+=1
            if current_frame>=4:
                current_frame=0
            animation_timer=0
    else:
        current_frame=0
    for x in range(0,800,100):
        for y in range(0,500,100):
            screen.blit(grass,(x,y))
    for tree_rect in trees:
        screen.blit(tree,tree_rect)        
    screen.blit(player_frames[current_frame],player)
    pygame.display.update()
    clock.tick(60)
pygame.quit()