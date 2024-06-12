import pygame
import pytmx
import npcs
import enemy

class Map():
    def __init__(self, map_folder , group) -> None:
        self.tmx_map = pytmx.load_pygame(map_folder)
        self.tile_width = self.tmx_map.tilewidth
        self.tile_height = self.tmx_map.tileheight
        self.scale_factor = 5
        self.x_correction = 0
        self.y_correction = 212
        self.off_set_x = 0
        self.off_set_y = 0

        self.pos_x_new_room = 0
        self.pos_y_new_room = 0
        self.pos_x_previous_room = 0
        self.pos_y_previous_room = 0

        self.map_number = group
        self.map_enemy_define()

    def render_visible_layers(self, screen: pygame.display, off_set_x: float, off_set_y: float) -> None:
        """Itera sobre a matriz do mapa para renderizar os tiles do mapas, assim como os objetos de colisão e de mudança de sala
        
        Args:
            screen: display no qual o jogo será aberto
            off_set_x: desvio no comprimento do mapa, que permite uma renderização mais otimizada por não precisar iterar a matriz inteira
            off_set_y: desvio na altura do mapa, que permite uma renderização mais otimizada por não precisar iterar a matriz inteira
        
        """
        #Valores que mostram a posição inicial e final das linhas e colunas visíveis no display
        set_x = int(off_set_x/5)
        set_y = int(off_set_y/5)
        start_col = max(-set_x // self.tile_width, 0)
        end_col = min((-set_x + 256) // self.tile_width, self.tmx_map.width - 1)
        start_row = max(set_y // self.tile_height, 0)
        end_row = min((set_y + 190) // self.tile_height, self.tmx_map.height - 1)
        
        for layer in self.tmx_map.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                # Se é uma camada de tile, renderize os tiles
                for x in range(start_col, end_col + 1):
                    for y in range(start_row, end_row + 1):
                        gid = layer.data[y][x]
                        if gid:
                            tile = self.tmx_map.get_tile_image_by_gid(gid)
                            if tile:
                                scaled_x = x * self.tile_width * self.scale_factor + self.x_correction
                                scaled_y = y * self.tile_height * self.scale_factor - self.y_correction
                                scaled_image = pygame.transform.scale(tile, (self.tile_width * self.scale_factor, 
                                                                            self.tile_height * self.scale_factor))
                                screen.blit(scaled_image, (scaled_x + self.off_set_x, scaled_y - self.off_set_y))
            elif isinstance(layer, pytmx.TiledObjectGroup):
            # Se é um grupo de objetos, renderize os objetos
                for obj in layer:
                    if obj.name == "Collision":
                        scaled_x = obj.x * self.scale_factor + self.x_correction
                        scaled_y = obj.y * self.scale_factor - self.y_correction
                        scaled_width = obj.width * self.scale_factor
                        scaled_height = obj.height * self.scale_factor
                        rect = pygame.Rect(scaled_x + self.off_set_x, scaled_y - self.off_set_y, scaled_width, scaled_height)
                        # Desenha um retângulo vermelho para representar a área de colisão, com uma borda de 1 pixel
                        # pygame.draw.rect(screen, (255, 0, 0), rect, 2) 
                    elif obj.name == "New Room":
                        self.pos_x_new_room = obj.x * self.scale_factor + self.x_correction
                        self.pos_y_new_room = obj.y * self.scale_factor - self.y_correction - self.off_set_y
                        scaled_width = obj.width * self.scale_factor
                        scaled_height = obj.height * self.scale_factor
                        rect = pygame.Rect(self.pos_x_new_room + self.off_set_x, self.pos_y_new_room, scaled_width, scaled_height)
                        # Desenha um retângulo verde para representar a área de colisão, com uma borda de 1 pixel
                        pygame.draw.rect(screen, (0, 255, 0), rect, 2) 
                    elif obj.name == "Previous Room":
                        self.pos_x_previous_room = obj.x * self.scale_factor + self.x_correction
                        self.pos_y_previous_room = obj.y * self.scale_factor - self.y_correction - self.off_set_y
                        scaled_width = obj.width * self.scale_factor
                        scaled_height = obj.height * self.scale_factor
                        rect = pygame.Rect(self.pos_x_previous_room + self.off_set_x, self.pos_y_previous_room, scaled_width, scaled_height)
                        # Desenha um retângulo azul para representar a área de colisão, com uma borda de 1 pixel
                        pygame.draw.rect(screen, (0, 0, 255), rect, 2) 

    #TODO: fazer docstring
    def check_collision(self, player_rect: pygame.rect) -> bool:
        for layer in self.tmx_map.visible_layers:
            if isinstance(layer, pytmx.TiledObjectGroup):
                for obj in layer:
                    if obj.name == "Collision":
                        rect = pygame.Rect(obj.x * self.scale_factor + self.x_correction + self.off_set_x, obj.y * self.scale_factor - self.y_correction - self.off_set_y, 
                                           obj.width * self.scale_factor, obj.height * self.scale_factor)
                        if player_rect.colliderect(rect):
                            #print("Colisão detectada")
                            return True
        #print("Colisão não detectada")
        return False
    
    #TODO: fazer docstring
    def return_ground_intersection(self, player_down_rect: pygame.rect) -> pygame.rect:
        for layer in self.tmx_map.visible_layers:
            if isinstance(layer, pytmx.TiledObjectGroup):
                for obj in layer:
                    if obj.name == "Collision":
                        rect = pygame.Rect(obj.x * self.scale_factor + self.x_correction + self.off_set_x, obj.y * self.scale_factor - self.y_correction - self.off_set_y, 
                                           obj.width * self.scale_factor, obj.height * self.scale_factor)
                        if player_down_rect.colliderect(rect):
                            intersection = rect.clip(player_down_rect)
                            return intersection
       
    
    def check_new_room(self, player_rect: pygame.rect) -> bool:
        """Retorna True se o retângulo do player estiver colidindo com um objeto "New Room" do map
        
        Args:
            player_rect: retângulo que permite a localização e identificação de colisões do player
        """
        for layer in self.tmx_map.visible_layers:
            if isinstance(layer, pytmx.TiledObjectGroup):
                for obj in layer:
                    if obj.name == "New Room":
                        rect = pygame.Rect(obj.x * self.scale_factor + self.x_correction + self.off_set_x, obj.y * self.scale_factor - self.y_correction - self.off_set_y, 
                                           obj.width * self.scale_factor, obj.height * self.scale_factor)
                        if player_rect.colliderect(rect):
                            return True
        return False
    
    def check_previous_room(self, player_rect: pygame.rect) -> bool:
        """Retorna True se o retângulo do player estiver colidindo com um objeto "Previous Room" do map
        
        Args:
            player_rect: retângulo que permite a localização e identificação de colisões do player
        """
        for layer in self.tmx_map.visible_layers:
            if isinstance(layer, pytmx.TiledObjectGroup):
                for obj in layer:
                    if obj.name == "Previous Room":
                        rect = pygame.Rect(obj.x * self.scale_factor + self.x_correction + self.off_set_x, obj.y * self.scale_factor - self.y_correction - self.off_set_y, 
                                           obj.width * self.scale_factor, obj.height * self.scale_factor)
                        if player_rect.colliderect(rect):
                            return True
        return False
    
    def map_npc_define(self):
        if self.map_number == 0:
            self.npc = npcs.Traveler([750, 300])

    def map_enemy_define(self):
        if self.map_number == 0:
            self.enemy_map_group = enemy.Enemy_Group(0)

        elif self.map_number == 1:
            self.enemy_map_group = enemy.Enemy_Group(1)

        else: self.enemy_map_group = None

