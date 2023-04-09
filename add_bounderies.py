"""
Starting Template

Once you have learned how to use classes, you can begin your program with this
template.

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.starting_template
"""
import arcade

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Starting Template"

import json

# Read Existing JSON File



class MyGame(arcade.Window):
    """
    Main application class.

    NOTE: Go ahead and delete the methods you don't need.
    If you do need a method, delete the 'pass' and replace it
    with your own code. Don't leave 'pass' in this program.
    """

    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        arcade.set_background_color(arcade.color.AMAZON)
        self.hospatial = arcade.Sprite(filename="map.png", center_x=160, center_y=160, scale=.5)
        # If you have sprite lists, you should create them here,
        # and set them to None

        #27x32

        self.mapper = []
        for x in range(20):
            self.mapper.append([])
            for y in range(20):
                self.mapper[x].append(0)


    def setup(self):
        """ Set up the game variables. Call to re-start the game. """
        # Create your sprites and sprite lists here
        pass

    def on_draw(self):
        """
        Render the screen.
        """

        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        self.clear()
        self.hospatial.draw()

        for x in range(len(self.mapper)):
            for y in range(len(self.mapper[0])):
                if self.mapper[x][y] == 1:
                    arcade.draw_rectangle_filled(x*16 + 8,y*16 + 8, 16, 16, (255, 0, 0))


        # Call draw() on all your sprite lists below

    def on_update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """
        print(self.mapper)

        data = {
            "name": self.mapper
        }

        # File name to save data
        filename = "boundermap.json"

        # Write data to file
        with open(filename, "w") as file:
            json.dump(data, file)

    def on_key_press(self, key, key_modifiers):
        """
        Called whenever a key on the keyboard is pressed.

        For a full list of keys, see:
        https://api.arcade.academy/en/latest/arcade.key.html
        """
        pass

    def on_key_release(self, key, key_modifiers):
        """
        Called whenever the user lets off a previously pressed key.
        """
        pass

    def on_mouse_motion(self, x, y, delta_x, delta_y):
        """
        Called whenever the mouse moves.
        """
        pass

    def on_mouse_press(self, x, y, button, key_modifiers):
        """
        Called when the user presses a mouse button.
        """
        if self.mapper[round((x)/16 -.5)][round(y/16 -.5)] == 0:
            self.mapper[round((x)/16 -.5)][round(y/16 -.5)] = 1
        elif self.mapper[round((x)/16 -.5)][round(y/16 -.5)] == 1:
            self.mapper[round((x)/16 -.5)][round(y/16 -.5)] = 0

    def on_mouse_release(self, x, y, button, key_modifiers):
        """
        Called when a user releases a mouse button.
        """
        pass


def main():
    """ Main function """
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()