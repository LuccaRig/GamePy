import pygame, sys
import player
import map

def main():
    pygame.init()
    clock = pygame.time.Clock()

    # Game Screen
    screen_width = 1280
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("PyGame Game")
    running = True

    # Creating Sprites and Groups
    player_character = player.Player()
    moving_sprites = pygame.sprite.Group()
    moving_sprites.add(player_character)


    myMap = map.Map("Tiled/Map1.tmx")

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_z]:
            player_character.walking = False
            player_character.attacking = True
            
        elif keys[pygame.K_LEFT]:
            if player_character.attacking == False:
                player_character.walking = True
                player_character.update_position(-2, 0)
                #x -= vel
        elif keys[pygame.K_RIGHT]:
            if player_character.attacking == False:
                player_character.walking = True
                player_character.update_position(2, 0)
                #x += vel
        elif keys[pygame.K_UP]:
            if (player_character.attacking == False) and (player_character.isGrounded(myMap)):
                player_character.jumping = True
                player_character.update_position(0, -20)
                    #y -= vel
        elif keys[pygame.K_DOWN]:
            if (not player_character.isGrounded(myMap)) and (player_character.attacking == False):
                player_character.walking = True
                player_character.update_position(0, 2)
                    #y += vel
        else:
            player_character.walking = False

        screen.fill((128, 128, 128))

        myMap.renderVisibleLayers(screen)
        player_character.draw_collision_rect(screen)

        moving_sprites.draw(screen)
        moving_sprites.update()

        player_character.animate()

        moving_sprites.draw(screen)
        moving_sprites.update()

        pygame.display.flip()

        clock.tick(60)

    pygame.quit()
main()