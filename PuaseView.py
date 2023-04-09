import arcade

class PuaseMenu(arcade.View):
    def __init__(self, game):
        self.game_view = game
        self.window = arcade.get_window()
        super().__init__(self.window)
        self.uimanager = arcade.gui.UIManager()
        self.uimanager.enable()
        self.Background = arcade.Sprite("resources/gui/Christmas_menu_Background.png", center_x=self.window.width/2, center_y=self.window.height/2, scale = 10)
    def on_draw(self):
        self.Background.draw()