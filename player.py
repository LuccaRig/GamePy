import pygame
import map

class Player(pygame.sprite.Sprite):
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
        self.import_sprites(9,'CharacterSprites/assassin/idlePNGright', self.sprites_idle_right)
        self.import_sprites(9,'CharacterSprites/assassin/idlePNGleft', self.sprites_idle_left)    
        self.import_sprites(8,'CharacterSprites/assassin/movementPNGright', self.sprites_moving_right)
        self.import_sprites(8,'CharacterSprites/assassin/movementPNGleft', self.sprites_moving_left)
        self.import_sprites(9,'CharacterSprites/assassin/attackPNGright', self.sprites_attacking_right)
        self.import_sprites(9,'CharacterSprites/assassin/attackPNGleft', self.sprites_attacking_left)
        self.import_sprites(4,'CharacterSprites/assassin/jumpPNGright', self.sprites_jumping_right)
        self.import_sprites(4,'CharacterSprites/assassin/jumpPNGleft', self.sprites_jumping_left)
        self.import_sprites(4,'CharacterSprites/assassin/fallPNGright', self.sprites_falling_right)
        self.import_sprites(4,'CharacterSprites/assassin/fallPNGleft', self.sprites_falling_left)
        self.import_sprites(4,'CharacterSprites/assassin/landPNGright', self.sprites_landing_right)
        self.import_sprites(4,'CharacterSprites/assassin/fallPNGleft', self.sprites_falling_left)

        # Default Boolean and Character States
        self.is_animating = False
        self.attacking = False
        self.walking = False
        self.grounded = False
        self.jumping = False
        self.direction = "right"
        self.current_sprite = 0
        self.current_sprite_attack = 0
        self.current_sprite_jump = 0
        self.image = self.sprites_idle_right[self.current_sprite]     

        # Default Position and movement
        self.speed = [0, 0]
        self.pos_x = 400
        self.pos_y = 400
        self.width = 200
        self.height = 77
        self.rect_ground = pygame.Rect(self.pos_x+85, self.pos_y+70,  30, 10)   
        self.rect = pygame.Rect(self.pos_x, self.pos_y,  self.width, self.height)
        self.rect.topleft = [self.pos_x, self.pos_y]

    def import_sprites(self, number_of_sprites=0, arquive='0', sprites_vector= [], scale=4):
        for i in range(number_of_sprites):
            sprite = pygame.image.load(f'{arquive}/tile00{i}.png')
            # Scale the sprite
            sprite = pygame.transform.scale(sprite, (int(sprite.get_width() * scale), int(sprite.get_height() * scale)))
            sprites_vector.append(sprite)

    def update_position(self, new_pos_x, new_pos_y):
        if self.walking == True or self.jumping == True:
            if(new_pos_x < 0):
                self.direction = "left"
            if(new_pos_x > 0):
                self.direction = "right"
            self.pos_x += new_pos_x
            self.pos_y += new_pos_y
            self.rect.topleft = [self.pos_x, self.pos_y]
            self.rect_ground.topleft = [self.pos_x+85, self.pos_y+70]

    def isGrounded(self, Map):
        return Map.check_collision(self.rect_ground)

    
    def animate_attack(self):
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

    def animate_jump(self):
        animation_speed = 0.10
        self.current_sprite_jump += animation_speed
        if self.direction == "right":
            if self.current_sprite_jump >= len(self.sprites_jumping_right):
                self.current_sprite_jump = 0
                self.is_animating = False
                self.jumping = False
            else:
                self.image = self.sprites_jumping_right[int(self.current_sprite_jump)]

        elif self.direction == "left":
            if self.current_sprite_jump >= len(self.sprites_jumping_left):
                self.current_sprite_jump = 0
                self.is_animating = False
                self.jumping = False
            else:
                self.image = self.sprites_jumping_left[int(self.current_sprite_jump)]


    def animate(self):
        self.is_animating = True
    
    def update(self):
        animation_speed = 0
        if self.walking == True:
            animation_speed = 0.10
        if self.walking == False:
            animation_speed = 0.20 

        if  self.is_animating == True:
            self.current_sprite += animation_speed


            if(self.direction == "right"):
                if self.attacking == True:
                    self.animate_attack()

                elif self.jumping == True:
                    self.animate_jump()

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
                    self.animate_attack()

                elif self.jumping == True:
                    self.animate_jump()

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
        pygame.draw.rect(screen, (0, 255, 0), self.rect_ground, 1)