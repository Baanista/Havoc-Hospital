import arcade
from Components import *
from GameView import *

class StartMenu(arcade.View):
    """
    First Menu that loads in. Customize things outside of the world.
    """
    def __init__(self):
        super().__init__()
        self.uimanager = arcade.gui.UIManager()
        self.uimanager.enable()

        self.text = arcade.create_text_sprite("Havoc Hospital", 200, 600, arcade.csscolor.DARK_RED, font_name="creepster", font_size=128)

        textures = arcade.load_spritesheet("resources/gui/Wooden Font.png", 14, 24, 12, 70, margin=1)
        self.Alphabet_Textures = {" ":None}
        string = "ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890abcdefghijklmnopqrstuvwxyz.:,%/-+_"
        for i in range(len(string)):
            self.Alphabet_Textures[string[i]] = textures[i]


        main_button = CustomUIFlatButton(self.Alphabet_Textures, click_sound = None, text="Start", width=140, height=50, x=0, y=0, text_offset_x = 16, text_offset_y=35, offset_x=75, offset_y=25)
        main_button.on_click = self.Start
        wrapper = arcade.gui.UIAnchorWidget(anchor_x="right", anchor_y="top",
                child=main_button, align_x=-600, align_y=-500)
        main_button.wrapper = wrapper
        self.uimanager.add(wrapper)
    def on_draw(self):
        arcade.start_render()
        self.text.draw()
        self.uimanager.draw()
    def Start(self, event):
        game = MyGame(self, 1440, 800, "Havoc Hospital")
        self.uimanager.disable()
        window = arcade.get_window()
        window.show_view(game)


def main():
    """ Main function """
    window = arcade.Window(width=1440, height=900, title="Havoc Hospital")
    game = StartMenu()
    window.show_view(game)
    arcade.run()

if __name__ == "__main__":
    main()