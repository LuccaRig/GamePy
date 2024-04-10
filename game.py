import pygame, sys
import player
import map

def main():
    pygame.init()
    clock = pygame.time.Clock()

    # Game Screen
    screen_width = 1280
    screen_height = 800
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("PyGame Game")
    running = True

    # Creating Sprites and Groups
    player1 = player.Player()
    moving_sprites = pygame.sprite.Group()
    moving_sprites.add(player1)


    myMap = map.Map("Tiled/Map1.tmx")

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_z]:
            player1.walking = False
            player1.attacking = True
            
        elif keys[pygame.K_LEFT]:
            player1.attacking = False
            player1.walking = True
            player1.update_position(-2, 0)
                #x -= vel
        elif keys[pygame.K_RIGHT]:
            player1.attacking = False
            player1.walking = True
            player1.update_position(2, 0)
                #x += vel
        elif keys[pygame.K_UP]:
            player1.attacking = False
            player1.walking = True
            player1.update_position(0, -2)
                #y -= vel
        elif keys[pygame.K_DOWN]:
            if myMap.check_collision(player1.rect) == False:
                player1.attacking = False
                player1.walking = True
                player1.update_position(0, 2)
                    #y += vel
        else:
            player1.walking = False
            player1.attacking = False


        myMap.renderVisibleLayers(screen)
        player1.draw_collision_rect(screen)

        screen.fill((128, 128, 128))
        moving_sprites.draw(screen)
        moving_sprites.update()


        myMap.check_collision(player1.rect)

        player1.animate()

        moving_sprites.draw(screen)
        moving_sprites.update()

        pygame.display.flip()

        clock.tick(60)

    pygame.quit()
main()