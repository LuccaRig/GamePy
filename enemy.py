import pygame
import numpy
from abc import abstractmethod, ABC

class Enemy(pygame.sprite.Sprite, ABC):
    def __init__(self) -> None:
        super().__init__()
        # Atributos dos inimigos
        self.hp = 0
        self.damage = 0
        self.coins_value = 0

        self._sprites_idle_right = []
        self._sprites_idle_left = []
        self._sprites_moving_right = []
        self._sprites_moving_left = []
        self._sprites_hit_right = []
        self._sprites_hit_left = []
        self._sprites_dying_right = []
        self._sprites_dying_left = []
        self._sprites_attack_right = []
        self._sprites_attack_left = []

        # Default Boolean and Character States
        self.is_animating = False
        self.is_attacking = False
        self.walking = False
        self.direction = "right"
        self.is_alive = True
        self.dying = False
        self.was_hit = False
        self.has_attack_rect = False

        self.current_sprite = 0
        self.current_death_sprite = 0
        self.current_hit_sprite = 0
        self.death_animation_speed = 0.12
        self.idle_animation_speed = 0.15
        self.walking_animation_speed = 0.10
        self.hit_animation_speed = 0.15

    def _import_sprites(self, number_of_sprites: int, arquive: str, sprites_vector : list) -> None:
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

    def update_position(self, delta_x: int, delta_y: int) -> None:
        """Modifica a posição do player 

        Args:
            delta_x: o tanto que será somado à direção x do player
            delta_y: o tanto que será somado à direção y do player
        """
        if not self.dying:
            if delta_x != 0: self.walking = True
            else: self.walking = False
            self.rect.x += delta_x
            self.rect.y += delta_y
            self.hitbox_rect.topleft = [self.rect.x +85, self.rect.y +70]

    def is_grounded(self, Map) -> bool:
        """Retorna verdadeiro se o rect de pé do player estiver tocando no chão
        """
        return Map.check_collision(self.rect)
    
    @abstractmethod
    def is_atk(self) -> bool:
        """Determina em que período de tempo uma interseção de rect de ataque do inimigo com o do player gerará
        uma perda de hp para o player. Se o inimigo não tiver rect de ataque, a função só devolve False
        """
        pass
    
    @abstractmethod
    def move_rects_toplefts(self, new_pos_x: int, new_pos_y: int) -> None:
        """Posiciona o topo dos rects de acordo com o comportamento e proporções do inimigo
        """

    def animate(self) -> None:
        self.is_animating = True 

    def animate_hit(self) -> None:
        """Coloca a animação de hit do inimigo em display
        """
        self.current_hit_sprite += self.hit_animation_speed
        if self.direction == "left":
             if self.current_hit_sprite >= len(self._sprites_hit_left):
                 self.current_hit_sprite = 0
                 self.was_hit = False
             else:
                 self.image = self._sprites_hit_left[int(self.current_hit_sprite)]

        elif self.direction == "right":
            if self.current_hit_sprite >= len(self._sprites_hit_right):
                 self.current_hit_sprite = 0
                 self.was_hit = False
            else:
                 self.image = self._sprites_hit_right[int(self.current_hit_sprite)]


    def animate_death(self) -> None:
        """Coloca a animação de morte do inimigo em display

        No final da animação, o inimigo é considerado morto (is_alive = False)
        """
        self.current_death_sprite += self.death_animation_speed
        if self.direction == "left":
             if self.current_death_sprite >= len(self._sprites_dying_left):
                 self.current_death_sprite = 0
                 self.is_animating = False
                 self.dying = False
                 self.is_alive = False
             else:
                 self.image = self._sprites_dying_left[int(self.current_death_sprite)]

        elif self.direction == "right":
            if self.current_death_sprite >= len(self._sprites_dying_right):
                 self.current_death_sprite = 0
                 self.is_animating = False
                 self.dying = False
                 self.is_alive = False
            else:
                 self.image = self._sprites_dying_right[int(self.current_death_sprite)]

    def update(self) -> None:
        """Atualiza a animação base do inimigo 
        """
        animation_speed = 0.10
        if self.is_attacking:
            self.current_sprite += animation_speed
            if(self.direction == "right"):
                if self.walking:
                    if self.current_sprite >= len(self._sprites_moving_right):
                        self.current_sprite = 0
                        self.is_animating = False
                    self.image = self._sprites_moving_right[int(self.current_sprite)]
                else:
                    if self.current_sprite >= len(self._sprites_idle_right):
                        self.current_sprite = 0
                        self.is_animating = False
                    self.image = self._sprites_idle_right[int(self.current_sprite)]
        elif self.is_animating:
            if(self.direction == "right"):
                if self.walking:
                    self.current_sprite += self.walking_animation_speed
                    if self.current_sprite >= len(self._sprites_moving_right):
                        self.current_sprite = 0
                        self.is_animating = False
                    self.image = self._sprites_moving_right[int(self.current_sprite)]
                else:
                    self.current_sprite += self.idle_animation_speed
                    if self.current_sprite >= len(self._sprites_idle_right):
                        self.current_sprite = 0
                        self.is_animating = False
                    self.image = self._sprites_idle_right[int(self.current_sprite)]

            if(self.direction == "left"):
                if self.walking:
                    self.current_sprite += self.walking_animation_speed
                    if self.current_sprite >= len(self._sprites_moving_left):
                        self.current_sprite = 0
                        self.is_animating = False
                    self.image = self._sprites_moving_left[int(self.current_sprite)]
                else:
                    self.current_sprite += self.idle_animation_speed
                    if self.current_sprite >= len(self._sprites_idle_left):
                        self.current_sprite = 0
                        self.is_animating = False
                    self.image = self._sprites_idle_left[int(self.current_sprite)]
            


