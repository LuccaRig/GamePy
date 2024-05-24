import pygame

class Enemy(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        # Atributos dos inimigos
        hp = 0
        attack = 0

        # Default Boolean and Character States
        self.is_animating = False
        self.walking = False
        self.direction = "left"

    def import_sprites(self, number_of_sprites=0, arquive='0', sprites_vector= [], scale=4) -> None:
        for i in range(number_of_sprites):
            sprite = pygame.image.load(f'{arquive}/tile00{i}.png')
            # Scale the sprite
            sprite = pygame.transform.scale(sprite, (int(sprite.get_width() * scale), int(sprite.get_height() * scale)))
            sprites_vector.append(sprite)

    def update_position(self, delta_x, delta_y):
        if delta_x != 0: self.walking = True
        else: self.walking = False

        
        self.rect.x += delta_x
        self.rect.y += delta_y
        self.rect_down.topleft = [self.rect.x +85, self.rect.y +70]

    def is_grounded(self, Map) -> None:
        return Map.check_collision(self.rect)

    def animate(self) -> None:
        self.is_animating = True 

    def update(self) -> None:
        animation_speed = 0.10
        if self.walking:
            animation_speed = 0.10
        if not self.walking:
            animation_speed = 0.20 

        if  self.is_animating:
            self.current_sprite += animation_speed


            if(self.direction == "right"):
                if self.walking:
                    if self.current_sprite >= len(self.sprites_moving_right):
                        self.current_sprite = 0
                        self.is_animating = False
                    self.image = self.sprites_moving_right[int(self.current_sprite)]
                else:
                    if self.current_sprite >= len(self.sprites_idle_right):
                        self.current_sprite = 0
                        self.is_animating = False
                    self.image = self.sprites_idle_right[int(self.current_sprite)]

            if(self.direction == "left"):
                if self.walking:
                    if self.current_sprite >= len(self.sprites_moving_left):
                        self.current_sprite = 0
                        self.is_animating = False
                    self.image = self.sprites_moving_left[int(self.current_sprite)]
                else:
                    if self.current_sprite >= len(self.sprites_idle_right):
                        self.current_sprite = 0
                        self.is_animating = False
                    self.image = self.sprites_idle_right[int(self.current_sprite)]
            


class Shooter(Enemy):
    def __init__(self, inital_pos : list) -> None:
        super().__init__()
        #Sprites and animation
        #TODO: Change walking to waking
        
        self.sprites_idle_right = []
        self.sprites_idle_left = []

        self.sprites_moving_right = []
        self.sprites_moving_left = []

        self.import_sprites(1,'CharacterSprites/shooter/idlePNGright', self.sprites_idle_right)
        self.import_sprites(1,'CharacterSprites/shooter/idlePNGleft', self.sprites_idle_left)
        self.import_sprites(5,'CharacterSprites/shooter/wakePNGright', self.sprites_moving_right)
        self.import_sprites(5,'CharacterSprites/shooter/wakePNGleft', self.sprites_moving_left)

        self.current_sprite = 0
        self.image = self.sprites_idle_right[self.current_sprite]


        # Default Position and movement
        self.pos_x = inital_pos[0]
        self.pos_y = inital_pos[1]
        self.width = 55
        self.height = 65
        self.rect = pygame.Rect(self.pos_x, self.pos_y,  self.width, self.height)
        self.rect.topleft = [self.pos_x, self.pos_y]
        self.rect_down = pygame.Rect(self.pos_x+85, self.pos_y+10,  30, 10)
        self.speed = 1
        self.actual_pos = 0

    def move_set(self):
        """ 
        Garante uma movimentacao fixa do objeto Little_Spider
        """

        self.update_position(0, 0)

    
class Little_Spider(Enemy):
    def __init__(self, inital_pos : list) -> None:
        super().__init__()
        #Sprites and animation
        
        self.sprites_idle_right = []
        self.sprites_idle_left = []

        self.sprites_moving_right = []
        self.sprites_moving_left = []

        self.import_sprites(1,'CharacterSprites/little_spider/idlePNGright', self.sprites_idle_right)
        self.import_sprites(1,'CharacterSprites/little_spider/idlePNGleft', self.sprites_idle_left)
        self.import_sprites(6,'CharacterSprites/little_spider/movementPNGright', self.sprites_moving_right)
        self.import_sprites(6,'CharacterSprites/little_spider/movementPNGleft', self.sprites_moving_left)

        self.current_sprite = 0
        self.image = self.sprites_idle_right[self.current_sprite]

        # Default Position and movement
        self.pos_x = inital_pos[0]
        self.pos_y = inital_pos[1]
        self.width = 96
        self.height = 65
        self.rect = pygame.Rect(self.pos_x, self.pos_y,  self.width, self.height)
        self.rect.topleft = [self.pos_x, self.pos_y]
        self.rect_down = pygame.Rect(self.pos_x+85, self.pos_y+10,  30, 10)
        self.speed = 1
        self.actual_pos = 0

    def move_set(self):
        """ 
        Garante uma movimentacao fixa do objeto Little_Spider
        """
        right_limit = 30
        left_limit = -30
        self.actual_pos = self.actual_pos + self.speed
        if self.actual_pos >= right_limit:
            self.speed = -1
            self.direction = "left"
        elif self.actual_pos <= left_limit:
            self.speed = 1
            self.direction = "right"

        self.update_position(self.speed, 0)


class Enemy_Group(Enemy):
    """
    Essa classe agrupa os inimigos criados em um vetor, e seus metodos chamam metodos de cada entidade 
    dentro desse vetor, um exemplo eh atualizar a animacao de todos os inimigos ao mesmo tempo

    """
    def __init__(self, enemy_group_number : int) -> None:
        super().__init__()
        self.enemy_vector = []
        self.enemy_group_number = enemy_group_number

        if enemy_group_number == 0:
            little_spider = Little_Spider([400, 500])
            enemy2 = Shooter([250, 360])
            self.enemy_vector = [little_spider, enemy2]

    def update_enemies_sprites(self):
        for enemy in self.enemy_vector:
            enemy.animate()
            enemy.update()

    def draw_enemies(self, screen, off_set_x, off_set_y):
        """
        Desenha os inimigos na tela e muda a posicao com o valor dos off_sets

        Args:
            off_set_x : Modifica a posicao do desenho do inimigo no eixo x (Obs: esse valor preferencialmente deve ser
            o off_set_x do mapa, para que o desenho do inimigo sempre esteja alinhado com as imagens do mapa)
            off_set_y : idem para a posicao y, segue a mesma observacao 
        """

        for enemy in self.enemy_vector:
            screen.blit(enemy.image, (enemy.rect.x + off_set_x, enemy.rect.y - off_set_y))

    def draw_collisions_rects(self, screen):
        green = (0, 255, 0)
        for enemy in self.enemy_vector:
            pygame.draw.rect(screen, green, enemy.rect_down, 1)
    
    def define_pos_group(self, delta_x, delta_y):
        """
        Atualiza a posicao do conjunto de inimigos 

        Args:
            delta_x: O quanto o valor de posicao em x vai se modificar
            delta_y: idem para a posicao em y
        """
        for enemy in self.enemy_vector:
            new_pos_x = enemy.rect.x + delta_x
            new_pos_y = enemy.rect.y - delta_y
            enemy.rect_down.topleft = [new_pos_x + 35, new_pos_y + 55]
    
    def set_move_sets(self):
        for enemy in self.enemy_vector:
            enemy.move_set()