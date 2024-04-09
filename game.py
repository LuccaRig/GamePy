import pygame, sys
import player
import pytmx


pygame.init()
clock = pygame.time.Clock()

# Game Screen
screen_width = 1280
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("PyGame Game")
running = True

# Creating Sprites and Groups

moving_sprites = pygame.sprite.Group()
player = player.Player()
moving_sprites.add(player)

tmx_map = pytmx.load_pygame("Tiled/Map1.tmx")

def render_layer(layer):
    for x, y, image in layer.tiles():
        screen.blit(image, (x * tmx_map.tilewidth, y * tmx_map.tileheight))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_z]:
        player.walking = False
        player.attacking = True
        
    elif keys[pygame.K_LEFT]:
        player.attacking = False
        player.walking = True
        player.update_position(-2, 0)
            #x -= vel
    elif keys[pygame.K_RIGHT]:
        player.attacking = False
        player.walking = True
        player.update_position(2, 0)
            #x += vel
    elif keys[pygame.K_UP]:
        player.attacking = False
        player.walking = True
        player.update_position(0, -2)
            #y -= vel
    elif keys[pygame.K_DOWN]:
        player.attacking = False
        player.walking = True
        player.update_position(0, 2)
            #y += vel
    else:
        player.walking = False
        player.attacking = False

    screen.fill((255, 255, 255))

    scale_factor = 10
    for layer in tmx_map.visible_layers:
         for x, y, image in layer.tiles():
            # Multiplique as coordenadas dos tiles pelo fator de escala
            scaled_x = (x * tmx_map.tilewidth * scale_factor) + 300
            scaled_y = y * tmx_map.tileheight * scale_factor
            # Redimensione a imagem do tile
            scaled_image = pygame.transform.scale(image, (tmx_map.tilewidth * scale_factor, tmx_map.tileheight * scale_factor))
            # Desenhe a imagem redimensionada na tela
            screen.blit(scaled_image, (scaled_x, scaled_y))
    

    player.animate()

    moving_sprites.draw(screen)
    moving_sprites.update()

    pygame.display.flip()

    clock.tick(60)

pygame.quit()