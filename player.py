from Interfaces.playerinterface import PlayerInterface
import pygame, sys
import map

class Player(PlayerInterface, pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        # Sprite Vectors
        self.__sprites_idle_right = []
        self.__sprites_idle_left = []

        self.__sprites_moving_right = []
        self.__sprites_moving_left = []

        self.__sprites_hit_right = []
        self.__sprites_hit_left = []

        self.__sprites_attacking_right = []
        self.__sprites_attacking_left = []

        self.__sprites_jumping_right = []
        self.__sprites_jumping_left = []

        self.__sprites_falling_right = []
        self.__sprites_falling_left = []

        self.__sprites_landing_right = []
        self.__sprites_landing_left = []

        self.__sprites_dying_right = []
        self.__sprites_dying_left = []

        # Load All Sprites
        self.__import_sprites(9,'CharacterSprites/assassin/idlePNGright', self.__sprites_idle_right)
        self.__import_sprites(9,'CharacterSprites/assassin/idlePNGleft', self.__sprites_idle_left)    
        self.__import_sprites(8,'CharacterSprites/assassin/movementPNGright', self.__sprites_moving_right)
        self.__import_sprites(8,'CharacterSprites/assassin/movementPNGleft', self.__sprites_moving_left)
        self.__import_sprites(2,'CharacterSprites/assassin/hitPNGright', self.__sprites_hit_right)
        self.__import_sprites(2,'CharacterSprites/assassin/hitPNGleft', self.__sprites_hit_left)    
        self.__import_sprites(9,'CharacterSprites/assassin/attackPNGright', self.__sprites_attacking_right)
        self.__import_sprites(9,'CharacterSprites/assassin/attackPNGleft', self.__sprites_attacking_left)
        self.__import_sprites(4, 'CharacterSprites/assassin/jumpPNGright', self.__sprites_jumping_right)
        self.__import_sprites(4, 'CharacterSprites/assassin/jumpPNGleft', self.__sprites_jumping_left)
        self.__import_sprites(4, 'CharacterSprites/assassin/fallPNGright', self.__sprites_falling_right)
        self.__import_sprites(4, 'CharacterSprites/assassin/fallPNGleft', self.__sprites_falling_left)
        self.__import_sprites(4, 'CharacterSprites/assassin/landPNGright', self.__sprites_landing_right)
        self.__import_sprites(4, 'CharacterSprites/assassin/landPNGleft', self.__sprites_landing_left)
        self.__import_sprites(4, 'CharacterSprites/assassin/deathPNGright', self.__sprites_dying_right)
        self.__import_sprites(4, 'CharacterSprites/assassin/deathPNGleft', self.__sprites_dying_left)

        # Default Boolean and Character States
        self.is_animating = False
        self.is_alive = True
        self.is_healing = False
        self.attacking = False
        self.walking = False
        self.grounded = False
        self.jumping = False
        self.landing = False
        self.falling = False
        self.dying = False
        self.was_hit = False
        self.hit_flinch = False
        self.is_invisible_by_invincibility = False
        self.direction = "right"
        self.current_sprite = 0
        self.current_sprite_attack = 0
        self.current_sprite_jump = 0
        self.current_sprite_land = 0
        self.current_sprite_death = 0
        self.current_sprite_hit = 0
        self.image = self.__sprites_idle_right[self.current_sprite]     

        # Default Position and movement
        self.jumping_speed = 2750
        self.vertical_speed = 0
        self.gravity_ = 25000
        self.pos_x = 0
        self.pos_y = 360
        self.width = 200
        self.height = 77
        self.rect_down = pygame.Rect(self.pos_x+85, self.pos_y+47,  30, 30)
        self.rect_up = pygame.Rect(self.pos_x+85, self.pos_y,  30, 10)
        self.rect_right = pygame.Rect(self.pos_x+121, self.pos_y, 2, 75)  
        self.rect_left = pygame.Rect(self.pos_x+77, self.pos_y, 2, 75)
        self.hitbox_rect = pygame.Rect(self.pos_x, self.pos_y, 45, self.height-5) 
        self.right_attack_rect = pygame.Rect(self.pos_x+45, self.pos_y, 65, self.height-5)  
        self.left_attack_rect = pygame.Rect(self.pos_x-45, self.pos_y, 65, self.height-5) 
        self.rect = pygame.Rect(self.pos_x, self.pos_y,  self.width, self.height)
        self.rect.topleft = [self.pos_x, self.pos_y]
        self.speed = [0.0, 0.0]
        self.max_horizontal_speed = 8
        self.delta_pos_y = 0
        self.x_limit_reached = False
        self.y_limit_reached = False
        self.hp_bar = pygame.Rect(28, 16, 200, 40)
        self.hp_bar_background = pygame.image.load('assets/HUD HP_BAR.png')
        self.heal_icon = pygame.image.load('assets/Heal_Icon.png')
        self.heal_icon = pygame.transform.scale(self.heal_icon, 
                                                (int(self.heal_icon.get_width() * 4), int(self.heal_icon.get_height() * 4)))
        self.coin_icon = pygame.image.load('assets/Coin_Icon.png')
        self.coin_icon = pygame.transform.scale(self.coin_icon, 
                                                (int(self.coin_icon.get_width() * 3), int(self.coin_icon.get_height() * 3)))

        # Stats
        self.attack_dmg = 15
        self.max_hp = 50
        self.hp = 50
        self.number_of_heals = 3
        self.coins = 0

        self.last_hit_time = 0
        self.last_landed_attack_time = 0
        
    #TODO: TERMINAR O DOCSTRING
    def __import_sprites(self, number_of_sprites: int, arquive: str, sprites_vector: list) -> None:

        """ Acessa a pasta selecionada {arquive} e guarda os PNG em um vetores de PNG {sprites_vector}.

        Args:
            number_of_sprites: número de sprites da animação específica do sprites_vector enviado como parâmetro
            arquive: nome do arquivo relacionado ao grupo de sprites que será importado para o sprites_vector
            sprites_vector: vetor de sprites para onde serão importados os sprites
    
        """
        scale = 4
        for i in range(number_of_sprites):
            sprite = pygame.image.load(f'{arquive}/tile00{i}.png')
            # Scale the sprite
            sprite = pygame.transform.scale(sprite, (int(sprite.get_width() * scale), int(sprite.get_height() * scale)))
            sprites_vector.append(sprite)
        
    def hp_bar_change(self) -> None:
        hp_bar_lost = self.max_hp - self.hp
        self.hp_bar = pygame.Rect(28, 16, (self.max_hp-hp_bar_lost)*4, 40)

    def heal(self) -> None:
        self.hp += self.max_hp*0.6
        if self.max_hp <= self.hp:
            self.hp = self.max_hp

    def reinitialize_position_advancing(self, map: map, pos_y: int) -> None:
        """Ajusta a posição do player para a nova sala

        Args:
            map: objeto que contém os blocos de colisão para ajuste do player
        """
        self.pos_x = map.pos_x_previous_room - 50
        self.pos_y = pos_y
        self.rect.topleft = [self.pos_x, self.pos_y]
        self.rect_down.topleft = [self.pos_x+85, self.pos_y+47]
        self.rect_up.topleft = [self.pos_x+85, self.pos_y]
        self.rect_right.topleft = [self.pos_x+121, self.pos_y]
        self.rect_left.topleft = [self.pos_x+77, self.pos_y]
        self.hitbox_rect.topleft = [self.pos_x+77, self.pos_y]
        self.right_attack_rect.topleft = [self.pos_x+110, self.pos_y]
        self.left_attack_rect.topleft = [self.pos_x+25, self.pos_y]

    def reinitialize_position_returning(self, map: map, off_set_x: int, pos_y: int) -> None:
        """Ajusta a posição do player para a sala anterior

        Args:
            map: objeto que contém os blocos de colisão para ajuste do player
        """
        self.pos_x = map.pos_x_new_room - 110 + off_set_x
        self.pos_y = pos_y
        self.rect.topleft = [self.pos_x, self.pos_y]
        self.rect_down.topleft = [self.pos_x+85, self.pos_y+47]
        self.rect_up.topleft = [self.pos_x+85, self.pos_y]
        self.rect_right.topleft = [self.pos_x+121, self.pos_y]
        self.rect_left.topleft = [self.pos_x+77, self.pos_y]
        self.hitbox_rect.topleft = [self.pos_x+77, self.pos_y]
        self.right_attack_rect.topleft = [self.pos_x+110, self.pos_y]
        self.left_attack_rect.topleft = [self.pos_x+25, self.pos_y]

    def update_position(self, new_pos_x: int, new_pos_y: int) -> None:
        """ Muda a posição do Rect do player e a posição dos seu rects direcionais

        Args:
            new_pos_x: valor a ser somado à posição da direção horizontal
            new_pos_y: o mesmo, porém à direção vertical
        """
        self.speed[0] = new_pos_x
        self.speed[1] = new_pos_y
        if self.walking or self.jumping or not self.grounded:
            if(new_pos_x < 0 ):
                self.direction = "left"
            if(new_pos_x > 0):
                self.direction = "right"
            if not(((self.rect.topleft[0] <= 400) and self.direction == "left") or ((self.rect.topleft[0] >= 720) and self.direction == "right")) or (self.x_limit_reached):
                self.pos_x += self.speed[0]
            if not(((self.rect.topleft[1] >= 350) and self.falling) or (self.rect.topleft[1] <= 200 and self.vertical_speed > 0)) or (self.y_limit_reached):
                self.pos_y += self.speed[1]
            self.rect.topleft = [self.pos_x, self.pos_y]
            self.rect_down.topleft = [self.pos_x+85, self.pos_y+47]
            self.rect_up.topleft = [self.pos_x+85, self.pos_y]
            self.rect_right.topleft = [self.pos_x+121, self.pos_y]
            self.rect_left.topleft = [self.pos_x+77, self.pos_y]
            self.hitbox_rect.topleft = [self.pos_x+77, self.pos_y]
            self.right_attack_rect.topleft = [self.pos_x+110, self.pos_y]
            self.left_attack_rect.topleft = [self.pos_x+25, self.pos_y]
    

    def apply_delta_gravity_effect(self, delta_t: float, map: map) -> None:
        """Modifica a posição vertical do jogador de acordo com as leis da gravidade no tempo delta_t.

        Args:
            delta_t: tempo que determina o delta posição 
        """
        self.delta_pos_y = self.vertical_speed*delta_t - self.gravity_*delta_t*delta_t/2 
        #delta(X) = Vot - g(t^2)/2
        self.vertical_speed -= self.gravity_*delta_t
         #V = Vo - gt
        if self.is_colliding(map, "up"):
            self.vertical_speed = 0
            self.update_position(0, 5)
        else:
            self.update_position(0, -self.delta_pos_y)

    def correct_ground_intersection(self, map: map) -> None:
        """Coloca o player precisamente acima do chão após uma queda.

        Args:
            map: objeto capaz de retornar a interseção entre o rect inferior do player e o rect do chão.
        """
        intersection_rect = map.return_ground_intersection(self.rect_down)
        if intersection_rect.height > 1:
            self.update_position(0, -intersection_rect.height+1)
    
    def is_colliding(self, map: map, direction: str) -> bool:
        """Retorna True se o player estiver colidindo na direção enviada
        
        Args:
            map: objeto que contém função capaz de checar colisões 
            direction: determina em que direção deve ser testada a colisão. Envie "right", "left", "up" ou "down".
        """
        if direction == "right":
            return map.check_collision(self.rect_right)
        elif direction == "left":
            return map.check_collision(self.rect_left)
        elif direction == "up":
            return map.check_collision(self.rect_up)
        elif direction == "down":
            return map.check_collision(self.rect_down)
        
    def is_advancing_room(self, map: map) -> bool:
        """Retorna True se o player estiver avançando para a próxima sala
        
        Args:
            map: objeto que contém função capaz de checar colisões
        """

        if self.direction == "right":
            return map.check_new_room(self.hitbox_rect)
        if (self.direction == "left") and (not self.walking):
            return map.check_new_room(self.hitbox_rect)
    
    def is_returning_room(self, map: map) -> bool:
        """Retorna True se o player estiver voltando para a sala anterior
        
        Args:
            map: objeto que contém função capaz de checar colisões
        """

        if self.direction == "left":
            return map.check_previous_room(self.hitbox_rect)
        if (self.direction == "right") and (not self.walking):
            return map.check_new_room(self.hitbox_rect)

    def animate_attack(self) -> None:
        """Anima o ataque do player.
        """
        animation_speed = 0.15
        self.current_sprite_attack += animation_speed
        if self.direction == "right":
            if self.current_sprite_attack >= len(self.__sprites_attacking_right):
                self.current_sprite_attack = 0
                self.is_animating = False
                self.attacking = False
            else:
                self.image = self.__sprites_attacking_right[int(self.current_sprite_attack)]

        elif self.direction == "left":
            if self.current_sprite_attack >= len(self.__sprites_attacking_left):
                self.current_sprite_attack = 0
                self.is_animating = False
                self.attacking = False
            else:
                self.image = self.__sprites_attacking_left[int(self.current_sprite_attack)]

    def animate_land(self) -> None:
        """Atualiza os sprites do player para ele cair no chão com a animação correta
        """
        if self.landing:    
            animation_speed = 0.3
            self.current_sprite_land += animation_speed
            if self.direction == "right":
                if self.current_sprite_land >= len(self.__sprites_landing_right):
                    self.current_sprite_land = 0
                    self.is_animating = False
                    self.landing = False
                else:
                    self.image = self.__sprites_landing_right[int(self.current_sprite_land)]

            elif self.direction == "left":
                if self.current_sprite_land >= len(self.__sprites_landing_left):
                    self.current_sprite_land = 0
                    self.is_animating = False
                    self.landing = False
                else:
                    self.image = self.__sprites_landing_left[int(self.current_sprite_land)]

    def animate_death(self) -> None:
        """Anima a morte do player e chama o game over
        """
        if self.dying:    
            animation_speed = 0.05
            self.current_sprite_death += animation_speed
            if self.direction == "right":
                if self.current_sprite_death >= len(self.__sprites_dying_right):
                    self.current_sprite_death = 0
                    self.dying = False
                    pygame.quit()
                    sys.exit()
                else:
                    self.image = self.__sprites_dying_right[int(self.current_sprite_death)]

            elif self.direction == "left":
                if self.current_sprite_death >= len(self.__sprites_dying_left):
                    self.current_sprite_death = 0
                    self.dying = False
                    pygame.quit()
                    sys.exit()
                else:
                    self.image = self.__sprites_dying_left[int(self.current_sprite_death)]

    def animate_hit(self) -> None:
        """Anima o player tomando um hit e dando um flinch para trás
        """
        if self.was_hit:    
            animation_speed = 0.1
            self.current_sprite_hit += animation_speed
            if self.direction == "right":
                if self.hit_flinch:
                    self.update_position(-30, 0)
                    self.update_position(1, 0)
                    self.hit_flinch = False
                if self.current_sprite_hit >= len(self.__sprites_hit_right):
                    self.current_sprite_hit = 0
                    self.was_hit = False
                else:
                    self.image = self.__sprites_hit_right[int(self.current_sprite_hit)]

            elif self.direction == "left":
                if self.hit_flinch:
                    self.update_position(30, 0)
                    self.update_position(-1, 0)
                    self.hit_flinch = False
                if self.current_sprite_hit >= len(self.__sprites_hit_left):
                    self.current_sprite_hit = 0
                    self.was_hit = False
                else:
                    self.image = self.__sprites_hit_left[int(self.current_sprite_hit)]
         
    def animate(self) -> None:
        self.is_animating = True
    
    #TODO: FAZER A DOCSTRING
    def update(self) -> None:
        """Atualiza 
        """
        if self.is_alive and not self.was_hit:
            animation_speed = 0
            if self.walking:
                animation_speed = 0.10
            if not self.walking:
                animation_speed = 0.20

            if  self.is_animating:
                self.current_sprite += animation_speed
                if self.vertical_speed < 0:
                    self.falling = True

                if(self.direction == "right"):
                    if self.attacking:
                        self.animate_attack()

                    elif self.falling and not self.attacking:
                        if self.current_sprite >= len(self.__sprites_falling_right):
                            self.current_sprite = 0
                            self.is_animating = False
                        self.image = self.__sprites_falling_right[int(self.current_sprite)]
                    
                    elif self.jumping:
                        if self.current_sprite >= len(self.__sprites_jumping_right):
                            self.current_sprite = 0
                            self.is_animating = False
                        self.image = self.__sprites_jumping_right[int(self.current_sprite)]

                    elif self.walking and not self.landing:
                        if self.current_sprite >= len(self.__sprites_moving_right):
                            self.current_sprite = 0
                            self.is_animating = False
                        self.image = self.__sprites_moving_right[int(self.current_sprite)]

                    elif not self.walking and not self.landing:
                        if self.current_sprite >= len(self.__sprites_idle_right):
                            self.current_sprite = 0
                            self.is_animating = False
                        self.image = self.__sprites_idle_right[int(self.current_sprite)]


                if(self.direction == "left"):
                    if self.attacking:
                        self.animate_attack()

                    elif self.falling and not self.attacking:
                        if self.current_sprite >= len(self.__sprites_falling_left):
                            self.current_sprite = 0
                            self.is_animating = False
                        self.image = self.__sprites_falling_left[int(self.current_sprite)]

                    elif self.jumping:
                        if self.current_sprite >= len(self.__sprites_jumping_left):
                            self.current_sprite = 0
                            self.is_animating = False
                        self.image = self.__sprites_jumping_left[int(self.current_sprite)]

                    elif self.walking and not self.landing:
                        if self.current_sprite >= len(self.__sprites_moving_left):
                            self.current_sprite = 0
                            self.is_animating = False
                        self.image = self.__sprites_moving_left[int(self.current_sprite)]

                    elif not self.walking and not self.landing:
                        if self.current_sprite >= len(self.__sprites_idle_left):
                            self.current_sprite = 0
                            self.is_animating = False
                        self.image = self.__sprites_idle_left[int(self.current_sprite)]
                
    def draw_collision_rect(self, screen: pygame.display) -> None:
        """Desenha os rects do player na tela.

        Função com uso estrito para testes relacionados aos rects do player.
        """
        # Desenha um retângulo vermelho em torno do retângulo do jogador
        green = (0, 255, 0)
        red = (255, 0, 0)
        white = (255, 255, 255)
        black = (0,0,0)
        #pygame.draw.rect(screen, yellow, self.rect, 1)
        #pygame.draw.rect(screen, black, self.rect_down, 1)
        #pygame.draw.rect(screen, white, self.hitbox_rect, 1)
        #pygame.draw.rect(screen, red, self.right_attack_rect, 1)
        #pygame.draw.rect(screen, red, self.left_attack_rect, 1)

        #pygame.draw.rect(screen, invisible, self.rect_up, 1)
        #pygame.draw.rect(screen, white, self.rect_right, 1)
        #pygame.draw.rect(screen, white, self.rect_left, 1)

    #docstring exemplo de função:
    """Fetches rows from a Smalltable.

    Retrieves rows pertaining to the given keys from the Table instance
    represented by table_handle.  String keys will be UTF-8 encoded.

    Args:
        table_handle: An open smalltable.Table instance.
        keys: A sequence of strings representing the key of each table
          row to fetch.  String keys will be UTF-8 encoded.
        require_all_keys: If True only rows with values set for all keys will be
          returned.

    Returns:
        A dict mapping keys to the corresponding table row data
        fetched. Each row is represented as a tuple of strings. For
        example:

        {b'Serak': ('Rigel VII', 'Preparer'),
         b'Zim': ('Irk', 'Invader'),
         b'Lrrr': ('Omicron Persei 8', 'Emperor')}

        Returned keys are always bytes.  If a key from the keys argument is
        missing from the dictionary, then that row was not found in the
        table (and require_all_keys must have been False).

    """