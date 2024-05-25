import pygame

class Npc():
    def __init__(self) -> None:
        self.is_animating = False
        self.current_sprite = 0

        self.sprites = []
                
        
    def import_sprites(self, number_of_sprites : int, arquive : str, sprites_vector : list, scale=4) -> None:
        for i in range(number_of_sprites):
            sprite = pygame.image.load(f'{arquive}/tile00{i}.png')
            # Scale the sprite
            sprite = pygame.transform.scale(sprite, (int(sprite.get_width() * scale), int(sprite.get_height() * scale)))
            sprites_vector.append(sprite)

    def animate(self) -> None:
        self.is_animating = True 

    def update(self) -> None:
        animation_speed = 0.10

        if  self.is_animating:
            self.current_sprite += animation_speed
        
        if self.current_sprite >= len(self.sprites):
            self.current_sprite = 0
            self.is_animating = False
        self.image = self.sprites[int(self.current_sprite)]

    def draw_npc(self, screen, off_set_x, off_set_y):
        screen.blit(self.image, (self.rect.x + off_set_x, self.rect.y - off_set_y))

class Traveler(Npc):
    def __init__(self) -> None:
        super().__init__()

        self.import_sprites(10, "CharacterSprites/TravelerNPC", self.sprites)
        self.pos = [750, 300]
        self.width = 90 
        self.height  = 65
        self.rect = pygame.Rect(self.pos[0], self.pos[1],  self.width, self.height)
        self.rect.topleft = [self.pos[0], self.pos[1]]
        self.image = self.sprites[int(self.current_sprite)]
        

    