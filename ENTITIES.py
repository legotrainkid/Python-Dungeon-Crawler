import arcade

class Tile(arcade.Sprite):
    def __init__(self, texture, x, y, is_barrier, pos, SCREENSIZE):
        super().__init__()

        self.texture = texture
        
        self.x = x
        self.y = y
        
        self.is_barrier = is_barrier
        
        self.pos = pos
        
        self.SCREENSIZE = SCREENSIZE


class Player(arcade.Sprite):
    def __init__(self, health, stamina, damage, SCREENSIZE):
        super().__init__()

        self.texture = arcade.texture.load_texture("resources/graphics/characters/Player/player.png")

        self.center_x = int(SCREENSIZE[0]/2-17.5)
        self.center_y = int(SCREENSIZE[1]/2-17.5)
        self.pos = []

        self.MAX_HEALTH = health
        self.health = health

        self.sprint = False
        self.stamina = stamina
        self.MAX_STAMINA = stamina

        self.NORMAL_DMG = damage
        self.damage = damage

        self.update_frames = 0

    def update(self):
        if self.stamina < 1:
            self.sprint = False
            self.stamina = 0
        if self.sprint:
            if not self.update_frames:
                self.stamina -= 1
                self.update_frames = 1
            else:
                self.update_frames-=1
        elif not self.sprint:
            if not self.update_frames:
                if self.stamina < self.MAX_STAMINA:
                    self.stamina +=1
                    self.update_frames = 5
            else:
                self.update_frames-=1
        if self.update_frames < 0:
            self.update_frames = 0

class Enemy(arcade.Sprite):
    def __init__(self, pos, frame, SCREENSIZE):
        super().__init__()
