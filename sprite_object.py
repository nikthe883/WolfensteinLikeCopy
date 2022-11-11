import pygame as pg
import math
from settings import *
import os
from collections import deque


class SpriteObject:
    def __init__(self, game, path='resources/sprites/static_sprites/candlebra.png',
                 pos=(10.5, 3.5), scale=0.7, shift=0.27, pick=False, type=None, gone=False):
        self.game = game
        self.player = game.player
        self.x, self.y = pos
        self.pick = pick
        self.picked = False
        self.gone = gone
        self.loot_type = type
        self.image = pg.image.load(path).convert_alpha()
        self.IMAGE_WIDTH = self.image.get_width()
        self.IMAGE_HALF_WIDTH = self.image.get_width() // 2
        self.IMAGE_RATIO = self.IMAGE_WIDTH / self.image.get_height()
        self.dx, self.dy, self.theta, self.screen_x, self.dist, self.norm_dist = 0, 0, 0, 0, 1, 1
        self.sprite_half_width = 0
        self.SPRITE_SCALE = scale
        self.SPRITE_HEIGHT_SHIFT = shift
        self.loot_type_list = ["armor", "minigun_ammo", "shotgun_ammo", "chainsaw_ammo", "health"]

    def get_sprite_projection(self):
        """Getting the sprite projection. More in docs"""
        projection = SCREEN_DIST / self.norm_dist * self.SPRITE_SCALE
        projection_width, projection_height = projection * self.IMAGE_RATIO, projection

        image = pg.transform.scale(self.image, (projection_width, projection_height))

        self.sprite_half_width = projection_width // 2
        height_shift = projection_height * self.SPRITE_HEIGHT_SHIFT
        pos = self.screen_x - self.sprite_half_width, self.game.player.half_height - projection_height // 2 + height_shift

        self.game.raycasting.objects_to_render.append((self.norm_dist, image, pos))

    def pick_object(self):
        """Function that checks if the sprites is picked if it can be picked
        and safeguard maximum quantity of each item"""
        if self.pick:
            if math.isclose(self.game.player.pos[0], self.x, rel_tol=0.05) and math.isclose(self.game.player.pos[1], self.y, rel_tol=0.05):
                self.picked = True
                if self.loot_type == "armor":
                    if self.game.player.armor < PLAYER_MAX_ARMOR:
                        self.game.player.armor += 20

                if self.loot_type == "health":
                    if self.game.player.health < PLAYER_MAX_HEALTH:
                        self.game.player.health += 30

                if self.loot_type == "minigun_ammo":
                    if self.game.player.minigun_ammo < PLAYER_MAX_MINIGUN_AMMO:
                        self.game.player.minigun_ammo += 40

                if self.loot_type == "shotgun_ammo":
                    if self.game.player.shotgun_ammo < PLAYER_MAX_SHOTGUN_AMMO:
                        self.game.player.shotgun_ammo += 20

                if self.loot_type == "chainsaw_ammo":
                    if self.game.player.vruum_vruum_fuel < PLAYER_MAX_CHAINSAW_FUEL:
                        self.game.player.vruum_vruum_fuel += 40

    def get_sprite(self):
        dx = self.x - self.player.x
        dy = self.y - self.player.y
        self.dx, self.dy = dx, dy
        self.theta = math.atan2(dy, dx)

        delta = self.theta - self.player.angle
        if (dx > 0 and self.player.angle > math.pi) or (dx < 0 and dy < 0):
            delta += math.tau

        delta_rays = delta / DELTA_ANGLE
        self.screen_x = (HALF_NUM_RAYS + delta_rays) * SCALE

        self.dist = math.hypot(dx, dy)
        self.norm_dist = self.dist * math.cos(delta)
        if -self.IMAGE_HALF_WIDTH < self.screen_x < (WIDTH + self.IMAGE_HALF_WIDTH) and self.norm_dist > 0.5:
            self.get_sprite_projection()

    def update(self):
        self.get_sprite()
        self.pick_object()


class AnimatedSprite(SpriteObject):
    def __init__(self, game, path='resources/sprites/animated_sprites/green_light/0.png',
                 pos=(11.5, 3.5), scale=0.8, shift=0.16, animation_time=120, gone=False):
        super().__init__(game, path, pos, scale, shift)
        self.animation_time = animation_time
        self.path = path.rsplit('/', 1)[0]
        self.images = self.get_images(self.path)
        self.animation_time_prev = pg.time.get_ticks()
        self.animation_trigger = False
        self.gone = gone

    def update(self):
        super().update()
        self.check_animation_time()
        self.animate(self.images)

    def animate(self, images):
        if self.animation_trigger:
            images.rotate(-1)
            self.image = images[0]

    def check_animation_time(self):
        self.animation_trigger = False
        time_now = pg.time.get_ticks()
        if time_now - self.animation_time_prev > self.animation_time:
            self.animation_time_prev = time_now
            self.animation_trigger = True

    def get_images(self, path):
        images = deque()
        for file_name in os.listdir(path):
            if os.path.isfile(os.path.join(path, file_name)):
                img = pg.image.load(path + '/' + file_name).convert_alpha()
                images.append(img)
        return images

    @property
    def map_pos(self):
        return int(self.x), int(self.y)
