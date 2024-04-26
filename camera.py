import player
import pytmx
import map
import pygame


class Camera():
    def __init__(self, map : map, player : player, screen) -> None:
        self.bounded_character = player
        self.bounded_map = map
        self.boundede_screen = screen
        self.off_set_x = 0
        self.off_set_y = 0


    def off_set_map(self, off_set_x : int, off_set_y : int) -> None:
        self.off_set_x += off_set_x
        self.bounded_map.off_set_x = self.off_set_x
        self.off_set_y += off_set_y
        self.bounded_map.off_set_y = self.off_set_y
        self.bounded_map.render_visible_layers(self.boundede_screen)

    def follow_player(self) -> None:
        if self.bounded_character.rect.topleft[0] <= 400 and self.bounded_character.horizontal_speed[0] < 0:
            self.off_set_map(4, 0)
        elif self.bounded_character.rect.topleft[0] >= 720 and self.bounded_character.horizontal_speed[0] > 0:
            self.off_set_map(-4, 0)
        if self.bounded_character.rect.topleft[1] <= 200 and self.bounded_character.vertical_speed > 0:
            self.off_set_map(0, -self.bounded_character.delta_pos_y)
        elif self.bounded_character.rect.topleft[1] >= 350 and self.bounded_character.falling:
            self.off_set_map(0, -self.bounded_character.delta_pos_y)
        else:
            self.off_set_map(0, 0)
