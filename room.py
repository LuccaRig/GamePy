import pygame
import map

class Room():
    def __init__(self) -> None:
        self.my_maps = []
        self.import_maps(3, self.my_maps)
        self.current_map_position = 0

    def import_maps(self, number_of_maps: int, maps_vector= []) -> None:
        """Acessa a pasta Tiled e guarda os mapas (arquivos tmx) em um vetor de mapas

        Args:
            number_of_maps: número de mapas desejados
            maps_vector: vetor que vai armazenar os mapas
        """
        for i in range(number_of_maps):
            cmap = map.Map(f"Tiled/Map{i}.tmx")
            maps_vector.append(cmap) 

    def current_room(self) -> map:
        return self.my_maps[self.current_map_position]
    
    def advance_room(self) -> None:
        """Aumenta o índice do vetor de mapas
        
        """
        self.current_map_position += 1

    def return_room(self) -> None:
        """Diminui o índice do vetor de mapas
        
        """
        self.current_map_position -= 1

