import pygame as pg
import math
from settings import *
import os
from collections import deque


class SpriteObject:
    """
    Base class SpriteObject.

    """
    def __init__(self, game, path='resources/sprites/static_sprites/candlebra.png',
                 pos=(10.5, 3.5), scale=0.7, shift=0.27, pick=False, type=None, gone=False):
        """
        Init method of class SpriteObject

        :param game: Instance of Game class
        :type game: object
        :param path: Path to the sprite images
        :type path: str
        :param pos: Position of the sprite image
        :type pos: tuple
        :param scale: Scale of the sprite
        :type scale: float
        :param shift: Shifting of the sprite
        :type shift: float
        :param pick: Can the sprite be picked
        :type pick: bool
        :param type: What is the loot type of the sprite
        :type type: str
        :param gone: Is the sprite death or alive
        :type gone: bool
        """

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
        """
        Function for getting the sprite projection.

        More info in section Explanation in docs

        :return: Bone
        :rtype: None
        """

        projection = SCREEN_DIST / self.norm_dist * self.SPRITE_SCALE
        projection_width, projection_height = projection * self.IMAGE_RATIO, projection

        image = pg.transform.scale(self.image, (projection_width, projection_height))

        self.sprite_half_width = projection_width // 2
        height_shift = projection_height * self.SPRITE_HEIGHT_SHIFT
        pos = self.screen_x - self.sprite_half_width, self.game.player.half_height - projection_height // 2 + height_shift

        self.game.raycasting.objects_to_render.append((self.norm_dist, image, pos))

    def pick_object(self):
        """
        Pick object function.

        Function that checks if the sprites is picked if it can be picked
        and safeguard maximum quantity of each item

        :return: None
        :rtype: None
        """

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
        """
        Function for getting the sprite to player.

        More information section Explanation in docs

        :return: None
        :rtype: None
        """

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
        """
        Updating function

        :return: None
        :rtype: None
        """

        self.get_sprite()
        self.pick_object()


class AnimatedSprite(SpriteObject):
    """
    AnimatedSprite class
    """
    def __init__(self, game, path='resources/sprites/animated_sprites/green_light/0.png',
                 pos=(11.5, 3.5), scale=0.8, shift=0.16, animation_time=120, gone=False):
        """
        Init method of animated spirtes.

        :param game: Instance of Game class
        :type game: object
        :param path: Path to the sprite images
        :type path: str
        :param pos: Position of the spite
        :type pos: tuple
        :param scale: Scale of the sprite
        :type scale: float
        :param shift: Shift of the sprite image
        :type shift: float
        :param animation_time: Animation time of the sprite
        :type animation_time: int
        :param gone: Check if alive
        :type gone: bool
        """

        super().__init__(game, path, pos, scale, shift)
        self.animation_time = animation_time
        self.path = path.rsplit('/', 1)[0]
        self.images = self.get_images(self.path)
        self.animation_time_prev = pg.time.get_ticks()
        self.animation_trigger = False
        self.gone = gone

    def update(self):
        """
        Updating function

        :return: None
        :rtype: None
        """

        super().update()
        self.check_animation_time()
        self.animate(self.images)

    def animate(self, images):
        """
        Function that animates the sprite

        :param images: Sprite images
        :type images: pygame.images
        :return: None
        :rtype: None
        """

        if self.animation_trigger:
            images.rotate(-1)
            self.image = images[0]

    def check_animation_time(self):
        """
        Function for checking animation time

        :return: None
        :rtype: None
        """

        self.animation_trigger = False
        time_now = pg.time.get_ticks()
        if time_now - self.animation_time_prev > self.animation_time:
            self.animation_time_prev = time_now
            self.animation_trigger = True

    def get_images(self, path):
        """
        Function for getting the sprite images.

        :param path: Path to the image folder
        :type path: str
        :return: image list
        :rtype: list
        """

        images = deque()
        for file_name in os.listdir(path):
            if os.path.isfile(os.path.join(path, file_name)):
                img = pg.image.load(path + '/' + file_name).convert_alpha()
                images.append(img)
        return images

    @property
    def map_pos(self):
        """
        Properyty method of the class

        :return: Position of the sprite
        :rtype: int
        """

        return int(self.x), int(self.y)
