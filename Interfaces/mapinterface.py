from abc import ABC, abstractmethod
import pygame

class MapInterface(ABC):
    @abstractmethod
    def render_visible_layers(self, screen: pygame.display, off_set_x: float, off_set_y: float) -> None:
        pass

    @abstractmethod
    def check_collision(self, player_rect: pygame.rect) -> bool:
        pass

    @abstractmethod
    def return_ground_intersection(self, player_down_rect: pygame.rect) -> pygame.rect:
        pass

    @abstractmethod   
    def check_new_room(self, player_rect: pygame.rect) -> bool:
        pass

    @abstractmethod
    def check_previous_room(self, player_rect: pygame.rect) -> bool:
        pass

    @abstractmethod
    def map_npc_define(self) -> None:
        pass
    
    @abstractmethod
    def map_enemy_define(self) -> None:
        pass