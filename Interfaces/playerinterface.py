from abc import ABC, abstractmethod
import pygame
import map

#TODO: fazer docstring da classe
class PlayerInterface(ABC):
    @abstractmethod
    def hp_bar_change(self) -> None:
        pass

    @abstractmethod
    def heal(self) -> None:
        pass

    @abstractmethod
    def reinitialize_position_advancing(self, map: map, pos_y: int) -> None:
        pass

    @abstractmethod
    def reinitialize_position_returning(self, map: map, off_set_x: int, pos_y: int) -> None:
        pass

    @abstractmethod
    def update_position(self, new_pos_x: int, new_pos_y: int) -> None:
        pass

    @abstractmethod
    def apply_delta_gravity_effect(self, delta_t: float, map: map) -> None:
        pass

    @abstractmethod
    def correct_ground_intersection(self, map: map) -> None:
        pass
    
    @abstractmethod
    def is_colliding(self, map: map, direction: str) -> bool:
        pass
        
    @abstractmethod
    def is_advancing_room(self, map: map) -> bool:
        pass
    
    @abstractmethod
    def is_returning_room(self, map: map) -> bool:
        pass

    @abstractmethod
    def animate_attack(self) -> None:
        pass

    @abstractmethod
    def animate_land(self) -> None:
        pass

    @abstractmethod
    def animate_death(self) -> None:
        pass

    @abstractmethod
    def animate_hit(self) -> None:
        pass
         
    @abstractmethod
    def animate(self) -> None:
        pass

    @abstractmethod
    def update(self) -> None:
        pass

    @abstractmethod
    def draw_collision_rect(self, screen: pygame.display) -> None:
        pass