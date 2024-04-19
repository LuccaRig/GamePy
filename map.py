import pygame
import pytmx

class Map():
    def __init__(self, map_folder) -> None:
        self.tmx_map = pytmx.load_pygame(map_folder)
        self.tile_width = self.tmx_map.tilewidth
        self.tile_height = self.tmx_map.tileheight
        self.scale_factor = 10
        self.x_correction = 0
        self.y_correction = 0
        pass

    #TODO: fazer docstring
    def render_visible_layers(self, screen: pygame.display, off_set_x, off_set_y):
            for layer in self.tmx_map.visible_layers:
                if isinstance(layer, pytmx.TiledTileLayer):
                    # Se é uma camada de tile, renderize os tiles
                    for x, y, gid in layer:
                        tile = self.tmx_map.get_tile_image_by_gid(gid)
                        if tile is not None:
                            scaled_x = x * self.tile_width * self.scale_factor + self.x_correction
                            scaled_y = y * self.tile_height * self.scale_factor - self.y_correction
                            scaled_image = pygame.transform.scale(tile, (self.tile_width * self.scale_factor, 
                                                                         self.tile_height * self.scale_factor))
                            screen.blit(scaled_image, (scaled_x + off_set_x, scaled_y - off_set_y))
                elif isinstance(layer, pytmx.TiledObjectGroup):
                # Se é um grupo de objetos, renderize os objetos
                    for obj in layer:
                        if obj.name == "Collision":
                            scaled_x = obj.x * self.scale_factor + self.x_correction
                            scaled_y = obj.y * self.scale_factor - self.y_correction
                            scaled_width = obj.width * self.scale_factor
                            scaled_height = obj.height * self.scale_factor
                            rect = pygame.Rect(scaled_x + off_set_x, scaled_y - off_set_y, scaled_width, scaled_height)
                            # Desenha um retângulo vermelho para representar a área de colisão, com uma borda de 1 pixel
                            pygame.draw.rect(screen, (255, 0, 0), rect, 1) 

    #TODO: fazer docstring
    def check_collision(self, player_rect: pygame.rect) -> bool:
        for layer in self.tmx_map.visible_layers:
            if isinstance(layer, pytmx.TiledObjectGroup):
                for obj in layer:
                    if obj.name == "Collision":
                        rect = pygame.Rect(obj.x * self.scale_factor + self.x_correction, obj.y * self.scale_factor - self.y_correction, 
                                           obj.width * self.scale_factor, obj.height * self.scale_factor)
                        if player_rect.colliderect(rect):
                            #print("Colisão detectada")
                            return True
        #print("Colisão não detectada")
        return False