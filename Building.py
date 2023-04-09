import arcade, random
from Components import *
from People import *

class BaseBuilding(arcade.Sprite):
    def __init__(self, game, x: float, y: float, health: float, dmg: float, range: int, max_len: int, texture: str,
                 scale=1):
        super().__init__(texture, center_x=x, center_y=y, scale=scale)

        self.texture = arcade.load_texture(texture)
        self.center_x = x
        self.center_y = y
        self.hit_box = self.texture.hit_box_points
        self.path = False

        self.dmg = dmg
        self.health = health
        self.max_health = self.health
        self.health_bar = HealthBar(game, position=self.position)
        self.health_bar.fullness = self.health / self.max_health
        self.range = range

        self.list_of_people = []
        self.max_length = max_len

        self.check_timer = 0
        self.enemy = None
        self.vars = {}

        self.timer = 0

    def add(self, sprite):
        if len(self.list_of_people) == self.max_length:
            return True
        self.list_of_people.append(sprite)
        sprite.health_bar.visible = False
        sprite.remove_from_sprite_lists()
        return False

    def remove(self):
        if len(self.list_of_people) == 0:
            return
        sprite = self.list_of_people[0]
        sprite.health_bar.visible = True
        self.list_of_people.pop(0)
        return sprite

    def destroy(self, game, menu_destroy=False):
        game.BuildingChangeEnemySpawner(self.center_x, self.center_y, placing=-1, min_dist=150, max_dist=200)
        self.remove_from_sprite_lists()
        self.health_bar.remove_from_sprite_lists()

        self.health = -100

    def on_destroy(self, source):
        self.destroy(source.game, source.menu_destroy)

    def clicked(self, game):
        game.clear_uimanager()
        if game.last == self:
            game.last = None
            return
        game.last = self

        button = CustomUIFlatButton(game.Alphabet_Textures, text="Destroy", width=140, height=50, x=0, y=50,
                                    text_offset_x=10, text_offset_y=35, offset_x=65, offset_y=25)
        button.on_click = game.destroy
        button.obj = self
        wrapper = arcade.gui.UIAnchorWidget(anchor_x="center_x", anchor_y="center_y",
                                            child=button, align_x=100, align_y=-200)
        game.uimanager.add(wrapper)
        game.extra_buttons.append(wrapper)

        self.clicked_override(game)

    def clicked_override(self, game):
        pass

    def update(self, game, delta_time):
        for resource, amount in self.vars.items():
            vars(game)[resource] += amount * delta_time * vars(game)[resource + "_multiplier"] / self.max_length * len(
                self.list_of_people) * game.overall_multiplier
        self.on_update(game, delta_time)

    def on_update(self, game, delta_time):
        if self.health <= 0:
            self.destroy(game)
        self.health_bar.fullness = self.health / self.max_health

        if self.enemy:
            if arcade.get_distance_between_sprites(self, self.enemy) < self.range:
                self.on_attack(game, delta_time)
        else:
            self.check_timer += delta_time
            if self.check_timer < 1:
                return
            self.check_timer -= 1
            enemy, distance = arcade.get_closest_sprite(self, game.Enemies)
            self.enemy = enemy
            print(enemy)

    def on_attack(self, game, delta_time):
        self.enemy.health -= self.dmg
        if self.enemy.health < 0:
            self.enemy.destroy(game)
            self.enemy = None

    def save(self, game):
        if self.enemy:
            self.enemy = game.Enemies.index(self.enemy)
        self.health_bar.remove_from_sprite_lists()

    def load(self, game):
        if self.enemy:
            self.enemy = game.Enemies[self.enemy]
        game.health_bars.append(self.health_bar._background_box)
        game.health_bars.append(self.health_bar._full_box)


class SnowTower(BaseBuilding):
    def __init__(self, game, x: float, y: float):
        super().__init__(game, x, y, 50, 2, 250, 1, "resources/Sprites/SnowTower.png")
        self.vars = {}
        self.Updates = False
        self.canAttack = True

        self.snowballs = arcade.SpriteList()
        self.focused_on = None
        self.WaitToAttack = 1

    """
    def update(self, game, delta_time):
        if self.health <= 0:
            self.destroy(game)
            return
        self.on_update(game, delta_time)

        for snowball in self.snowballs:
            snowball.forward(speed=delta_time * 50)
            snowball.update()
            snowball.time += delta_time
            if snowball.time > 15:
                snowball.remove_from_sprite_lists()
            elif not self.focused_on:
                break
            elif arcade.get_distance(snowball.center_x, snowball.center_y, self.focused_on.center_x,
                                     self.focused_on.center_y) < 25:
                self.focused_on.health -= self.damage * random.random() * random.random() * 4
                snowball.remove_from_sprite_lists()

        self.timer += delta_time
        if self.timer < self.WaitToAttack:
            return
        self.timer -= self.WaitToAttack
        self.canAttack = True

    def on_attack(self, game, delta_time):
        if not self.canAttack or not self.focused_on:
            return
        angle = rotation(self.center_x, self.center_y, self.focused_on.center_x, self.focused_on.center_y,
                         max_turn=360) + random.randrange(-5, 5)
        snowball = arcade.Sprite("resources/Sprites/Snowball.png", scale=1, center_x=self.center_x,
                                 center_y=self.center_y, angle=angle)
        snowball.time = 0
        self.snowballs.append(snowball)
        game.overParticles.append(snowball)
        snowball.forward()
        snowball.update()"""

class Carrot(BaseBuilding):
    def __init__(self, game, x: float, y: float):
        super().__init__(game, x, y, 50, .5, 250, 1, "resources/Sprites/food.png")
        self.Updates = False
        self.canAttack = True
        self.focused_on = None

        game.population += 1
        person = Person(game, x, y)
        game.People.append(person)
    def on_update(self, game, delta_time):
        self.remove_from_sprite_lists()


class PetBomb(BaseBuilding):
    def __init__(self, game, x: float, y: float):
        super().__init__(game, x, y, 50, .5, 250, 1, "resources/Sprites/Pet.png", scale = 5)
        self.Updates = False
        self.canAttack = True
        self.focused_on = None

    def on_update(self, game, delta_time):
        output = arcade.check_for_collision_with_list(self, game.Enemies)
        if not output: return
        for enemy in output: enemy.health -= 50
        self.remove_from_sprite_lists()


class Heal(BaseBuilding):
    def __init__(self, game, x: float, y: float):
        super().__init__(game, x, y, 50, .5, 250, 1, "resources/Sprites/Seringe.png", scale = .1)
        self.Updates = False
        self.canAttack = True
        self.focused_on = None

        for people in arcade.check_for_collision_with_list(self, game.People):
            people.health = 100

    def on_update(self, game, delta_time):
        self.remove_from_sprite_lists()