class Shooter(Enemy):
    def __init__(self, inital_pos : list) -> None:
        super().__init__()
        #Sprites and animation
        #TODO: Change walking to waking

        self._import_sprites(5,'CharacterSprites/shooter/wakePNGright', self._sprites_idle_right)
        self._import_sprites(5,'CharacterSprites/shooter/wakePNGleft', self._sprites_idle_left)
        self._import_sprites(5,'CharacterSprites/shooter/wakePNGright', self._sprites_moving_right)
        self._import_sprites(5,'CharacterSprites/shooter/wakePNGleft', self._sprites_moving_left)
        self._import_sprites(6,'CharacterSprites/shooter/deathPNGleft', self._sprites_dying_left)
        self._import_sprites(6,'CharacterSprites/shooter/deathPNGright', self._sprites_dying_right)
        self._import_sprites(2,'CharacterSprites/shooter/hitPNGright', self._sprites_hit_right)
        self._import_sprites(2,'CharacterSprites/shooter/hitPNGleft', self._sprites_hit_left)

        self.image = self._sprites_idle_right[self.current_sprite]
        self.type = "Shooter"

        # Default Position and movement
        self.pos_x = inital_pos[0]
        self.pos_y = inital_pos[1]
        self.width = 55
        self.height = 65
        self.rect = pygame.Rect(self.pos_x, self.pos_y,  self.width, self.height)
        self.rect.topleft = [self.pos_x, self.pos_y]
        self.hitbox_rect = pygame.Rect(self.pos_x+85, self.pos_y-50, 45, 68)
        self.hitbox_rect.topleft = [self.pos_x, self.pos_y]
        self.attack_rect = pygame.Rect(self.pos_x+60, self.pos_y-60, 15, 15)
        self.attack_rect.topleft = [self.pos_x, self.pos_y]
        self.speed = 1
        self.actual_pos = 0
        self.death_animation_speed = 0.12
        self.idle_animation_speed = 0.10
        self.bullet_distance = 0
        self.bullet_direction = "left"
        self.has_attack_rect = True

        # Stats
        self.contact_dmg = 5
        self.attack_dmg = 5
        self.hp = 25
        self.coins_value = 500

    def move_rects_toplefts(self, new_pos_x: int, new_pos_y: int) -> None:
        if self.is_alive:
            self.hitbox_rect.topleft = [new_pos_x+48, new_pos_y+32]
        if self.bullet_direction == "left":
            self.attack_rect.topleft = [new_pos_x+20 - self.bullet_distance, new_pos_y+55]
        else:
            self.attack_rect.topleft = [new_pos_x+100 + self.bullet_distance, new_pos_y+55]
        if self.bullet_distance%800 == 0:
            self.bullet_distance = 0
            if self.direction == "left": 
                self.bullet_direction = "left"
            else: 
                self.bullet_direction = "right"
        self.bullet_distance += 4

    def is_atk(self) -> bool:
        return True

