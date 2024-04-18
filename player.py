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
    def __init__(self, scale=4) -> None:
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
        self.jumping_speed = 160
        self.vertical_speed = 0
        self.gravity_ = 90
        self.pos_x = 400
        self.pos_y = 402
        self.width = 200
        self.height = 77
        self.rect_ground = pygame.Rect(self.pos_x+85, self.pos_y+70,  30, 10)   
        self.rect = pygame.Rect(self.pos_x, self.pos_y,  self.width, self.height)
        self.rect.topleft = [self.pos_x, self.pos_y]

    #TODO: fazer docstring
    def _import_sprites(self, number_of_sprites: int, arquive: str, sprites_vector= []) -> None:
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

    #TODO: fazer docstring
    def update_position(self, new_pos_x: int, new_pos_y: int) -> None:
        """ Muda a posição do Rect do player e a posição do rect_ground

        Args:
            new_pos_x:
            new_pos_y:
        """
        if self.walking or self.jumping or not self.grounded:
            if(new_pos_x < 0):
                self.direction = "left"
            if(new_pos_x > 0):
                self.direction = "right"
            self.pos_x += new_pos_x
            self.pos_y += new_pos_y
            self.rect.topleft = [self.pos_x, self.pos_y]
            self.rect_ground.topleft = [self.pos_x+85, self.pos_y+70]
    

    def apply_delta_gravity_effect(self, delta_t: float) -> None:
        """Modifica a posição vertical do jogador de acordo com as leis da gravidade no tempo delta_t.

        Args:
            delta_t: tempo que determina o delta posição 
        """
        time.sleep(0.01)
        delta_pos_y = self.vertical_speed*delta_t - self.gravity_*delta_t*delta_t/2 
        #delta(X) = Vot - g(t^2)/2
        self.vertical_speed -= self.gravity_*delta_t
        #V = Vo - gt

        self.update_position(0, -delta_pos_y)

    def get_jumping_speed(self):
        return self.jumping_speed

    def is_grounded(self, map: map) -> bool:
        """Retorna True se o player estiver tocando o chão
        
        Args:
            map: objeto que contém função capaz de checar se o player está colidindo com o chão ou não
        """
        return map.check_collision(self.rect_ground)

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

                elif self.falling:
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

                elif self.falling:
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
        red = (255, 0, 0)
        yellow = (255, 255, 0)
        pygame.draw.rect(screen, yellow, self.rect, 1)
        pygame.draw.rect(screen, (0, 255, 0), self.rect_ground, 1)

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