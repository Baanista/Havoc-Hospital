import arcade, math

from collections import ChainMap
from typing import Optional, Tuple, Union

from pyglet.event import EVENT_UNHANDLED

import arcade
from arcade.experimental.uistyle import UISliderStyle
from arcade.gui import UIWidget, Surface, UIEvent, UIMouseMovementEvent, UIMouseDragEvent, UIMousePressEvent, \
    UIMouseReleaseEvent
from arcade.gui._property import _Property, _bind
from arcade.gui.events import UIOnChangeEvent

from pathlib import Path
from typing import Optional, Union
import pyglet.media as media



def get_dist(pos, pos2):
    return math.hypot(pos[0] - pos2[0], pos[1] - pos2[1])
def get_closest_sprite(pos, sprite_list):
    lowest_dist = float("inf")
    save = None
    for sprite in sprite_list:
        dist = get_dist(pos, sprite.position)
        if dist < lowest_dist:
            lowest_dist = dist
            save = sprite
    return save, lowest_dist
def rotation(x, y, x2, y2, angle=0, max_turn=5):
    x_diff = x2 - x
    y_diff = y2 - y
    target_angle_radians = math.atan2(y_diff, x_diff)
    if target_angle_radians < 0:
        target_angle_radians += 2 * math.pi
    actual_angle_radians = math.radians(angle)
    rot_speed_radians = math.radians(max_turn)
        # What is the difference between what we want, and where we are?
    angle_diff_radians = target_angle_radians - actual_angle_radians
        # Figure out if we rotate clockwise or counter-clockwise
    if abs(angle_diff_radians) <= rot_speed_radians:
        actual_angle_radians = target_angle_radians
        clockwise = None
    elif angle_diff_radians > 0 and abs(angle_diff_radians) < math.pi:
        clockwise = False
    elif angle_diff_radians > 0 and abs(angle_diff_radians) >= math.pi:
        clockwise = True
    elif angle_diff_radians < 0 and abs(angle_diff_radians) < math.pi:
        clockwise = True
    else:
        clockwise = False

    # Rotate the proper direction if needed
    if actual_angle_radians != target_angle_radians and clockwise:
        actual_angle_radians -= rot_speed_radians
    elif actual_angle_radians != target_angle_radians:
        actual_angle_radians += rot_speed_radians

        # Keep in a range of 0 to 2pi
    if actual_angle_radians > 2 * math.pi:
        actual_angle_radians -= 2 * math.pi
    elif actual_angle_radians < 0:
        actual_angle_radians += 2 * math.pi

    return math.degrees(actual_angle_radians)


