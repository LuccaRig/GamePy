import pygame, sys
import player
import enemy
import map
import camera

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
    enemy1 = enemy.Mobs()
    moving_sprites = pygame.sprite.Group()
    moving_sprites.add(player_character, enemy1)

    myMap = map.Map("Tiled/Mapateste.tmx")
    my_camera = camera.Camera(myMap, player_character, screen)

    while running:

        if not player_character.is_colliding(myMap, "down"):
            player_character.apply_delta_gravity_effect(0.003, myMap)
        if (player_character.is_colliding(myMap, "down")):
            player_character.vertical_speed = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_z]:

            if not (player_character.landing) or not(player_character.is_colliding(myMap, "down")):
                player_character.walking = False
                player_character.attacking = True
            else:
                player_character.animate_land()
                player_character.jumping = False
                player_character.falling = False

        else:
            player_character.walking = False
            enemy1.walking = False
            if player_character.is_colliding(myMap, "down") and not(player_character.attacking):
                player_character.animate_land()
                player_character.jumping = False
                player_character.falling = False
            
        if keys[pygame.K_LEFT]:
            if not player_character.attacking \
                and (not player_character.landing or not(player_character.is_colliding(myMap, "down"))) \
                and not (player_character.is_colliding(myMap, "left")):
                player_character.walking = True
                player_character.update_position(-4, 0)
                #x -= vel

        if keys[pygame.K_RIGHT]:
            if not player_character.attacking \
                and (not player_character.landing or not(player_character.is_colliding(myMap, "down"))) \
                and not (player_character.is_colliding(myMap, "right")):
                player_character.walking = True
                player_character.update_position(4, 0)
                #x += vel

        if keys[pygame.K_UP]:
            if (not player_character.attacking) \
                and (player_character.is_colliding(myMap, "down")) \
                and (not player_character.landing or not(player_character.is_colliding(myMap, "down"))):
                player_character.landing = True
                player_character.jumping = True
                player_character.update_position(0, -25)
                player_character.vertical_speed += player_character.jumping_speed
                    #y -= vel

        if keys[pygame.K_a]:
            enemy1.walking = True
            enemy1.update_position(-2, 0)
                #x -= vel
        if keys[pygame.K_d]:
            enemy1.walking = True
            enemy1.update_position(2, 0)
                #x += vel

        screen.fill((128, 128, 128))

        my_camera.follow_player()
        player_character.draw_collision_rect(screen)
        enemy1.draw_collision_rect(screen)

        moving_sprites.draw(screen)
        moving_sprites.update()

        player_character.animate()
        enemy1.animate()

        moving_sprites.draw(screen)
        moving_sprites.update()

        pygame.display.flip()

        clock.tick(60)

    pygame.quit()
main()