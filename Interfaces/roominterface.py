from abc import ABC, abstractmethod
import map
import Npcs
import enemy

class RoomInterface(ABC):
    @abstractmethod
    def import_maps(self, number_of_maps: int, maps_vector: list) -> None:
        pass

    @abstractmethod
    def first_time_in_room(self, number_of_maps: int, first_time_dictionary: dict) -> None:
        pass

    @abstractmethod
    def current_room(self) -> map:
        pass

    @abstractmethod
    def advance_room(self) -> None:
        pass

    @abstractmethod
    def return_room(self) -> None:
        pass

    @abstractmethod
    def current_room_npc(self) -> Npcs:
        pass

    @abstractmethod
    def current_room_enemies(self) -> enemy.Enemy_Group:
        pass
