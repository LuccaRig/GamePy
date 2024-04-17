import pygame, sys
import player
import enemy
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
    enemy1 = enemy.Mobs()
    moving_sprites = pygame.sprite.Group()
    moving_sprites.add(player_character, enemy1)

    myMap = map.Map("Tiled/Map1.tmx")

    while running:

        if not player_character.isGrounded(myMap):
            player_character.applyDeltaGravityEffect(0.2)
        if (player_character.isGrounded(myMap)):
            player_character.set_vertical_speed(0)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_z]:

            if player_character.landing == False or not(player_character.isGrounded(myMap)): #TODO: Adicionar a variavel que se o player tiver caindo nao pode atacar
                player_character.walking = False
                player_character.attacking = True
        else:
            player_character.walking = False
            if player_character.isGrounded(myMap) and not(player_character.attacking):
                player_character.animate_land()
                player_character.jumping = False
            
        if keys[pygame.K_LEFT]:
            if player_character.attacking == False and (player_character.landing == False or not(player_character.isGrounded(myMap))):
                player_character.walking = True
                player_character.update_position(-3, 0)
                #x -= vel

        if keys[pygame.K_RIGHT]:
            if player_character.attacking == False and (player_character.landing == False or not(player_character.isGrounded(myMap))):
                player_character.walking = True
                player_character.update_position(3, 0)
                #x += vel

        if keys[pygame.K_UP]:
            if (player_character.attacking == False) and (player_character.isGrounded(myMap)) and (player_character.landing == False or not(player_character.isGrounded(myMap))):
                player_character.landing = True
                player_character.jumping = True
                player_character.update_position(0, -10)
                player_character.set_vertical_speed(45)
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

        myMap.renderVisibleLayers(screen)
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