class Ghoul(Enemy):
    def __init__(self, inital_pos : list) -> None:
        super().__init__()
        #Sprites and animation

        self._import_sprites(6,'CharacterSprites/Ghoul/idlePNGright', self._sprites_idle_right)
        self._import_sprites(6,'CharacterSprites/Ghoul/idle2PNGleft', self._sprites_idle_left)
        self._import_sprites(9,'CharacterSprites/Ghoul/movementPNGright', self._sprites_moving_right)
        self._import_sprites(9,'CharacterSprites/Ghoul/movementPNGleft', self._sprites_moving_left)
        self._import_sprites(8,'CharacterSprites/Ghoul/deathPNGright', self._sprites_dying_right)
        self._import_sprites(8,'CharacterSprites/Ghoul/deathPNGleft', self._sprites_dying_left)
        self._import_sprites(4,'CharacterSprites/Ghoul/hitPNGright', self._sprites_hit_right)
        self._import_sprites(4,'CharacterSprites/Ghoul/hitPNGleft', self._sprites_hit_left)

        self.image = self._sprites_idle_right[self.current_sprite]
        self.type = "Ghoul"

        # Default Position and movement
        self.pos_x = inital_pos[0]
        self.pos_y = inital_pos[1]
        self.width = 55
        self.height = 65
        self.rect = pygame.Rect(self.pos_x, self.pos_y,  self.width, self.height)
        self.rect.topleft = [self.pos_x, self.pos_y]
        self.hitbox_rect = pygame.Rect(self.pos_x+85, self.pos_y-50, 34, 93)
        self.hitbox_rect.topleft = [self.pos_x, self.pos_y]
        self.speed = 1
        self.actual_pos = 0
        self.idle_animation_speed = 0.06

        # Stats
        self.contact_dmg = 3
        self.attack_dmg = 5
        self.hp = 40
        self.coins_value = 1000

    def move_rects_toplefts(self, new_pos_x: int, new_pos_y: int) -> None:
        if self.is_alive:
            self.hitbox_rect.topleft = [new_pos_x+107, new_pos_y+36]

    def is_atk(self) -> None:
        return False
    

class Flower(Enemy):
    def __init__(self, inital_pos : list) -> None:
        super().__init__()
        #Sprites and animation

        self._import_sprites(17,'CharacterSprites/flower/idle2PNGright', self._sprites_idle_right)
        self._import_sprites(17,'CharacterSprites/flower/idle2PNGleft', self._sprites_idle_left)
        self._import_sprites(12,'CharacterSprites/flower/attackPNGright', self._sprites_attack_right)
        self._import_sprites(12,'CharacterSprites/flower/attackPNGleft', self._sprites_attack_left)
        self._import_sprites(4,'CharacterSprites/flower/deathPNGright', self._sprites_dying_right)
        self._import_sprites(4,'CharacterSprites/flower/deathPNGleft', self._sprites_dying_left)
        self._import_sprites(2,'CharacterSprites/flower/hitPNGright', self._sprites_hit_right)
        self._import_sprites(2,'CharacterSprites/flower/hitPNGleft', self._sprites_hit_left)

        self.image = self._sprites_idle_left[self.current_sprite]
        self.type = "Flower"

        # Default Position and movement
        self.pos_x = inital_pos[0]
        self.pos_y = inital_pos[1]
        self.width = 55
        self.height = 65
        self.rect = pygame.Rect(self.pos_x, self.pos_y,  self.width, self.height)
        self.rect.topleft = [self.pos_x, self.pos_y]
        self.hitbox_rect = pygame.Rect(self.pos_x+83, self.pos_y-50, 40, 40)
        self.hitbox_rect.topleft = [self.pos_x-5, self.pos_y]
        self.attack_rect = pygame.Rect(self.pos_x+65, self.pos_y-90, 120, 85)
        self.attack_rect.topleft = [self.pos_x+15, self.pos_y+45]
        self.speed = 1
        self.actual_pos = 0
        self.has_attack_rect = True

        # Stats
        self.contact_dmg = 3
        self.attack_dmg = 7
        self.hp = 35
        self.coins_value = 100
        
    def is_atk(self) -> bool:
        """Retorna verdadeiro caso o objeto esteja na parte de ataque da animação.
        """
        if 1 <= self.current_sprite <= 7:
            return True
        return False

    def move_rects_toplefts(self, new_pos_x: int, new_pos_y: int) -> None:
        if self.is_alive:
            self.hitbox_rect.topleft = [new_pos_x+48, new_pos_y+92]
            self.attack_rect.topleft = [new_pos_x+5, new_pos_y+45]


