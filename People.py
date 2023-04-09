import random

import arcade
from Components import *

class Person(arcade.Sprite):
    def __init__(self, game, x, y):
        super().__init__("resources/Sprites/"+random.choice(["male.png", "female.png"]), center_x=x, center_y=y, scale = 2)

        self.health = random.randrange(20, 80)
        self.max_health = 100
        self.health_bar = HealthBar(game, position = self.position)
    def destroy(self, game):
        self.remove_from_sprite_lists()
        self.health_bar.remove_from_sprite_lists()
        game.population -= 1
    def update(self, game, delta_time):
        self.health_bar.fullness = self.health/self.max_health
