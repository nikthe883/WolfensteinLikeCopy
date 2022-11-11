import pygame as pg
from settings import *
import numpy as np


class RayCasting:
    def __init__(self, game):
        self.game = game
        self.objects_to_render = []
        self.textures = self.game.object_renderer.wall_textures
        self.depth = 0
        self.show_raycast = False
        self.ray_casting_result = []

    def update(self):
        self.ray_cast()
        self.get_objects_to_render()

    def get_objects_to_render(self):
        self.objects_to_render = []

        for ray, values in enumerate(self.ray_casting_result):
            depth, projection_height, texture, offset = values

            wall_column = self.textures[texture].subsurface(
                offset * (TEXTURE_SIZE - SCALE), 0, SCALE, TEXTURE_SIZE

            )
            wall_column = pg.transform.scale(wall_column, (SCALE, projection_height))
            wall_position = (ray * SCALE, self.game.player.half_height - projection_height // 2)
            self.objects_to_render.append((depth, wall_column, wall_position))

    def ray_cast(self):
        self.ray_casting_result = []
        texture_vertical, texture_horizontal = 1, 1
        self.ox, self.oy = self.game.player.pos
        x_map, y_map = self.game.player.map_pos

        ray_angle = self.game.player.angle - HALF_FOV + 0.0001
        for ray in range(NUM_RAYS):
            self.sin_a = np.sin(ray_angle)
            self.cos_a = np.cos(ray_angle)

            # horizontals
            y_horizontal, dy = (y_map + 1, 1) if self.sin_a > 0 else (y_map - 1e-6, -1)

            depth_horizontal = (y_horizontal - self.oy) / self.sin_a
            x_horizontal = self.ox + depth_horizontal * self.cos_a

            delta_depth = dy / self.sin_a
            dx = delta_depth * self.cos_a

            for i in range(MAX_DEPTH):
                tile_horizontal = int(x_horizontal), int(y_horizontal)
                if tile_horizontal in self.game.map.world_map:
                    texture_horizontal = self.game.map.world_map[tile_horizontal]
                    break
                x_horizontal += dx
                y_horizontal += dy
                depth_horizontal += delta_depth

            # verticals
            x_vertical, dx = (x_map + 1, 1) if self.cos_a > 0 else (x_map - 1e-6, -1)

            depth_vertical = (x_vertical - self.ox) / self.cos_a
            y_vertical = self.oy + depth_vertical * self.sin_a

            delta_depth = dx / self.cos_a
            dy = delta_depth * self.sin_a

            for i in range(MAX_DEPTH):
                tile_vertical = int(x_vertical), int(y_vertical)
                if tile_vertical in self.game.map.world_map:
                    texture_vertical = self.game.map.world_map[tile_vertical]
                    break
                x_vertical += dx
                y_vertical += dy
                depth_vertical += delta_depth

            # depth, texture offset
            if depth_vertical < depth_horizontal:
                depth, texture = depth_vertical, texture_vertical
                y_vertical %= 1
                offset = y_vertical if self.cos_a > 0 else (1 - y_vertical)
            else:
                depth, texture = depth_horizontal, texture_horizontal
                x_horizontal %= 1
                offset = (1 - x_horizontal) if self.sin_a > 0 else x_horizontal

            # remove fishbowl effect
            depth *= math.cos(self.game.player.angle - ray_angle)

            # projection
            projection_height = SCREEN_DIST / (depth + 0.0001)

            # ray casting result
            self.ray_casting_result.append((depth, projection_height, texture, offset))

            # drawing the cast on the minimap
            if self.show_raycast:
                pg.draw.line(self.game.sc_map, 'yellow', (MINIMAP_TILE_SIZE * self.ox, MINIMAP_TILE_SIZE * self.oy),
                             (MINIMAP_TILE_SIZE * self.ox + MINIMAP_TILE_SIZE * depth * self.cos_a, MINIMAP_TILE_SIZE * self.oy + MINIMAP_TILE_SIZE * depth * self.sin_a), 2)

            ray_angle += DELTA_ANGLE
