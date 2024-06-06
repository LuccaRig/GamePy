import pygame
import map
import time

#TODO: fazer docstring da classe
class Player(pygame.sprite.Sprite):
    """A one-line summary of the module or program, terminated by a period.

Leave one blank line.  The rest of this docstring should contain an
overall description of the module or program.  Optionally, it may also
contain a brief description of exported classes and functions and/or usage
examples.

Typical usage example:

  foo = ClassFoo()
  bar = foo.FunctionBar()
    """
    def __init__(self) -> None:
        super().__init__()
        # Sprites Vectors
        self.sprites_idle_right = []
        self.sprites_idle_left = []

        self.sprites_moving_right = []
        self.sprites_moving_left = []

        self.sprites_attacking_right = []
        self.sprites_attacking_left = []

        self.sprites_jumping_right = []
        self.sprites_jumping_left = []

        self.sprites_falling_right = []
        self.sprites_falling_left = []

        self.sprites_landing_right = []
        self.sprites_landing_left = []

        # Load All Sprites
        self._import_sprites(9,'CharacterSprites/assassin/idlePNGright', self.sprites_idle_right)
        self._import_sprites(9,'CharacterSprites/assassin/idlePNGleft', self.sprites_idle_left)    
        self._import_sprites(8,'CharacterSprites/assassin/movementPNGright', self.sprites_moving_right)
        self._import_sprites(8,'CharacterSprites/assassin/movementPNGleft', self.sprites_moving_left)
        self._import_sprites(9,'CharacterSprites/assassin/attackPNGright', self.sprites_attacking_right)
        self._import_sprites(9,'CharacterSprites/assassin/attackPNGleft', self.sprites_attacking_left)
        self._import_sprites(4, 'CharacterSprites/assassin/jumpPNGright', self.sprites_jumping_right)
        self._import_sprites(4, 'CharacterSprites/assassin/jumpPNGleft', self.sprites_jumping_left)
        self._import_sprites(4, 'CharacterSprites/assassin/fallPNGright', self.sprites_falling_right)
        self._import_sprites(4, 'CharacterSprites/assassin/fallPNGleft', self.sprites_falling_left)
        self._import_sprites(4, 'CharacterSprites/assassin/landPNGright', self.sprites_landing_right)
        self._import_sprites(4, 'CharacterSprites/assassin/landPNGleft', self.sprites_landing_left)

        # Default Boolean and Character States
        self.is_animating = False
        self.attacking = False
        self.walking = False
        self.grounded = False
        self.jumping = False
        self.landing = False
        self.falling = False
        self.direction = "right"
        self.current_sprite = 0
        self.current_sprite_attack = 0
        self.current_sprite_jump = 0
        self.current_sprite_land = 0
        self.image = self.sprites_idle_right[self.current_sprite]     

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
        self.delta_pos_y = 0
        self.x_limit_reached = False
        self.y_limit_reached = False

        # Stats
        self.attack_dmg = 10
        self.hp = 50
        self.hp_bar_background = pygame.Rect(10, 10, 200, 40)
        self.hp_bar = pygame.Rect(10, 10, 200, 40)

        self.last_hit_time = 0
        self.last_landed_attack_time = 0

    def _import_sprites(self, number_of_sprites: int, arquive: str, sprites_vector) -> None:
        """ Acessa a pasta selecionada {arquive} e guarda os PNG em um vetores de PNG {sprites_vector}

        Args:
            number_of_sprites:
            arquive:
            sprites_vector:
        """
        scale = 4
        for i in range(number_of_sprites):
            sprite = pygame.image.load(f'{arquive}/tile00{i}.png')
            # Scale the sprite
            sprite = pygame.transform.scale(sprite, (int(sprite.get_width() * scale), int(sprite.get_height() * scale)))
            sprites_vector.append(sprite)
        
    def hp_bar_change(self) -> None:
        hp_bar_percent = self.hp*4
        self.hp_bar = pygame.Rect(10, 10, hp_bar_percent, 40)

    def reinitialize_position_advancing(self, map: map) -> None:
        """Ajusta a posição do player para a nova sala

        Args:
            map: objeto que contém os blocos de colisão para ajuste do player
        """
        self.pos_x = map.pos_x_previous_room - 40
        self.pos_y = map.pos_y_previous_room + 110

    def reinitialize_position_returning(self, map: map, off_set_x: int) -> None:
        """Ajusta a posição do player para a sala anterior

        Args:
            map: objeto que contém os blocos de colisão para ajuste do player
        """
        self.pos_x = map.pos_x_new_room - 125 + off_set_x
        self.pos_y = map.pos_y_new_room + 110

    def update_position(self, new_pos_x: int, new_pos_y: int) -> None:
        """ Muda a posição do Rect do player e a posição dos seu rects direcionais

        Args:
            new_pos_x:
            new_pos_y:
        """
        self.speed[0] = new_pos_x
        self.speed[1] = new_pos_y
        if self.walking or self.jumping or not self.grounded :
            #print(self.x_limit_reached)
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
        time.sleep(0.01)
        self.delta_pos_y = self.vertical_speed*delta_t - self.gravity_*delta_t*delta_t/2 
        #delta(X) = Vot - g(t^2)/2
        self.vertical_speed -= self.gravity_*delta_t
         #V = Vo - gt
        if self.is_colliding(map, "up"):
            self.vertical_speed = 0
            self.update_position(0, 5)
        else:
            self.update_position(0, -self.delta_pos_y)

    def correct_ground_intersection(self, map: map):
        """Coloca o player precisamente acima do chão após uma queda

        Args:
            map: objeto capaz de retornar a interseção entre o rect inferior do player e o rect do chão
        """
        intersection_rect = map.return_ground_intersection(self.rect_down)
        if intersection_rect.height > 1:
            #print("corrigindo pulo: ", intersection_rect.height)
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
        if(self.direction == "right"):
            return map.check_new_room(self.rect_right)
        elif(self.direction == "left"):
            return map.check_new_room(self.rect_left)
    
    def is_returning_room(self, map: map) -> bool:
        """Retorna True se o player estiver voltando para a sala anterior
        
        Args:
            map: objeto que contém função capaz de checar colisões
        """
        if(self.direction == "left"):
            return map.check_previous_room(self.rect_left)
        elif(self.direction == "right"):
            return map.check_previous_room(self.rect_right)

    #TODO: fazer docstring
    def animate_attack(self) -> None:
        """
        """
        animation_speed = 0.15
        self.current_sprite_attack += animation_speed
        if self.direction == "right":
            if self.current_sprite_attack >= len(self.sprites_attacking_right):
                self.current_sprite_attack = 0
                self.is_animating = False
                self.attacking = False
            else:
                self.image = self.sprites_attacking_right[int(self.current_sprite_attack)]

        elif self.direction == "left":
            if self.current_sprite_attack >= len(self.sprites_attacking_left):
                self.current_sprite_attack = 0
                self.is_animating = False
                self.attacking = False
            else:
                self.image = self.sprites_attacking_left[int(self.current_sprite_attack)]

    #TODO: fazer docstring
    def animate_land(self) -> None:
        """
        """
        if self.landing:    
            animation_speed = 0.3
            self.current_sprite_land += animation_speed
            if self.direction == "right":
                if self.current_sprite_land >= len(self.sprites_landing_right):
                    self.current_sprite_land = 0
                    self.is_animating = False
                    self.landing = False
                else:
                    self.image = self.sprites_landing_right[int(self.current_sprite_land)]

            elif self.direction == "left":
                if self.current_sprite_land >= len(self.sprites_landing_left):
                    self.current_sprite_land = 0
                    self.is_animating = False
                    self.landing = False
                else:
                    self.image = self.sprites_landing_left[int(self.current_sprite_land)]

    #sugestão: tratar is_animating como atributo público e apagar essa função 
    def animate(self) -> None:
        self.is_animating = True
    
    #TODO: fazer a docstring
    def update(self) -> None:
        """
        """
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
                    if self.current_sprite >= len(self.sprites_falling_right):
                        self.current_sprite = 0
                        self.is_animating = False
                    self.image = self.sprites_falling_right[int(self.current_sprite)]
                
                elif self.jumping:
                    if self.current_sprite >= len(self.sprites_jumping_right):
                        self.current_sprite = 0
                        self.is_animating = False
                    self.image = self.sprites_jumping_right[int(self.current_sprite)]

                elif self.walking and not self.landing:
                    if self.current_sprite >= len(self.sprites_moving_right):
                        self.current_sprite = 0
                        self.is_animating = False
                    self.image = self.sprites_moving_right[int(self.current_sprite)]

                elif not self.walking and not self.landing:
                    if self.current_sprite >= len(self.sprites_idle_right):
                        self.current_sprite = 0
                        self.is_animating = False
                    self.image = self.sprites_idle_right[int(self.current_sprite)]


            if(self.direction == "left"):
                if self.attacking:
                    self.animate_attack()

                elif self.falling and not self.attacking:
                    if self.current_sprite >= len(self.sprites_falling_left):
                        self.current_sprite = 0
                        self.is_animating = False
                    self.image = self.sprites_falling_left[int(self.current_sprite)]

                elif self.jumping:
                    if self.current_sprite >= len(self.sprites_jumping_left):
                        self.current_sprite = 0
                        self.is_animating = False
                    self.image = self.sprites_jumping_left[int(self.current_sprite)]

                elif self.walking and not self.landing:
                    if self.current_sprite >= len(self.sprites_moving_left):
                        self.current_sprite = 0
                        self.is_animating = False
                    self.image = self.sprites_moving_left[int(self.current_sprite)]

                elif not self.walking and not self.landing:
                    if self.current_sprite >= len(self.sprites_idle_left):
                        self.current_sprite = 0
                        self.is_animating = False
                    self.image = self.sprites_idle_left[int(self.current_sprite)]
                

    #TODO: fazer a docstring
    def draw_collision_rect(self, screen: pygame.display) -> None:
        # Desenha um retângulo vermelho em torno do retângulo do jogador
        green = (0, 255, 0)
        red = (255, 0, 0)
        white = (255, 255, 255)
        black = (0,0,0)
        #pygame.draw.rect(screen, yellow, self.rect, 1)
        pygame.draw.rect(screen, black, self.rect_down, 1)
        pygame.draw.rect(screen, white, self.hitbox_rect, 1)
        pygame.draw.rect(screen, red, self.right_attack_rect, 1)
        pygame.draw.rect(screen, red, self.left_attack_rect, 1)

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