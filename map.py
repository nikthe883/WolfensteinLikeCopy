import pygame as pg
from settings import *
from random_map_generation import *
from random_map_generation import generate_best_level


class Map:
    def __init__(self, game):
        print("Here")
        self.game = game
        self.load_minimap()
        self.world_map = {}
        self.get_map()

        self.rows = len(self.mini_map)
        self.cols = len(self.mini_map[0])


    def get_map(self):
        for j, row in enumerate(self.mini_map):
            for i, value in enumerate(row):
                if value:
                    self.world_map[i, j] = value

    def load_minimap(self):
        if self.game.load.load_game:
            self.mini_map = self.game.load.loaded_data['map']
        else:
            self.mini_map = generate_best_level(50)

    def draw(self):
        """"Drawing the minimap with set squares og 13 x 13"""
        [pg.draw.rect(self.game.sc_map, 'darkgrey', (pos[0] * MINIMAP_TILE_SIZE, pos[1] * MINIMAP_TILE_SIZE, MINIMAP_TILE_SIZE, MINIMAP_TILE_SIZE), 1) for pos in self.world_map]
