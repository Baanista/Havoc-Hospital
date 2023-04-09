import arcade
from GameView import *
from Components import *


SCREEN_WIDTH = 1440
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Better Move Sprite with Keyboard Example"
SPRITE_SCALING = 0.5
MOVEMENT_SPEED = 5

SIZE_X = 5000
SIZE_Y = 5000

class Player(arcade.Sprite):
    def __init__(self, game, filename, x, y):
        super().__init__(filename=filename, center_x=x, center_y=y)

        self.health = 100
        self.max_health = self.health
        self.health_bar = HealthBar(game, position = (self.center_x, self.center_y-50))
        self.health_bar.fullness = self.health/self.max_health
    def update(self):
        """ Move the player """
        # Move player.
        # Remove these lines if physics engine is moving player.

        self.center_x += self.change_x
        self.center_y += self.change_y

        if self.health < 100: self.health += 1/60
        
        self.health_bar.fullness = self.health/self.max_health
        self.health_bar.position = self.center_x, self.center_y-50
    def destroy(self, game):
        game.End()