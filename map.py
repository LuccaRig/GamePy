import pygame
import pytmx

class Map():
    def __init__(self, map_folder) -> None:
        self.tmx_map = pytmx.load_pygame(map_folder)
        pass

    def renderVisibleLayers(self, screen):
        scale_factor = 10
        for layer in self.tmx_map.visible_layers:
            for x, y, image in layer.tiles():
                scaled_x = (x * self.tmx_map.tilewidth * scale_factor) + 300
                scaled_y = y * self.tmx_map.tileheight * scale_factor
                scaled_image = pygame.transform.scale(image, (self.tmx_map.tilewidth * scale_factor, self.tmx_map.tileheight * scale_factor))
                screen.blit(scaled_image, (scaled_x, scaled_y))