class HealthBar:
    """
    Represents a bar which can display information about a sprite.

    :param MyGame Game: Game
    :param Tuple[float, float] position: The initial position of the bar.
    :param arcade.Color full_color: The color of the bar.
    :param arcade.Color background_color: The background color of the bar.
    :param int width: The width of the bar.
    :param int height: The height of the bar.
    :param int border_size: The size of the bar's border.
    """

    def __init__(
        self,
        game,
        position: Tuple[float, float] = (0, 0),
        full_color: arcade.Color = arcade.color.GREEN,
        background_color: arcade.Color = arcade.color.BLACK,
        width: int = 40,
        height: int = 4,
        border_size: int = 4,
    ) -> None:
        # Store the reference to the owner and the sprite list


        # Set the needed size variables
        self._box_width: int = width
        self._box_height: int = height
        self._half_box_width: int = self._box_width // 2
        self._center_x: float = 0.0
        self._center_y: float = 0.0
        self._fullness: float = 0.0

        # Create the boxes needed to represent the indicator bar
        self._background_box: arcade.SpriteSolidColor = arcade.SpriteSolidColor(
            self._box_width + border_size,
            self._box_height + border_size,
            background_color,
        )
        self._full_box: arcade.SpriteSolidColor = arcade.SpriteSolidColor(
            self._box_width,
            self._box_height,
            full_color,
        )
        game.health_bars.append(self._background_box)
        game.health_bars.append(self._full_box)

        # Set the fullness and position of the bar
        self.fullness: float = 1.0
        self.visible: bool = True
        self.position: Tuple[float, float] = position
    def remove_from_sprite_lists(self):
        self._background_box.remove_from_sprite_lists()
        self._full_box.remove_from_sprite_lists()

    @property
    def background_box(self) -> arcade.SpriteSolidColor:
        """Returns the background box of the indicator bar."""
        return self._background_box

    @property
    def full_box(self) -> arcade.SpriteSolidColor:
        """Returns the full box of the indicator bar."""
        return self._full_box

    @property
    def fullness(self) -> float:
        """Returns the fullness of the bar."""
        return self._fullness

    @fullness.setter
    def fullness(self, new_fullness: float) -> None:
        """Sets the fullness of the bar."""
        # Check if new_fullness if valid
        if 0.0 > new_fullness:
            new_fullness = 0
        elif 1.0 < new_fullness:
            new_fullness = 1

        # Set the size of the bar
        self._fullness = new_fullness

        self.full_box.width = self._box_width * new_fullness
        self.full_box.left = self._center_x - (self._box_width // 2)
    
    @property
    def visible(self) -> float:
        """Returns the visibility"""
        return self.visible
    @visible.setter
    def visible(self, visible) -> None:
        self._full_box.visible = visible
        self._background_box.visible = visible

    @property
    def position(self) -> Tuple[float, float]:
        """Returns the current position of the bar."""
        return self._center_x, self._center_y

    @position.setter
    def position(self, new_position: Tuple[float, float]) -> None:
        """Sets the new position of the bar."""
        # Check if the position has changed. If so, change the bar's position
        if new_position != self.position:
            new_position = new_position[0], new_position[1]-20
            self._center_x, self._center_y = new_position
            self.background_box.position = new_position
            self.full_box.position = new_position

            # Make sure full_box is to the left of the bar instead of the middle
            self.full_box.left = self._center_x - (self._box_width // 2)

class CustomUIFlatButton(arcade.gui.UIInteractiveWidget):
    """
    A text button, with support for background color and a border.

    :param float x: x coordinate of bottom left
    :param float y: y coordinate of bottom left
    :param float width: width of widget. Defaults to texture width if not specified.
    :param float height: height of widget. Defaults to texture height if not specified.
    :param str text: text to add to the button.
    :param style: Used to style the button

    """

    def __init__(self, 
                 Alphabet_Textures,
                 center_x: float = 0,
                 center_y: float = 0,
                 width: float = 100,
                 height: float = 60,
                 scale=1,
                 text="",
                 size_hint=None,
                 size_hint_min=None,
                 size_hint_max=None,
                 style=None, 
                 text_offset_x=0, text_offset_y = 0, 
                 text_scale=1, text_margin=16,  
                 offset_x=0, offset_y=0, 
                 line_spacing = 20,
                 Texture="resources/gui/Wood Button.png", Hovered_Texture="resources/gui/Wood Button.png", Pressed_Texture="resources/gui/Wood Button Pressed.png", 
                 click_sound = None,
                 **kwargs):
        super().__init__(center_x, center_y, width, height,
                         size_hint=size_hint,
                         size_hint_min=size_hint_min,
                         size_hint_max=size_hint_max)
        self.click_sound = click_sound
        self.clicked = False

        self._text = text
        self._style = style or {}
        
#image_width=width+50, image_height=height+50       image_width=width+607, image_height=height+303, 
        self.sprite = arcade.Sprite(filename=Texture, scale=scale, center_x=center_x+offset_x, center_y=center_x+offset_y)#arcade.load_texture(Texture)
        self.hovered_sprite = arcade.Sprite(filename=Hovered_Texture, scale=scale, center_x=center_x+offset_x, center_y=center_x+offset_y)#arcade.load_texture(Hovered_Texture)
        self.pressed_sprite = arcade.Sprite(filename=Pressed_Texture, scale=scale, center_x=center_x+offset_x, center_y=center_x+offset_y)#arcade.load_texture(Pressed_Texture)

        #game.spritelist.append(self.sprite)
        #game.spritelist.append(self.hovered_sprite)
        #game.spritelist.append(self.pressed_sprite)

        self.text_sprites = arcade.SpriteList()
        """
        if self.text:
            pos_x = -45+text_offset_x
            pos_y = 5+text_offset_y
            if len(text)*text_scale*text_margin > width:
                pos_y += 10
            for string in text:
                sprite = arcade.Sprite(center_x=x+offset_x+pos_x, center_y=y+offset_y+pos_y, scale=text_scale)
                sprite.texture = Alphabet_Textures[string]
                self.text_sprites.append(sprite)
                pos_x += text_margin
                if pos_x*text_scale > width-90:
                    pos_x = -45+text_offset_x
                    pos_y -= 24
        """
        """
        self.text_sprites.clear()
        if not text:
            return
        words = text.split(' ')
        x = text_offset_x
        y = text_offset_y
        for word in words:
            if x > width-90+x:
                y -= text_margin+text_offset_y
                x = text_offset_x
            for string in word:
                sprite = arcade.Sprite(center_x=center_x+x, center_y=center_y+y, scale=text_scale)
                sprite.texture = Alphabet_Textures[string]
                self.text_sprites.append(sprite)
                x += text_margin
            x += text_margin
        """

        self.line_spacing = line_spacing
        self.text_offset_x=text_offset_x
        self.text_offset_y = text_offset_y 
        self.text_scale=text_scale
        self.text_margin=text_margin
        self.offset_x=offset_x
        self.offset_y=offset_y

        
        self.set_text(text, Alphabet_Textures)
        self.scale(1.2)

    def do_render(self, surface: arcade.gui.Surface):
        self.prepare_render(surface)
        if self.pressed:
            self.pressed_sprite.draw()
            if self.click_sound and not self.clicked: 
                self.click_sound.play()
                self.clicked = True
        elif self.hovered:
            self.clicked = False
            self.hovered_sprite.draw()
        else:
            self.clicked = False
            self.sprite.draw()
        if self.text:
            self.text_sprites.draw()

            return
            font_name = self._style.get("font_name", ("calibri", "arial"))
            font_size = self._style.get("font_size", 15)
            font_color = self._style.get("font_color", arcade.color.WHITE)
            border_width = self._style.get("border_width", 2)

            start_x = self.width // 2
            start_y = self.height // 2

            text_margin = 2
            arcade.draw_text(
                text=self.text,
                start_x=start_x,
                start_y=start_y,
                font_name=font_name,
                font_size=font_size,
                color=font_color,
                align="center",
                anchor_x='center', anchor_y='center',
                width=self.width - 2 * border_width - 2 * text_margin
            )
    def do_render2(self, surface: arcade.gui.Surface):
        self.prepare_render(surface)

        # Render button
        font_name = self._style.get("font_name", ("calibri", "arial"))
        font_size = self._style.get("font_size", 15)
        font_color = self._style.get("font_color", arcade.color.WHITE)
        border_width = self._style.get("border_width", 2)
        border_color = self._style.get("border_color", None)
        bg_color = self._style.get("bg_color", (21, 19, 21))

        if self.pressed:
            bg_color = self._style.get("bg_color_pressed", arcade.color.WHITE)
            border_color = self._style.get("border_color_pressed", arcade.color.WHITE)
            font_color = self._style.get("font_color_pressed", arcade.color.BLACK)
        elif self.hovered:
            border_color = self._style.get("border_color_pressed", arcade.color.WHITE)

        # render BG
        if bg_color:
            arcade.draw_xywh_rectangle_filled(0, 0, self.width, self.height, color=bg_color)

        # render border
        if border_color and border_width:
            arcade.draw_xywh_rectangle_outline(
                border_width,
                border_width,
                self.width - 2 * border_width,
                self.height - 2 * border_width,
                color=border_color,
                border_width=border_width)

        # render text
        if self.text:
            start_x = self.width // 2
            start_y = self.height // 2

            text_margin = 2
            arcade.draw_text(
                text=self.text,
                start_x=start_x,
                start_y=start_y,
                font_name=font_name,
                font_size=font_size,
                color=font_color,
                align="center",
                anchor_x='center', anchor_y='center',
                width=self.width - 2 * border_width - 2 * text_margin
            )

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        text = value
        self._text = value
        self.trigger_render()



    def set_text(self, text, Alphabet_Textures):
        self.text_sprites.clear()
        #self.text_scale = 1
        if not text:
            return 
        words = text.split(" ")
        pos_x = -45+self.text_offset_x
        pos_y = 5+self.text_offset_y

        if len(text)*self.text_scale*self.text_margin > self.width:
            pos_y += 10
        line_num_of_characters = 0
        for word in words:
            spaces = len(word)
            spaces *= self.text_margin
            if pos_x+len(word)*self.text_scale*14+self.text_margin > self.width-30:
                pos_x = -45+self.text_offset_x
                pos_y -= 24

            
            for character in word:
                #self.offset_y+pos_y
                sprite = arcade.Sprite(center_x=self.offset_x+pos_x, center_y=-self.offset_y/2+pos_y, scale=self.text_scale)
                sprite.texture = Alphabet_Textures[character]
                self.text_sprites.append(sprite)
                pos_x += self.text_margin
            pos_x += self.text_margin
            line_num_of_characters = len(word)
            
        return
        if self.text:
            pos_x = -45+self.text_offset_x
            pos_y = 5+self.text_offset_y
            if len(text)*self.text_scale*self.text_margin > self.width:
                pos_y += 10
            for string in text:
                #self.offset_y+pos_y
                sprite = arcade.Sprite(center_x=self.offset_x+pos_x, center_y=-self.offset_y/2+pos_y, scale=self.text_scale)
                sprite.texture = Alphabet_Textures[string]
                self.text_sprites.append(sprite)
                pos_x += self.text_margin
                if pos_x*self.text_scale > self.width-90:
                    pos_x = -45+self.text_offset_x
                    pos_y -= 24