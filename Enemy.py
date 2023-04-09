import arcade, random, os
from Components import *


class BaseEnemy(arcade.Sprite):
    def __init__(self, game, file_name:str, x:float, y:float, health:float, damage:float, range:int, scale:float=1):
        super().__init__(file_name, center_x=x, center_y=y, scale=scale)
        self.texture = arcade.load_texture(file_name)
        self.center_x = x
        self.center_y = y
        self.hit_box = self.texture.hit_box_points

        self.damage = damage
        self.health = health
        self.range = range
        self.state = "Idle"

        self.barriers = []
        self.path = []
        self.path_timer = 0

        self.check = True
        self.rotation = 0
        self.next_time = .5

        self.max_health = self.health
        self.health_bar = HealthBar(game, position = (self.center_x, self.center_y-50))
        self.health_bar.fullness = self.health/self.max_health

    def destroy(self, game):
        self.remove_from_sprite_lists()
        self.health_bar.remove_from_sprite_lists()
        self.health = -100

        game.money += 5
    def get_path(self):
        if type(self.path) != list:
            return None
        elif len(self.path) == 0:
            return None

        path = self.path[0]
        self.path.pop(0)
        return path
    #NOTE: over ride the function
    def update(self, game, delta_time):
        if self.health <= 0:
            self.destroy(game)
            return 
        self.on_update(game, delta_time)
        self.update_movement(game, delta_time)
    #NOTE: Always call on_update in update
    def on_update(self, game, delta_time):
        self.health_bar.fullness = self.health/self.max_health
        if self.state == "Attack":
            self.state = "Idle"
        if self.focused_on:
            if arcade.get_distance_between_sprites(self, self.focused_on) <= self.range:
                self.on_attack(game, delta_time)
            elif len(self.path) < 1:
                self.check = True
            elif self.check:
                game.calculate_enemy_path(self)
                self.check = False
            if self.focused_on.health <= 0:
                self.focused_on.destroy(game)
                self.focused_on = None
                self.check = True
        if self.check:
            game.calculate_enemy_path(self)
        return True
    def update_movement(self, game, delta_time):
        self.path_timer += delta_time
        if self.path_timer > self.next_time:
            pos = self.get_path()
            if pos is not None:
                self.position = pos
                self.health_bar.position = self.center_x, self.center_y-50
            self.path_timer -= self.next_time
            #self.next_time = difficulty[game["map"][round(self.center_x/50)][round(self.center_y/50)]]
    def on_attack(self, game, delta_time):
        self.focused_on.health -= self.damage*delta_time*random.random()*random.random()*4
    def On_Focused_on(self):
        pass
    
    def save(self, game):
        if not self.focused_on:
            return
        if self.focused_on.__module__ == "Buildings":
            index = game.Buildings.index(self.focused_on)
            sprite_list_name = "Buildings"
        elif self.focused_on.__module__ == "Player":
            try:
                #if not boat except
                self.focused_on.capacity
                index = game.Boats.index(self.focused_on)
                sprite_list_name = "Boats"
            except:
                index = game.People.index(self.focused_on)
                sprite_list_name = "People"
        return (sprite_list_name, index)
    def load(self, game):
        if self.focused_on:
            self.focused_on = game[self.focused_on[0]][self.focused_on[1]]

class Enemy_Slinger(BaseEnemy):
    def __init__(self, game, x, y, difficulty=1):
        super().__init__(game, "resources/Sprites/enemy.png", x, y, 10*difficulty, 2*difficulty, 50, scale=.5)
        self.texture = arcade.load_texture("resources/Sprites/enemy.png", flipped_horizontally=True)

        self.movelist = [0]

        self.people_bias = 1
        self.building_bias = 1
        self.player_bias = 1
    
