import pygame

class Enemy(pygame.sprite.Sprite):
    def __init__(self, scale=4) -> None:
        super().__init__()
        # Atributos dos inimigos
        hp = 0
        attack = 0

        # Sprites Vectors
        self.sprites_idle_right = []
        self.sprites_idle_left = []

        self.sprites_moving_right = []
        self.sprites_moving_left = []

        # Load All Sprites
        self.import_sprites(1,'CharacterSprites/enemy1/idlePNGright', self.sprites_idle_right)
        self.import_sprites(1,'CharacterSprites/enemy1/idlePNGleft', self.sprites_idle_left)
        self.import_sprites(6,'CharacterSprites/enemy1/movementPNGright', self.sprites_moving_right)
        self.import_sprites(6,'CharacterSprites/enemy1/movementPNGleft', self.sprites_moving_left)

        # Default Boolean and Character States
        self.is_animating = False
        self.walking = False
        self.direction = "left" 
        self.current_sprite = 0
        self.image = self.sprites_idle_right[self.current_sprite] 

    def import_sprites(self, number_of_sprites=0, arquive='0', sprites_vector= [], scale=4) -> None:
        for i in range(number_of_sprites):
            sprite = pygame.image.load(f'{arquive}/tile00{i}.png')
            # Scale the sprite
            sprite = pygame.transform.scale(sprite, (int(sprite.get_width() * scale), int(sprite.get_height() * scale)))
            sprites_vector.append(sprite)

    def update_position(self, new_pos_x, new_pos_y) -> None:
        if self.walking:
            if(new_pos_x < 0):
                self.direction = "left"
            if(new_pos_x > 0):
                self.direction = "right"
            self.pos_x += new_pos_x
            self.pos_y += new_pos_y
            self.rect.topleft = [self.pos_x, self.pos_y]

    def is_grounded(self, Map) -> None:
        return Map.check_collision(self.rect)

    def animate(self) -> None:
        self.is_animating = True 

    def update(self) -> None:
        animation_speed = 0
        if self.walking:
            animation_speed = 0.10
        if not self.walking:
            animation_speed = 0.20 

        if  self.is_animating:
            self.current_sprite += animation_speed


            if(self.direction == "right"):
                if not self.walking:
                    if self.current_sprite >= len(self.sprites_idle_right):
                        self.current_sprite = 0
                        self.is_animating = False
                    self.image = self.sprites_idle_right[int(self.current_sprite)]
                elif self.walking:
                    if self.current_sprite >= len(self.sprites_moving_right):
                        self.current_sprite = 0
                        self.is_animating = False
                    self.image = self.sprites_moving_right[int(self.current_sprite)]

            if(self.direction == "left"):
                if not self.walking:
                    if self.current_sprite >= len(self.sprites_idle_left):
                        self.current_sprite = 0
                        self.is_animating = False
                    self.image = self.sprites_idle_left[int(self.current_sprite)]
                elif self.walking:
                    if self.current_sprite >= len(self.sprites_moving_left):
                        self.current_sprite = 0
                        self.is_animating = False
                    self.image = self.sprites_moving_left[int(self.current_sprite)]  

class Mobs(Enemy):
    def __init__(self, scale=4) -> None:
        super().__init__(scale) 
        # Default Position and movement
        self.speed = [0, 0]
        self.pos_x = 700
        self.pos_y = 410
        self.width = 96
        self.height = 65
        self.rect = pygame.Rect(self.pos_x, self.pos_y,  self.width, self.height)
        self.rect.topleft = [self.pos_x, self.pos_y]

    def draw_collision_rect(self, screen) -> None:
        # Desenha um retângulo vermelho em torno do retângulo do jogador
        pygame.draw.rect(screen, (255, 0, 0), self.rect, 1)