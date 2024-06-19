from abc import ABC, abstractmethod
import pygame
import enemy
import Npcs

class CameraInterface(ABC):
    @abstractmethod
    def off_set_map(self, off_set_x : int, off_set_y : int) -> None:
        pass

    @abstractmethod
    def follow_player(self) -> None:
        pass

    @abstractmethod
    def keep_enemy_pos(self, screen: pygame.display, enemies : enemy.Enemy_Group) -> None:
        pass

    @abstractmethod
    def keep_npc_pos(self, screen: pygame.display, npc: Npcs) -> None:
        pass