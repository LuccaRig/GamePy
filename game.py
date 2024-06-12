import pygame
import player
import enemy
import camera
import room
import time

class Game():
    def __init__(self) -> None:
        self.clock = pygame.time.Clock()

        pygame.font.init()
        pygame.mixer.init()
        #pygame.mixer.music.load("assets/Before It Ends.mp3")
        #pygame.mixer.music.play()

        # Game Screen
        screen_width = 1280
        screen_height = 720
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("PyGame Game")
        self.running = True

        # Creating Sprites and Groups
        self.player_character = player.Player()
        self.moving_sprites = pygame.sprite.Group()
        self.moving_sprites.add(self.player_character)

        self.myRoom = room.Room()
        self.my_camera = camera.Camera(self.myRoom.current_room(), self.player_character, self.screen)
        self.my_camera_off_set = {}

        self.rb_dusk = 0
        self.g_dusk = 0
        self.time_passed_in_dusk = 0
        self.background_color = [130, 181, 250]


    def game_run(self):

        while self.running:

            #print(self.player_character.pos_x, self.player_character.pos_y)
            #print(self.my_camera_off_set)
            #print(self.myRoom.is_first_time)
            current_time = time.time()
            
            #Testa se o player está avançando para a nova sala, e se estiver
            # atualiza o mapa no vetor de mapas e reinicializa a posição do player e da câmera
            if self.player_character.is_advancing_room(self.myRoom.current_room()):
                #Armazena o quanto a câmera se deslocou, para a reinicialização dessa quando retornando para a sala
                self.player_character.pos_x_returning_room = self.my_camera.off_set_x
                self.player_character.pos_y_returning_room = self.my_camera.off_set_y
                self.my_camera_off_set[self.myRoom.current_map_position] = [self.my_camera.off_set_x, self.my_camera.off_set_y]

                self.myRoom.advance_room()
                self.my_camera = camera.Camera(self.myRoom.current_room(), self.player_character, self.screen)
                self.my_camera.off_set_map(0, self.my_camera_off_set[self.myRoom.current_map_position-1][1])
                self.player_character.reinitialize_position_advancing(self.myRoom.current_room())

            #Testa se o player está voltando para a sala anterior, e se estiver
            #atualiza o mapa no vetor de mapas e reinicializa a posição do player e da câmera
            if self.player_character.is_returning_room(self.myRoom.current_room()):
                self.myRoom.return_room()
                self.my_camera = camera.Camera(self.myRoom.current_room(), self.player_character, self.screen)
                self.my_camera.off_set_map(self.my_camera_off_set[self.myRoom.current_map_position][0], 
                                           self.my_camera_off_set[self.myRoom.current_map_position][1])
                self.player_character.reinitialize_position_returning(self.myRoom.current_room(), self.my_camera_off_set[self.myRoom.current_map_position][0])

            if not self.player_character.is_colliding(self.myRoom.current_room(), "down"):
                self.player_character.apply_delta_gravity_effect(0.003, self.myRoom.current_room())
            else:
                self.player_character.correct_ground_intersection(self.myRoom.current_room())
            if (self.player_character.is_colliding(self.myRoom.current_room(), "down")):
                self.player_character.vertical_speed = 0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                
            keys = pygame.key.get_pressed()
            
            if keys[pygame.K_z]:
                self.player_character.speed[0] = 0
                self.player_character.speed[1] = 0 

                if not (self.player_character.landing) or not(self.player_character.is_colliding(self.myRoom.current_room(), "down")):
                    self.player_character.walking = False
                    self.player_character.attacking = True
                    #testa se o ataque pode tirar vida de um inimigo e, se sim, o faz
                    hit_was_successfull = False
                    for enemy in self.myRoom.current_room_enemies().enemy_vector:
                        if enemy.is_alive:
                            if (self.player_character.right_attack_rect.colliderect(enemy.hitbox_rect) and (self.player_character.direction == "right") or \
                             self.player_character.left_attack_rect.colliderect(enemy.hitbox_rect) and (self.player_character.direction == "left")):
                                if current_time - self.player_character.last_landed_attack_time > 0.48:
                                    enemy.hp -= self.player_character.attack_dmg
                                    enemy.was_hit = True
                                    hit_was_successfull = True
                                    print("HP do inimigo: ", enemy.hp)
                    if hit_was_successfull:
                        self.player_character.last_landed_attack_time = time.time()
                                     
                else:
                    self.player_character.animate_land()
                    self.player_character.jumping = False
                    self.player_character.falling = False

            else:
                self.player_character.walking = False
                self.player_character.speed[0] = 0
                self.player_character.speed[1] = 0
                if self.player_character.is_colliding(self.myRoom.current_room(), "down") and not(self.player_character.attacking):
                    self.player_character.animate_land()
                    self.player_character.jumping = False
                    self.player_character.falling = False
                
            if keys[pygame.K_LEFT]:
                if not self.player_character.attacking and not keys[pygame.K_RIGHT]\
                    and (not self.player_character.landing or not(self.player_character.is_colliding(self.myRoom.current_room(), "down"))) \
                    and not (self.player_character.is_colliding(self.myRoom.current_room(), "left")):
                    self.player_character.walking = True
                    self.player_character.update_position(-6, 0)
                    #x -= vel

            if keys[pygame.K_RIGHT]:
                if not self.player_character.attacking and not keys[pygame.K_LEFT]\
                    and (not self.player_character.landing or not(self.player_character.is_colliding(self.myRoom.current_room(), "down"))) \
                    and not (self.player_character.is_colliding(self.myRoom.current_room(), "right")):
                    self.player_character.walking = True
                    self.player_character.update_position(6, 0)
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

            #checa se o jogador deve receber dano de contato
            if self.myRoom.current_room_enemies() != None:
                for enemy in self.myRoom.current_room_enemies().enemy_vector:
                    if enemy.is_alive:
                        if self.player_character.hitbox_rect.colliderect(enemy.hitbox_rect):
                            if current_time - self.player_character.last_hit_time > 1.3:
                                self.player_character.hp -= enemy.contact_dmg
                                self.player_character.hp_bar_change()
                                self.player_character.last_hit_time = time.time()
                                print("HP do jogador:", self.player_character.hp)
                                break

            is_it_dusk = False
            if current_time - self.time_passed_in_dusk >= 1:
                if self.rb_dusk <= 124:
                    self.rb_dusk += 1
                if self.g_dusk <= 180:
                    self.g_dusk +=1
                self.background_color = [130+self.rb_dusk, 181-self.g_dusk, 250-2*self.rb_dusk]
                is_it_dusk = True
            if is_it_dusk:
                self.time_passed_in_dusk = time.time()
            self.screen.fill(self.background_color)

            self.my_camera.follow_player()
            self.player_character.draw_collision_rect(self.screen)

            self.moving_sprites.draw(self.screen)
            self.moving_sprites.update()

            self.player_character.animate()

            if self.myRoom.current_room_npc() != None:
                self.my_camera.keep_npc_pos(self.screen, self.myRoom.current_room_npc())
                self.myRoom.current_room_npc().talk_to_player(self.player_character, self.screen)
                self.myRoom.current_room_npc().animate()
                self.myRoom.current_room_npc().update()

            if self.myRoom.current_room_enemies() != None:
                self.myRoom.current_room_enemies().set_move_sets()
                self.my_camera.keep_enemy_pos(self.screen, self.myRoom.current_room_enemies())
                self.myRoom.current_room_enemies().update_enemies_sprites()
                self.myRoom.current_room_enemies().draw_collisions_rects(self.screen)
                self.myRoom.current_room_enemies().check_deaths()
                self.myRoom.current_room_enemies().animate_deaths()
                self.myRoom.current_room_enemies().animate_hits()
                self.myRoom.current_room_enemies().destruct_dead_enemies()

            self.moving_sprites.draw(self.screen)
            self.moving_sprites.update()
            self.screen.blit(self.player_character.hp_bar_background, (10, 10))
            pygame.draw.rect(self.screen, (192, 0, 0), self.player_character.hp_bar)

            pygame.display.flip()

            self.clock.tick(60)

        pygame.quit()


# Apenas existe para ser possivel rodar a Game Sem utilizar o menu
if __name__ ==  '__main__':
    my_game = Game()
    my_game.game_run()