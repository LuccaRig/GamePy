import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, scale=4) -> None:
        super().__init__()
        # Sprites Import and Set Scale
        self.sprites_idle = []
        self.is_animating = False
        number_of_sprites_idle = 9
        
        for i in range(number_of_sprites_idle):
            sprite = pygame.image.load(f'CharacterSprites/assassin/idlePNG/tile00{i}.png')
            # Scale the sprite
            sprite = pygame.transform.scale(sprite, (int(sprite.get_width() * scale), int(sprite.get_height() * scale)))
            self.sprites_idle.append(sprite)
        self.current_sprite = 0
        self.image = self.sprites_idle[self.current_sprite]


        # Position and movement
        self.pos_x = 100
        self.pos_y = 100
        self.rect = self.image.get_rect()
        self.rect.topleft = [self.pos_x, self.pos_y]

    def update_position(self, pos_x, pos_y):
        self.pos_x += pos_x
        self.pos_y += pos_y
        self.rect.topleft = [self.pos_x, self.pos_y]


    def animate(self):
        self.is_animating = True
    
    def update(self, speed=0.25):
        if  self.is_animating == True:
            self.current_sprite += speed

            if self.current_sprite >= len(self.sprites_idle):
                self.current_sprite = 0
                self.is_animating = False

            self.image = self.sprites_idle[int(self.current_sprite)]
