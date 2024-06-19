import pygame
import player
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
        self.player = player.Player()
        self.moving_sprites = pygame.sprite.Group()
        self.moving_sprites.add(self.player)

        self.myRoom = room.Room()
        self.my_camera = camera.Camera(self.myRoom.current_room(), self.player, self.screen)
        self.my_camera_off_set_advancing = {}
        self.my_camera_off_set_returning = {}

        # Color of background
        self.rb_dusk = 0
        self.g_dusk = 0
        self.time_passed_in_dusk = 0
        self.background_color = [130, 181, 250]

        # Texts of icons
        self.text_coin = ""
        self.text_coin_pos = [1200, 16]
        self.texts_color = (255, 255, 255)
        self.font_size = 18
        self.text_font = pygame.font.Font('assets/font.ttf', self.font_size)

        self.is_healing_time = 0

    def act_upon_pressed_keys(self, current_time: float) -> None:
        """Toma as ações necessárias a respeito das teclas pressionadas no teclado.

        Permite a movimentação lateral, o pulo, o ataque e o heal. As ações necessárias - como mudanças de variável - para regular 
        as animações e atributos do player e inimigos são tomadas em cada bloco condicional de acordo com a necessidade.
        
        Args:
            current_time: tempo atual fornecido pela biblioteca time
        """
        keys = pygame.key.get_pressed()
            
        if keys[pygame.K_z]:
            self.player.speed[0] = 0
            self.player.speed[1] = 0 

            if not (self.player.landing) and not self.player.was_hit \
                or not(self.player.is_colliding(self.myRoom.current_room(), "down")):
                self.player.walking = False
                self.player.attacking = True
                self.check_dmg_to_enemies(current_time)
                                     
            else:
                self.player.animate_land()
                self.player.jumping = False
                self.player.falling = False

        else:
            self.player.walking = False
            self.player.speed[0] = 0
            self.player.speed[1] = 0
            if self.player.is_colliding(self.myRoom.current_room(), "down") and not(self.player.attacking):
                self.player.animate_land()
                self.player.jumping = False
                self.player.falling = False

        if keys[pygame.K_c]:
            if not self.player.is_healing and (current_time - self.is_healing_time >= 0.2) and self.player.is_alive:
                self.player.is_healing = True
                self.player.number_of_heals -= 1
                if self.player.number_of_heals >= 0:
                    self.player.heal()
                    self.player.hp_bar_change()
            if current_time - self.is_healing_time >= 0.2:
                self.player.is_healing = False
            if not self.player.is_healing:
                self.is_healing_time = time.time()
                
        if keys[pygame.K_LEFT]:
            if not self.player_character.attacking and not self.player_character.was_hit and not keys[pygame.K_RIGHT]\
                and (not self.player_character.landing or not(self.player_character.is_colliding(self.myRoom.current_room(), "down"))) \
                and not (self.player_character.is_colliding(self.myRoom.current_room(), "left")) and self.player_character.is_alive:
                self.player_character.walking = True
                self.player_character.update_position(-4, 0)
                #x -= vel

        if keys[pygame.K_RIGHT]:
            if not self.player_character.attacking and not self.player_character.was_hit and not keys[pygame.K_LEFT]\
                and (not self.player_character.landing or not(self.player_character.is_colliding(self.myRoom.current_room(), "down"))) \
                and not (self.player_character.is_colliding(self.myRoom.current_room(), "right")) and self.player_character.is_alive:
                self.player_character.walking = True
                self.player_character.update_position(4, 0)
                #x += vel

        if keys[pygame.K_UP]:
            if not self.player.attacking and not self.player.was_hit and self.player.is_alive\
                and (self.player.is_colliding(self.myRoom.current_room(), "down")) \
                and (not self.player.landing or not(self.player.is_colliding(self.myRoom.current_room(), "down"))):
                self.player.landing = True
                self.player.jumping = True
                self.player.update_position(0, -25)
                self.player.vertical_speed += self.player.jumping_speed
                    #y -= vel

    def check_dmg_to_player(self, current_time: float) -> None:
        """Checa por dano de contato ou de ataque de um inimigo e aplica o dano válido que for detectado.

        Aplica o flinch e animação de hit do player e atualiza a barra de vida no caso de subtração de hp.

        Args:
            current_time: tempo atual fornecido pela biblioteca time
        """
        if self.myRoom.current_room_enemies() != None:
                for enemy in self.myRoom.current_room_enemies().enemy_vector:
                    if enemy.is_alive:
                        rects_intersected = False
                        if self.player.hitbox_rect.colliderect(enemy.hitbox_rect):
                            damage_received = enemy.contact_dmg
                            rects_intersected = True
                        if enemy.has_attack_rect and enemy.is_atk():
                            if self.player.hitbox_rect.colliderect(enemy.attack_rect):
                                damage_received = enemy.attack_dmg
                                rects_intersected = True
                        
                        if current_time - self.player.last_hit_time > 1.4 and rects_intersected:
                            self.player.hp -= damage_received
                            self.player.hp_bar_change()
                            self.player.was_hit = True
                            self.player.hit_flinch = True
                            self.player.last_hit_time = time.time()
                            print("HP do jogador:", self.player.hp)
                            break
            
    def check_dmg_to_enemies(self, current_time: float) -> None:
        """Testa se o ataque do player pode tirar vida de um inimigo e, se sim, o faz
        
        Função auxiliar de self.act_upon_pressed_keys()
        Caso um inimigo seja derrotado, a quantidade de moedas dele é adicionada ao número de moedas do jogador
        Pré-condição para a chamada de função: o player está atacando

        Args:
            current_time: tempo atual fornecido pela biblioteca time
        """
        hit_was_successfull = False
        for enemy in self.myRoom.current_room_enemies().enemy_vector:
            if enemy.is_alive:
                if (self.player.right_attack_rect.colliderect(enemy.hitbox_rect) and (self.player.direction == "right") or \
                 self.player.left_attack_rect.colliderect(enemy.hitbox_rect) and (self.player.direction == "left")):
                    if current_time - self.player.last_landed_attack_time > 0.5:
                        enemy.hp -= self.player.attack_dmg
                        enemy.was_hit = True
                        if enemy.hp <= 0:
                            self.player.coins += enemy.coins_value
                        hit_was_successfull = True
                        print("HP do inimigo: ", enemy.hp)
        if hit_was_successfull:
            self.player.last_landed_attack_time = time.time()

    def fill_background(self, current_time: float) -> None:
        """Preenche a cor da background dinamicamente
        """
        is_it_dusk = False
        if (current_time - self.time_passed_in_dusk >= 1) and (self.myRoom.current_map_position <= 7):
            if self.rb_dusk <= 124:
                self.rb_dusk += 1
            if self.g_dusk <= 180:
                self.g_dusk += 1
            self.background_color = [130+self.rb_dusk, 181-self.g_dusk, 250-2*self.rb_dusk]
            is_it_dusk = True
        elif self.myRoom.current_map_position == 8:
            self.background_color = [64, 64, 64]
        if is_it_dusk:
            self.time_passed_in_dusk = time.time()
        self.screen.fill(self.background_color)

    def control_player(self, current_time: float) -> None:
        """Atualiza as animações do player e desenha elas na tela, movimentando a câmera de acordo
        """
        self.my_camera.follow_player()

        #atualiza todas animações
        self.player.draw_collision_rect(self.screen)
        self.player.animate_hit()
        self.player.animate()
        if self.player.hp <= 0:
            self.player.dying = True
            self.player.is_alive = False
            self.player.is_animating = False
        self.player.animate_death()

        #permite que o player "pisque" após ter tomado dano, indicando período de invincibilidade
        invincibility_time = current_time - self.player.last_hit_time
        if (0.2 <= invincibility_time <= 0.4) or (0.6 <= invincibility_time <= 0.8) or (1 <= invincibility_time <= 1.2):
            self.player.is_invisible_by_invincibility = True
        else:
            self.player.is_invisible_by_invincibility = False

        #desenha o player na tela
        if self.player.dying or not self.player.is_invisible_by_invincibility:
            self.moving_sprites.draw(self.screen)
        self.moving_sprites.update()

    def control_enemy_group(self) -> None:
        """Atualiza as animações de todos os inimigos e desenha elas na tela, atualizando a câmera de acordo
        """
        if self.myRoom.current_room_enemies() != None:
            self.myRoom.current_room_enemies().follow_player(self.player.pos_x, self.my_camera.off_set_x)
            self.myRoom.current_room_enemies().set_move_sets()
            self.my_camera.keep_enemy_pos(self.screen, self.myRoom.current_room_enemies())
            self.myRoom.current_room_enemies().update_enemies_sprites()
            self.myRoom.current_room_enemies().draw_collisions_rects(self.screen)
            self.myRoom.current_room_enemies().check_deaths()
            self.myRoom.current_room_enemies().animate_deaths()
            self.myRoom.current_room_enemies().animate_hits()
            self.myRoom.current_room_enemies().destruct_dead_enemies()

    def control_npc(self) -> None:
        """Atualiza as animações do npc e desenha elas na tela, atualizando a câmera de acordo
        """
        if self.myRoom.current_room_npc() != None:
            self.my_camera.keep_npc_pos(self.screen, self.myRoom.current_room_npc())
            self.myRoom.current_room_npc().talk_to_player(self.player, self.screen)
            self.myRoom.current_room_npc().animate()
            self.myRoom.current_room_npc().update()

    def apply_gravity_to_player(self) -> None:
        """Aplica gravidade ao player e garante que ele caia no chão corretamente
        """
        if not self.player.is_colliding(self.myRoom.current_room(), "down"):
            self.player.apply_delta_gravity_effect(0.003, self.myRoom.current_room())
        else:
            self.player.correct_ground_intersection(self.myRoom.current_room())
        if (self.player.is_colliding(self.myRoom.current_room(), "down")):
            self.player.vertical_speed = 0

    def control_rooms_player_position(self) -> None:
        """Atualiza a posição da câmera e do player ao mudar de sala
        """
        #Testa se o player está avançando para a nova sala, e se estiver
        # atualiza o mapa no vetor de mapas e reinicializa a posição do player e da câmera
        if self.player.is_advancing_room(self.myRoom.current_room()):
            #Armazena o quanto a câmera se deslocou, para a reinicialização dessa quando retornando para a sala
            player_pos_y = self.player.pos_y
            self.my_camera_off_set_advancing[self.myRoom.current_map_position] = [self.my_camera.off_set_x, self.my_camera.off_set_y]

            self.myRoom.advance_room()
            self.my_camera = camera.Camera(self.myRoom.current_room(), self.player, self.screen)
            self.my_camera.off_set_map(0, self.my_camera_off_set_advancing[self.myRoom.current_map_position-1][1])
            self.player.reinitialize_position_advancing(self.myRoom.current_room(), player_pos_y)

        #Testa se o player está voltando para a sala anterior, e se estiver
        #atualiza o mapa no vetor de mapas e reinicializa a posição do player e da câmera
        if self.player.is_returning_room(self.myRoom.current_room()):
            player_pos_y = self.player.pos_y
            self.my_camera_off_set_returning[self.myRoom.current_map_position] = [self.my_camera.off_set_x, self.my_camera.off_set_y]

            self.myRoom.return_room()
            self.my_camera = camera.Camera(self.myRoom.current_room(), self.player, self.screen)
            self.my_camera.off_set_map(self.my_camera_off_set_advancing[self.myRoom.current_map_position][0], 
                                        self.my_camera_off_set_returning[self.myRoom.current_map_position+1][1])
            self.player.reinitialize_position_returning(self.myRoom.current_room(), 
                                                                    self.my_camera_off_set_advancing[self.myRoom.current_map_position][0],
                                                                    player_pos_y)

    def draw_hp_bar_and_coins(self, text_coin_render):
        """Desenha a barra de hp e o símbolo de moedas
        """
        self.screen.blit(self.player.hp_bar_background, (10, 10))
        for heal in range(self.player.number_of_heals):
            self.screen.blit(self.player.heal_icon, (30+heal*20, 65))
        self.screen.blit(self.player.coin_icon, (1165, 10))
        self.screen.blit(text_coin_render, self.text_coin_pos)
        pygame.draw.rect(self.screen, (192, 0, 0), self.player.hp_bar)
    

    def game_run(self):

        while self.running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            current_time = time.time()
            self.text_coin = str(self.player.coins)
            text_coin_render = self.text_font.render(self.text_coin, True, self.texts_color)
            
            self.control_rooms_player_position()

            self.apply_gravity_to_player()

            self.act_upon_pressed_keys(current_time)

            self.check_dmg_to_player(current_time)

            self.fill_background(current_time)

            self.control_player(current_time)

            self.control_enemy_group()

            self.control_npc()

            self.draw_hp_bar_and_coins(text_coin_render)

            #não apagar de forma alguma, está repetido mas por algum motivo é necessário para o jogo não travar
            if self.player.dying or not self.player.is_invisible_by_invincibility:
                self.moving_sprites.draw(self.screen)
            self.moving_sprites.update()

            pygame.display.flip()

            self.clock.tick(60)

        pygame.quit()


# Apenas existe para ser possivel rodar a Game Sem utilizar o menu
if __name__ ==  '__main__':
    my_game = Game()
    my_game.game_run()