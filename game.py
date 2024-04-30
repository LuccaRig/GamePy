import pygame, sys
import player
import enemy
import camera
import room

class Game():
    def __init__(self) -> None:
        self.clock = pygame.time.Clock()

        pygame.mixer.init()
        pygame.mixer.music.load("assets/Before It Ends.mp3")
        pygame.mixer.music.play()

        # Game Screen
        screen_width = 1280
        screen_height = 720
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("PyGame Game")
        self.running = True

        # Creating Sprites and Groups
        self.player_character = player.Player()
        self.enemy1 = enemy.Mobs()
        self.moving_sprites = pygame.sprite.Group()
        self.moving_sprites.add(self.player_character, self.enemy1)

        self.myRoom = room.Room()
        self.my_camera = camera.Camera(self.myRoom.current_room(), self.player_character, self.screen)

    def game_run(self):

        while self.running:

            #Teste se o player está mudando de sala, e se estiver, atualiza o mapa no vetor de mapas e reinicializa a posição do player e da câmera
            if self.player_character.is_changing_room(self.myRoom.current_room()):
                self.myRoom.change_room()
                self.my_camera = camera.Camera(self.myRoom.current_room(), self.player_character, self.screen)
                self.player_character.reinitialize_position()

            if not self.player_character.is_colliding(self.myRoom.current_room(), "down"):
                self.player_character.apply_delta_gravity_effect(0.003, self.myRoom.current_room())
            if (self.player_character.is_colliding(self.myRoom.current_room(), "down")):
                self.player_character.vertical_speed = 0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                
            keys = pygame.key.get_pressed()
            
            if keys[pygame.K_z]:
                self.player_character.horizontal_speed[0] = 0
                self.player_character.horizontal_speed[1] = 0 

                if not (self.player_character.landing) or not(self.player_character.is_colliding(self.myRoom.current_room(), "down")):
                    self.player_character.walking = False
                    self.player_character.attacking = True
                else:
                    self.player_character.animate_land()
                    self.player_character.jumping = False
                    self.player_character.falling = False

            else:
                self.player_character.walking = False
                self.enemy1.walking = False
                self.player_character.horizontal_speed[0] = 0
                self.player_character.horizontal_speed[1] = 0
                if self.player_character.is_colliding(self.myRoom.current_room(), "down") and not(self.player_character.attacking):
                    self.player_character.animate_land()
                    self.player_character.jumping = False
                    self.player_character.falling = False
                
            if keys[pygame.K_LEFT]:
                if not self.player_character.attacking \
                    and (not self.player_character.landing or not(self.player_character.is_colliding(self.myRoom.current_room(), "down"))) \
                    and not (self.player_character.is_colliding(self.myRoom.current_room(), "left")):
                    self.player_character.walking = True
                    self.player_character.update_position(-4, 0)
                    #x -= vel

            if keys[pygame.K_RIGHT]:
                if not self.player_character.attacking \
                    and (not self.player_character.landing or not(self.player_character.is_colliding(self.myRoom.current_room(), "down"))) \
                    and not (self.player_character.is_colliding(self.myRoom.current_room(), "right")):
                    self.player_character.walking = True
                    self.player_character.update_position(4, 0)
                    #x += vel

            if keys[pygame.K_UP]:
                if (not self.player_character.attacking) \
                    and (self.player_character.is_colliding(self.myRoom.current_room(), "down")) \
                    and (not self.player_character.landing or not(self.player_character.is_colliding(self.myRoom.current_room(), "down"))):
                    self.player_character.landing = True
                    self.player_character.jumping = True
                    self.player_character.update_position(0, -25)
                    self.player_character.vertical_speed += self.player_character.jumping_speed
                        #y -= vel

            if keys[pygame.K_a]:
                self.enemy1.walking = True
                self.enemy1.update_position(-2, 0)
                    #x -= vel
            if keys[pygame.K_d]:
                self.enemy1.walking = True
                self.enemy1.update_position(2, 0)
                    #x += vel

            self.screen.fill((128, 128, 128))

            self.my_camera.follow_player()
            self.player_character.draw_collision_rect(self.screen)
            self.enemy1.draw_collision_rect(self.screen)

            self.moving_sprites.draw(self.screen)
            self.moving_sprites.update()

            self.player_character.animate()
            self.enemy1.animate()

            self.moving_sprites.draw(self.screen)
            self.moving_sprites.update()

            pygame.display.flip()

            self.clock.tick(60)

        pygame.quit()
