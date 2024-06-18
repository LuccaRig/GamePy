from abc import ABC, abstractmethod
import pygame
import player

class NpcInterface(ABC):
    @abstractmethod
    def import_sprites(self, number_of_sprites : int, arquive : str, sprites_vector : list, scale=4) -> None:
        pass
    
    @abstractmethod
    def animate(self) -> None:
        pass

    @abstractmethod
    def update(self) -> None:
        pass

    @abstractmethod
    def draw_npc(self, screen: pygame.display, off_set_x: int, off_set_y: int) -> None:
        pass

    @abstractmethod
    def check_player_interaction(self, player: player) -> bool:
        pass
