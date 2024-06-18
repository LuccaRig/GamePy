import pygame
import player

class Npc():
    def __init__(self) -> None:
        self.is_animating = False
        self.current_sprite = 0
        self.sprites = []  
        
    def import_sprites(self, number_of_sprites : int, arquive : str, sprites_vector : list) -> None:
        """Acessa a pasta selecionada {arquive} e guarda os PNG em um vetores de PNG {sprites_vector}.

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

    def animate(self) -> None:
        self.is_animating = True 

    def update(self) -> None:
        """Atualiza a animação de idle 
        """
        animation_speed = 0.10

        if  self.is_animating:
            self.current_sprite += animation_speed
        
        if self.current_sprite >= len(self.sprites):
            self.current_sprite = 0
            self.is_animating = False
        self.image = self.sprites[int(self.current_sprite)]

    def draw_npc(self, screen, off_set_x, off_set_y) -> None:
        """Desenha o npc na nela e corrige sua posição de acordo com a movimentação da câmera
        """
        screen.blit(self.image, (self.rect.x + off_set_x, self.rect.y - off_set_y))

    def check_player_interaction(self, player) -> None:
        """Testa se o npc está tocando no player
        """
        return self.interact_rect.colliderect(player.hitbox_rect)


class Traveler(Npc):
    def __init__(self, pos : list, talk_number : int) -> None:
        super().__init__()

        self.import_sprites(10, "CharacterSprites/TravelerNPC", self.sprites)
        self.y_correction = 55
        self.pos = pos
        self.width = 90 
        self.height  = 65
        self.rect = pygame.Rect(self.pos[0], self.pos[1],  self.width, self.height)
        self.rect.topleft = [self.pos[0], self.pos[1]]
        self.image = self.sprites[int(self.current_sprite)]
        self.text_pos = [pos[0] - 50, pos[1]]
        
        self.interact_rect = pygame.Rect(self.pos[0], self.pos[1]+ self.y_correction,  self.width, self.height)
        self.text_color = (255, 255, 255)
        self.font_size = 36
        self.dialogue_font = pygame.font.Font(None, self.font_size)
        self.text_index = 0
        self.last_letter_time = 0
        self.talk_number = talk_number  

    def draw_interact_rect(self, screen, off_set_x, off_set_y) -> None:
        self.interact_rect = pygame.Rect(self.pos[0] + off_set_x, self.pos[1] - off_set_y + self.y_correction,  self.width, self.height)
        #pygame.draw.rect(screen, (0,255,0), self.interact_rect, 1)
        self.text_pos = (self.pos[0] + off_set_x, self.pos[1] - off_set_y)
        
    def talk_to_player(self, player: player, screen: pygame.display) -> None:
        """Desenha um texto de diálogo para o player
        """
        current_time = pygame.time.get_ticks()
        letter_interval = 100

        if self.talk_number == 0:
            text = "Olá, Jogador!"

        if self.talk_number == 1:
            text = "Boa tarde senhor chupapica"

        if(self.check_player_interaction(player)):

            if self.text_index < len(text) and current_time - self.last_letter_time > letter_interval:
                self.text_index += 1
                self.last_letter_time = current_time
            
            text_render = self.dialogue_font.render(text[:self.text_index], True, self.text_color)
            screen.blit(text_render, self.text_pos)
        else: 
            pass
        


    