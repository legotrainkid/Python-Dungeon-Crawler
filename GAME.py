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
        self.all_sprites = arcade.SpriteList()
        self.walls = arcade.SpriteList(use_spatial_hash=True)
        self.tiles = arcade.SpriteList(use_spatial_hash=True)
        self.enemies = arcade.SpriteList()
        self.arrows = arcade.SpriteList()
        self.tiles_list = arcade.SpriteList(use_spatial_hash=True)
        self.player = None

    def setup(self):
        self.paused = False
        self.MOVE_SPEED = int(self.config["game"]["speed"])
        self.MAPSIZE = int(self.config["game"]["map_size"])
        self.FPS = int(self.config["game"]["fps"])
        self.NUM_ENEMIES = int(self.config["game"]["num_of_enemies"])
        self.PLAYER_DAMAGE = int(self.config["game"]["player_damage"])
        self.ARROW_SPEED = int(self.config["game"]["arrow_speed"])
        self.ARROW_DAMAGE = int(self.config["game"]["arrow_damage"])
        self.SCREENSIZE = [int(self.config["init"]["width"]),
                               int(self.config["init"]["height"])]

        self.items = DATA.load_items()

        #self.player = arcade.AnimatedTimeBasedSprite()

        #Initialize map generator
        dg = GENERATION.Generator(width=self.MAPSIZE, height=self.MAPSIZE)

        #Generate level
        dg.gen_level()

        #Get world map
        self.world_map = dg.return_tiles()

        self.TILES = {}
        load_tiles = ["empty", "floor", "wall"]
        for tile in load_tiles:
            self.TILES[tile] = arcade.texture.load_texture("resources/graphics/world/"+tile+".png")

        self.all_sprites = arcade.SpriteList()
        self.walls = arcade.SpriteList(use_spatial_hash=True)
        self.tiles = arcade.SpriteList(use_spatial_hash=True)
        self.enemies = arcade.SpriteList()
        self.arrows = arcade.SpriteList()
        self.tiles_list = arcade.SpriteList(use_spatial_hash=True)

        y_v = 0
        x_v = 0
        i = 0
        #Loop trough every tile in map
        for y in range(len(self.world_map)):
            for x in self.world_map[y]:
                #Create tile sprite
                if x == 0:
                    new = ENTITIES.Tile(
                        self.TILES["empty"], x_v, y_v,
                        True, [i, y], self.SCREENSIZE)
                elif x == 1:
                    new = ENTITIES.Tile(
                        self.TILES["wall"], x_v, y_v,
                        True, [i, y], self.SCREENSIZE)
                    self.walls.append(new)
                elif x == 2:
                    new = ENTITIES.Tile(
                        self.TILES["floor"], x_v, y_v,
                        False, [i, y], self.SCREENSIZE)
                x_v += 50
                #add tile to sprite groups
                self.tiles_list.append(new)
                self.all_sprites.append(new)
                i+=1
            y_v += 50
            x_v = 0
            i = 0

        self.player = ENTITIES.Player(30, 500, self.PLAYER_DAMAGE, self.SCREENSIZE)

        self.spawn_enemies(self.NUM_ENEMIES)
        self.all_sprites.append(self.player)

    def on_show(self):
        self.setup()

    def on_draw(self):
        arcade.start_render()
        arcade.set_background_color(arcade.color.BLACK)
        self.tiles_list.draw()
        self.player.draw()

    def on_update(self, delta_time):
        if self.paused:
            return
        self.all_sprites.update()

    def spawn_enemies(self, num):
        for i in range(num):
            pos = self.spawn_ent()
            enemy = ENTITIES.Enemy(pos, i, self.SCREENSIZE)
            self.all_sprites.append(enemy)
            self.enemies.append(enemy)

    def spawn_ent(self):
        tiles = self.spawnable_tiles()
        spawned = False
        while not spawned:
            tile = random.choice(tiles)
            pos = self.tile_pos(tile)
            spawned = True
        return pos

    def spawnable_tiles(self):
        spawnable = []
        for y in range(len(self.world_map)):
            for x in range(len(self.world_map[y])):
                if self.world_map[y][x] == 2:
                    spawnable.append([x, y])
        return spawnable

    def tile_pos(self, tile):
        pos_x = tile[0] * 50
        pos_y = tile[1] * 50
        return [pos_x, pos_y]
