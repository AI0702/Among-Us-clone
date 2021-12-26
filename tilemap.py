import pygame as pg
from settings import *
import pytmx


class Map:
    def __init__(self, filename):
        self.data = []
        with open(filename, 'rt') as f:
            for line in f:
                self.data.append(line.strip())

        self.tilewidth = len(self.data[0])
        self.tileheight = len(self.data)
        self.width = self.tilewidth * TILESIZE
        self.height = self.tileheight * TILESIZE


class TiledMap:
    def __init__(self, filename):
        tm = pytmx.load_pygame(filename, pixelalpha=True)
        self.width = tm.width * tm.tilewidth
        self.height = tm.height * tm.tileheight
        self.tmxdata = tm

    def render(self, surface):
        # tile data
        ti = self.tmxdata.get_tile_image_by_gid
        # For each layer look for each tile and draw on surface
        for layer in self.tmxdata.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid, in layer:
                    tile = ti(gid)
                    if tile:
                        surface.blit(tile, (x * self.tmxdata.tilewidth,
                                            y * self.tmxdata.tileheight))
    def make_map(self):
        temp_surface = pg.Surface((self.width, self.height))
        self.render(temp_surface)
        return temp_surface


class Camera:
    def __init__(self, width, height):
        self.camera = pg.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        # Move rectangle according to camera coordinates are
        return entity.rect.move(self.camera.topleft)

    def apply_rect(self, rect):
        return rect.move(self.camera.topleft)

    def update(self, player_sprite):
        # center player sprite on screen
        x = -player_sprite.rect.x + int(WIDTH / 2)
        y = -player_sprite.rect.y + int(HEIGHT / 2)

        # Limit the map scrolling when sprite reaches end point of map
        # For left boundary
        x = min(0, x)
        # For right boundary
        x = max(-(self.width - WIDTH), x)
        # For top boundary
        y = min(0, y)  # checks if y < 0
        # For bottom boundary
        y = max(-(self.height - HEIGHT), y)

        # Adjust camera rectangle
        self.camera = pg.Rect(x, y, self.width, self.height)
