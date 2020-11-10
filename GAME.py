import arcade
import arcade.gui
import random

import GENERATION
import DATA

import ENTITIES

class Game(arcade.View):
    def __init__(self, config):
        super().__init__()
        
        self.config = config

        self.MOVE_SPEED = None
        self.MAPSIZE = None
        self.FPS = None
        self.NUM_ENEMIES = None
        self.PLAYER_DAMAGE = None
        self.ARROW_SPEED = None
        self.ARROW_DAMAGE = None
        self.paused = False
        self.physics_engine = None

    def setup(self):
        self.paused = False
        self.MOVE_SPEED = int(self.config["game"]["speed"])
        self.MAPSIZE = int(self.config["game"]["map_size"])
        self.FPS = int(self.config["game"]["fps"])
        self.NUM_ENEMIES = int(self.config["game"]["num_of_enemies"])
        self.PLAYER_DAMAGE = int(self.config["game"]["player_damage"])
        self.ARROW_SPEED = int(self.config["game"]["arrow_speed"])
        self.ARROW_DAMAGE = int(self.config["game"]["arrow_damage"])

        self.items = DATA.load_items()

        #self.player = arcade.AnimatedTimeBasedSprite()

        #Initialize map generator
        dg = GENERATION.Generator(width=self.MAPSIZE, height=self.MAPSIZE)

        #Generate level
        dg.gen_level()

        #Get world map
        self.world_map = dg.return_tiles()

    def on_show_view(self):
        self.setup()
        arcade.set_background_color(arcade.color.WHITE)

    def on_draw(self):
        arcade.start_render()

    def on_update(self, delta_time):
        if self.paused:
            return

               