class Little_Spider(Enemy):
    def __init__(self, inital_pos : list, move_set_number = 0) -> None:
        super().__init__()
        #Sprites and animation

        self._import_sprites(1,'CharacterSprites/little_spider/idlePNGright', self._sprites_idle_right)
        self._import_sprites(1,'CharacterSprites/little_spider/idlePNGleft', self._sprites_idle_left)
        self._import_sprites(6,'CharacterSprites/little_spider/movementPNGright', self._sprites_moving_right)
        self._import_sprites(6,'CharacterSprites/little_spider/movementPNGleft', self._sprites_moving_left)
        self._import_sprites(6,'CharacterSprites/little_spider/deathPNGright', self._sprites_dying_right)
        self._import_sprites(6,'CharacterSprites/little_spider/deathPNGleft', self._sprites_dying_left)
        self._import_sprites(2,'CharacterSprites/little_spider/hitPNGright', self._sprites_hit_right)
        self._import_sprites(2,'CharacterSprites/little_spider/hitPNGleft', self._sprites_hit_left)

        self.image = self._sprites_idle_right[self.current_sprite]
        self.type = "Little Spider"

        # Default Position and movement
        self.pos_x = inital_pos[0]
        self.pos_y = inital_pos[1]
        self.width = 96
        self.height = 65
        self.rect = pygame.Rect(self.pos_x, self.pos_y,  self.width, self.height)
        self.rect.topleft = [self.pos_x, self.pos_y]
        self.hitbox_rect = pygame.Rect(self.pos_x+85, self.pos_y+10, 30, 30)
        self.speed = 1
        self.actual_pos = 0

        # Stats
        self.move_set_number = move_set_number
        self.contact_dmg = 3
        self.hp = 12
        self.coins_value = 50

    def move_set(self) -> None:
        """ Garante uma movimentação fixa do objeto.
        """
        if self.move_set_number == 0:
            right_limit = 90
            left_limit = -30
        elif self.move_set_number == 1:
            right_limit = 120
            left_limit = -60  
        elif self.move_set_number == 2:
            right_limit = 75
            left_limit = -50

        self.actual_pos = self.actual_pos + self.speed
        if self.actual_pos >= right_limit:
            self.speed = -1
            self.direction = "left"
        elif self.actual_pos <= left_limit:
            self.speed = 1
            self.direction = "right"

        self.update_position(self.speed, 0)

    def move_rects_toplefts(self, new_pos_x: int, new_pos_y: int) -> None:
        self.hitbox_rect.topleft = [new_pos_x + 2, new_pos_y + 35]

    def is_atk(self) -> None:
        return False

