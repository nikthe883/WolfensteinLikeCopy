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
        # self.ray_casting_result = self.ray_cast(self.game.player.pos, self.game.player.map_pos, self.game.player.angle, self.game.map.world_map , self.game.sc_map)

        for ray, values in enumerate(self.ray_casting_result):
            depth, proj_height, texture, offset = values

            wall_column = self.textures[texture].subsurface(
                offset * (TEXTURE_SIZE - SCALE), 0, SCALE, TEXTURE_SIZE

            )
            wall_column = pg.transform.scale(wall_column, (SCALE, proj_height))
            wall_pos = (ray * SCALE, self.game.player.half_height - proj_height // 2)
            self.objects_to_render.append((depth, wall_column, wall_pos))

    def ray_cast(self):
        self.ray_casting_result = []
        texture_vert, texture_hor = 1, 1
        self.ox, self.oy = self.game.player.pos
        x_map, y_map = self.game.player.map_pos

        ray_angle = self.game.player.angle - HALF_FOV + 0.0001
        for ray in range(NUM_RAYS):
            self.sin_a = np.sin(ray_angle)
            self.cos_a = np.cos(ray_angle)

            # horizontals
            y_hor, dy = (y_map + 1, 1) if self.sin_a > 0 else (y_map - 1e-6, -1)

            depth_hor = (y_hor - self.oy) / self.sin_a
            x_hor = self.ox + depth_hor * self.cos_a

            delta_depth = dy / self.sin_a
            dx = delta_depth * self.cos_a

            for i in range(MAX_DEPTH):
                tile_hor = int(x_hor), int(y_hor)
                if tile_hor in self.game.map.world_map:
                    texture_hor = self.game.map.world_map[tile_hor]
                    break
                x_hor += dx
                y_hor += dy
                depth_hor += delta_depth

            # verticals
            x_vert, dx = (x_map + 1, 1) if self.cos_a > 0 else (x_map - 1e-6, -1)

            depth_vert = (x_vert - self.ox) / self.cos_a
            y_vert = self.oy + depth_vert * self.sin_a

            delta_depth = dx / self.cos_a
            dy = delta_depth * self.sin_a

            for i in range(MAX_DEPTH):
                tile_vert = int(x_vert), int(y_vert)
                if tile_vert in self.game.map.world_map:
                    texture_vert = self.game.map.world_map[tile_vert]
                    break
                x_vert += dx
                y_vert += dy
                depth_vert += delta_depth

            # depth, texture offset
            if depth_vert < depth_hor:
                depth, texture = depth_vert, texture_vert
                y_vert %= 1
                offset = y_vert if self.cos_a > 0 else (1 - y_vert)
            else:
                depth, texture = depth_hor, texture_hor
                x_hor %= 1
                offset = (1 - x_hor) if self.sin_a > 0 else x_hor

            # remove fishbowl effect
            depth *= math.cos(self.game.player.angle - ray_angle)

            # projection
            proj_height = SCREEN_DIST / (depth + 0.0001)

            # ray casting result
            self.ray_casting_result.append((depth, proj_height, texture, offset))


            # drawing the cast on the minimap
            if self.show_raycast:
                pg.draw.line(self.game.sc_map, 'yellow', (MINIMAP_TILE_SIZE * self.ox, MINIMAP_TILE_SIZE * self.oy),
                             (MINIMAP_TILE_SIZE * self.ox + MINIMAP_TILE_SIZE * depth * self.cos_a, MINIMAP_TILE_SIZE * self.oy + MINIMAP_TILE_SIZE * depth * self.sin_a), 2)

            ray_angle += DELTA_ANGLE