import pygame, sys
import player


pygame.init()
clock = pygame.time.Clock()

# Game Screen
screen_width = 500
screen_height = 250
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("PyGame Game")
running = True

# Creating Sprites and Groups

moving_sprites = pygame.sprite.Group()
player = player.Player()
moving_sprites.add(player)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_LEFT]:
        player.walking = True
        player.update_position(-2, 0)
            #x -= vel
    elif keys[pygame.K_RIGHT]:
        player.walking = True
        player.update_position(2, 0)
            #x += vel
    elif keys[pygame.K_UP]:
        player.walking = True
        player.update_position(0, -2)
            #y -= vel
    elif keys[pygame.K_DOWN]:
        player.walking = True
        player.update_position(0, 2)
            #y += vel
    else:
        player.walking = False
    

    player.animate()

    screen.fill((255, 255, 255))
    moving_sprites.draw(screen)
    moving_sprites.update()

    pygame.display.flip()

    clock.tick(60)

pygame.quit()