class Enemy_Group:
    """
    Essa classe agrupa os inimigos criados em um vetor, e seus métodos chamam métodos de cada entidade 
    dentro desse vetor. Por exemplo, atualiza-se a animação de todos os inimigos ao mesmo tempo.
    """
    def __init__(self, enemy_group_number : int) -> None:
        super().__init__()
        self.enemy_vector = []
        self.enemy_group_number = enemy_group_number

        if enemy_group_number == 0:
            enemy4 = Flower([0, 2000])
            self.enemy_vector = numpy.array([enemy4])

        elif enemy_group_number == 1:
            enemy2 = Little_Spider([760, 44])
            enemy3 = Little_Spider([1500, 362])
            enemy4 = Flower([2000, 300])
            enemy5 = Flower([1800, 300])
            enemy6 = Little_Spider([2300, 362])
            self.enemy_vector = numpy.array([ enemy2, enemy3, enemy4, enemy5, enemy6])

        elif enemy_group_number == 2:
            enemy0 = Little_Spider([400, 363], 1)
            enemy1 = Little_Spider([300, 363])
            enemy2 = Little_Spider([1700, 680], 2)
            enemy3 = Little_Spider([1800, 680], 1)
            enemy4 = Little_Spider([1900, 680])
            enemy5 = Flower([1900, 780])
            enemy6 = Flower([1750, 780])
            enemy7 = Flower([1350, 780])
            self.enemy_vector = numpy.array([enemy0, enemy1, enemy2, enemy3, enemy4, enemy5, enemy6, enemy7])
        
        elif enemy_group_number == 3:
            enemy0 = Shooter([1040, 808])
            enemy1 = Shooter([1220, 648])
            enemy2 = Shooter([1380, 490])
            enemy3 = Flower([2200, -20])
            enemy4 = Flower([1950, -20])
            self.enemy_vector = numpy.array([enemy0, enemy1, enemy2, enemy3, enemy4])

        elif enemy_group_number == 4:
            enemy0 = Little_Spider([250, 45])
            enemy1 = Shooter([1930, 44])
            enemy2 = Shooter([1900, 363])
            enemy3 = Shooter([640, 644])
            enemy4 = Flower([1500, 780])
            enemy5 = Ghoul([2300, -100])
            self.enemy_vector = numpy.array([enemy0, enemy1, enemy2, enemy3, enemy4, enemy5])

        elif enemy_group_number == 5:
            little_spider = Little_Spider([0, 2000])
            self.enemy_vector = numpy.array([little_spider])
        
        elif enemy_group_number == 6:
            little_spider = Little_Spider([0, 2000])
            self.enemy_vector = numpy.array([little_spider])
        
        elif enemy_group_number == 7:
            little_spider = Little_Spider([0, 2000])
            self.enemy_vector = numpy.array([little_spider])
        
        elif enemy_group_number == 8:
            little_spider = Little_Spider([0, 2000])
            self.enemy_vector = numpy.array([little_spider])

    def update_enemies_sprites(self) -> None:
        for enemy in self.enemy_vector:
            if enemy.is_alive:
                enemy.animate()
                enemy.update()

    def follow_player(self, pos_player_x:int, offset_x:int) -> None:
        for enemy in self.enemy_vector:
            if (not enemy.type == "Little Spider") and (not enemy.dying):
                if (enemy.pos_x < pos_player_x-offset_x):
                    enemy.direction = "right"
                elif (enemy.pos_x > pos_player_x-offset_x):
                    enemy.direction = "left"

    def draw_enemies(self, screen: pygame.display, off_set_x: int, off_set_y: int) -> None:
        """Desenha os inimigos na tela e muda a posicao com o valor dos off_sets.

        Args:
            off_set_x : Modifica a posição do desenho do inimigo no eixo x (Obs: esse valor preferencialmente deve ser
            o off_set_x do mapa, para que o desenho do inimigo sempre esteja alinhado com as imagens do mapa)
            off_set_y : idem para a posição y, segue a mesma observação 
        """

        for enemy in self.enemy_vector:
            if enemy.is_alive:
                screen.blit(enemy.image, (enemy.rect.x + off_set_x, enemy.rect.y - off_set_y))

    def draw_collisions_rects(self, screen: pygame.display) -> None:
        """Desenha os rects dos inimigos na tela.

        Função de uso estrito para testes relacionados aos rects.
        """
        green = (0, 255, 0)
        white = (200, 200, 200)
        red = (255, 0, 0)
        for enemy in self.enemy_vector:
            if enemy.type == "Shooter" and not enemy.dying:
                    pygame.draw.rect(screen, white, enemy.attack_rect, 10)
                    nada = 0
            #if enemy.is_alive:
                 #pygame.draw.rect(screen, green, enemy.hitbox_rect, 1)
                #if enemy.has_attack_rect:
                    #pygame.draw.rect(screen, red, enemy.attack_rect, 1)

    
    def define_pos_group(self, delta_x: int, delta_y: int) -> None:
        """Atualiza a posicao do conjunto de inimigos. 

        Args:
            delta_x: O quanto o valor de posição em x vai se modificar
            delta_y: idem para a posição em y
        """
        for enemy in self.enemy_vector:
            if enemy.is_alive:
                new_pos_x = enemy.rect.x + delta_x
                new_pos_y = enemy.rect.y - delta_y
                enemy.move_rects_toplefts(new_pos_x, new_pos_y)

    def set_move_sets(self) -> None:
        for enemy in self.enemy_vector:
            if enemy.is_alive and enemy.type == "Little Spider":
                enemy.move_set()

    def check_deaths(self) -> None:
        """Verifica se algum inimigo morreu e toma as ações necessárias.

        Se algum inimigo estiver morto, seu rect de hitbox e de ataque é reposicionado para não afetar o player, ele entra em estado de morte
        e é permitido que sua animação de morte seja chamada na classe game.
        """
        for enemy in self.enemy_vector:
            if enemy.hp <= 0 and enemy.is_alive:
                enemy.dying = True
                enemy.hitbox_rect.topleft = [0, 2000]
                if enemy.has_attack_rect:
                    enemy.attack_rect.topleft = [0, 2000]

    def animate_deaths(self) -> None:
        """Anima as mortes de cada inimigo do vetor caso ele esteja morrendo.
        """
        for enemy in self.enemy_vector:
            if enemy.dying:
                enemy.animate_death()

    def animate_hits(self) -> None:
        """Faz a animação de hit de cada inimigo do vetor caso ele tenha sido acertado por um ataque.
        """
        for enemy in self.enemy_vector:
            if enemy.was_hit and not enemy.dying:
                enemy.animate_hit()

    def destruct_dead_enemies(self) -> None:
        """Apaga do vetor os inimigos que já passaram pela animação de morte.
        """
        for i, enemy in numpy.ndenumerate(self.enemy_vector):
            if not enemy.is_alive and not enemy.dying:
                enemy.hitbox_rect = None
                numpy.delete(self.enemy_vector, i)