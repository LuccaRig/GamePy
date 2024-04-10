import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, scale=4) -> None:
        super().__init__()
        # Sprites Import and Set Scale
        self.sprites_idle_right = []
        self.sprites_idle_left = []

        self.sprites_moving_right = []
        self.sprites_moving_left = []

        self.sprites_attacking_right = []
        self.sprites_attacking_left = []

        self.is_animating = False

        self.attacking = False
        self.walking = False
        self.direction = "right"


        # Load All Sprites

        number_of_sprites_idle_right = 9
        for i in range(number_of_sprites_idle_right):
            sprite = pygame.image.load(f'CharacterSprites/assassin/idlePNG/tile00{i}.png')
            # Scale the sprite
            sprite = pygame.transform.scale(sprite, (int(sprite.get_width() * scale), int(sprite.get_height() * scale)))
            self.sprites_idle_right.append(sprite)

        number_of_sprites_idle_left = 9
        for i in range(number_of_sprites_idle_left):
            sprite = pygame.image.load(f'CharacterSprites/assassin/idlePNGleft/tile00{i}.png')
            # Scale the sprite
            sprite = pygame.transform.scale(sprite, (int(sprite.get_width() * scale), int(sprite.get_height() * scale)))
            self.sprites_idle_left.append(sprite)

        number_of_sprites_movement_left = 8
        for i in range(number_of_sprites_movement_left):
            sprite = pygame.image.load(f'CharacterSprites/assassin/movementPNGleft/tile00{i}.png')
            # Scale the sprite
            sprite = pygame.transform.scale(sprite, (int(sprite.get_width() * scale), int(sprite.get_height() * scale)))
            self.sprites_moving_left.append(sprite)

        number_of_sprites_movement_right = 8
        for i in range(number_of_sprites_movement_right):
            sprite = pygame.image.load(f'CharacterSprites/assassin/movementPNG/tile00{i}.png')
            # Scale the sprite
            sprite = pygame.transform.scale(sprite, (int(sprite.get_width() * scale), int(sprite.get_height() * scale)))
            self.sprites_moving_right.append(sprite)
        
        number_of_sprites_attack_right = 9
        for i in range(number_of_sprites_attack_right):
            sprite = pygame.image.load(f'CharacterSprites/assassin/attackPNG/tile00{i}.png')
            # Scale the sprite
            sprite = pygame.transform.scale(sprite, (int(sprite.get_width() * scale), int(sprite.get_height() * scale)))
            self.sprites_attacking_right.append(sprite)

        number_of_sprites_attack_left = 9
        for i in range(number_of_sprites_attack_left):
            sprite = pygame.image.load(f'CharacterSprites/assassin/attackPNGleft/tile00{i}.png')
            # Scale the sprite
            sprite = pygame.transform.scale(sprite, (int(sprite.get_width() * scale), int(sprite.get_height() * scale)))
            self.sprites_attacking_left.append(sprite)



        self.current_sprite = 0
        self.image = self.sprites_idle_right[self.current_sprite]


        # Position and movement
        self.pos_x = 400
        self.pos_y = 400
        self.width = 110
        self.height = 80   
        self.rect = pygame.Rect(self.pos_x, self.pos_y,  self.width, self.height)
        self.rect.topleft = [self.pos_x, self.pos_y]

    def update_position(self, new_pos_x, new_pos_y):
        if self.walking == True:
            if(new_pos_x < 0):
                self.direction = "left"
            if(new_pos_x > 0):
                self.direction = "right"
            self.pos_x += new_pos_x
            self.pos_y += new_pos_y
            self.rect.topleft = [self.pos_x, self.pos_y]


    def animate(self):
        self.is_animating = True
    
    def update(self):
        animation_speed = 0
        if self.walking == True:
            animation_speed = 0.15
        if self.walking == False:
            animation_speed = 0.25 
        if self.attacking == True:
            animation_speed = 0.25

        if  self.is_animating == True:
            self.current_sprite += animation_speed


            if(self.direction == "right"):
                if self.attacking == True:
                    if self.current_sprite >= len(self.sprites_attacking_right):
                        self.current_sprite = 0
                        self.is_animating = False
                    self.image = self.sprites_attacking_right[int(self.current_sprite)]

                elif self.walking == False:
                    if self.current_sprite >= len(self.sprites_idle_right):
                        self.current_sprite = 0
                        self.is_animating = False
                    self.image = self.sprites_idle_right[int(self.current_sprite)]
                elif self.walking == True:
                    if self.current_sprite >= len(self.sprites_moving_right):
                        self.current_sprite = 0
                        self.is_animating = False
                    self.image = self.sprites_moving_right[int(self.current_sprite)]

            if(self.direction == "left"):
                if self.attacking == True:
                    if self.current_sprite >= len(self.sprites_attacking_left):
                        self.current_sprite = 0
                        self.is_animating = False
                    self.image = self.sprites_attacking_left[int(self.current_sprite)]
                elif self.walking == False:
                    if self.current_sprite >= len(self.sprites_idle_left):
                        self.current_sprite = 0
                        self.is_animating = False
                    self.image = self.sprites_idle_left[int(self.current_sprite)]
                elif self.walking == True:
                    if self.current_sprite >= len(self.sprites_moving_left):
                        self.current_sprite = 0
                        self.is_animating = False
                    self.image = self.sprites_moving_left[int(self.current_sprite)]


    def draw_collision_rect(self, screen):
        # Desenha um retângulo vermelho em torno do retângulo do jogador
        pygame.draw.rect(screen, (255, 0, 0), self.rect, 1)