import player
import enemy
import map


class Camera():
    def __init__(self, map : map, player : player, screen) -> None:
        self.bounded_character = player
        self.bounded_map = map
        self.boundede_screen = screen
        self.off_set_x = 0
        self.off_set_y = 0 
        self.camera_is_moving = False


    def off_set_map(self, off_set_x : int, off_set_y : int) -> None:
        self.off_set_x += off_set_x
        self.bounded_map.off_set_x = self.off_set_x
        self.off_set_y += off_set_y
        self.bounded_map.off_set_y = self.off_set_y
        self.bounded_map.render_visible_layers(self.boundede_screen)

    def follow_player(self) -> None:
        if (self.off_set_x > -4) or (self.off_set_x < -1276):
            self.bounded_character.x_limit_reached = True
        else:
            self.bounded_character.x_limit_reached = False

        if (self.off_set_y < -212.5):
            self.bounded_character.y_limit_reached = True
        else:
            self.bounded_character.y_limit_reached = False


        if (self.bounded_character.rect.topleft[0] <= 400 and self.bounded_character.speed[0] < 0) and not(self.off_set_x > -4):
            self.off_set_map(4, 0)
        elif (self.bounded_character.rect.topleft[0] >= 720 and self.bounded_character.speed[0] > 0) and not(self.off_set_x < -1276):
            self.off_set_map(-4, 0)
        if (self.bounded_character.rect.topleft[1] <= 200 and self.bounded_character.vertical_speed > 0) and not(self.off_set_y < -212.5):
            self.off_set_map(0, -self.bounded_character.delta_pos_y)
        elif self.bounded_character.rect.topleft[1] >= 350 and self.bounded_character.falling and not self.bounded_character.is_colliding(self.bounded_map, "down"):
            self.off_set_map(0, -self.bounded_character.delta_pos_y)
        else:
            self.off_set_map(0, 0)

    def keep_enemy_pos(self, screen , enemies : enemy.Enemy_Group):
        enemies.draw_enemies(screen, self.off_set_x, self.off_set_y)
        enemies.define_pos_group(self.off_set_x, self.off_set_y)