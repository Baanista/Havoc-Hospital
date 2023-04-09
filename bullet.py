import arcade
from Components import *
class BaseBullet(arcade.Sprite):
    def __init__(self, filename, x, y, scale, range, dmg, speed, accuracy):
        super().__init__(filename, center_x=x, center_y=y, scale=scale)
        self.time = range
        self.dmg = dmg
        self.speed = speed
        self.accuracy = accuracy


    def update(self, game, delta_time):
        self.time -= delta_time
        self.forward(self.speed * delta_time)
        self.center_x += self.change_x
        self.center_y += self.change_y
        if self.time < 0:
            self.remove_from_sprite_lists()

        enemy, dist = get_closest_sprite(self.position, game.Enemies)
        if dist < self.accuracy:
            enemy.health -= self.dmg
            self.remove_from_sprite_lists()


class RifleBullet(BaseBullet):
    def __init__(self, x, y, scale):
        super().__init__("resources/Sprites/bullet.png", x, y, scale, range = 100, dmg = 5, speed = 10, accuracy = 20)

