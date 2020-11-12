import arcade
import arcade.gui
import configparser

import GAME

class Button(arcade.gui.UIImageButton):
    def __init__(self, function ,x=0, y=0, normal_texture=None,
            hover_texture=None, press_texture=None, text="Button"):
        super().__init__(center_x=x,
            center_y=y,
            normal_texture=normal_texture,
            hover_texture=hover_texture,
            press_texture=press_texture,
            text=text)
        self.function = function

    def on_press(self):
        self.function()

    def on_release(self):
        pass

class MainMenu(arcade.View):
    def __init__(self, config):
        super().__init__()
        
        self.ui_manager = arcade.gui.UIManager()

        self.config = config

    def setup(self):
        normal = arcade.texture.load_texture(
            "resources/ui/buttons/menu/normal.png"
            )
        hover = arcade.texture.load_texture(
            "resources/ui/buttons/menu/hover.png"
            )
        press = arcade.texture.load_texture(
            "resources/ui/buttons/menu/clicked.png"
            )
        center_x = int(self.window.width/2)
        center_y = int(self.window.height/2)
        x = center_x
        y = center_y
        button = Button(
            self.play,
            x=x,
            y=y,
            normal_texture=normal,
            hover_texture=hover,
            press_texture=press,
            text='Play'
        )
        self.ui_manager.add_ui_element(button)

    def on_show(self):
        self.setup()
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        arcade.start_render()

    def play(self):
        game = GAME.Game(self.config)
        self.window.show_view(game)

    def on_hide_view(self):
        self.ui_manager.unregister_handlers()
        self.ui_manager.purge_ui_elements()

def main():
    config = configparser.ConfigParser()
    config.read("settings.ini")
    width = int(config["init"]["width"])
    height = int(config["init"]["height"])
    title = config["init"]["title"]
    window = arcade.Window(width=width, height=height,
                           title=title)
    view = MainMenu(config)
    window.show_view(view)
    arcade.run()

if __name__ == "__main__":
    main()
    
