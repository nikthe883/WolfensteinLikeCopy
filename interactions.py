from settings import *
from sprite_object import *
from random import random, choice
import numpy as np


class ObjectInteraction(AnimatedSprite):
    """
    Class object interactions.

    This clss is responsible for the loot drop objects - barrels
    """
    def __init__(self, game, path='resources/sprites/interactables/barrel/0.png', pos=(10.5, 5.5),
                 scale=0.5, shift=0.5, gone=False):
        """
        Init method of ObjectInteraction class

        :param game: instance of Game class
        :type game: object
        :param path: path to images
        :type path: str
        :param pos: position of the barrel
        :type pos: tuple
        :param scale: scaling the image
        :type scale: float
        :param shift: shifting the image
        :type shift: float
        :param gone: checks if destroyed
        :type gone: bool
        """

        super().__init__(game, path, pos, scale, shift, gone)

        self.idle_images = self.get_images(self.path + '/anim')
        self.death_images = self.get_images(self.path + '/death')
        self.pos = pos
        self.size = 20
        self.gone = gone
        self.drop_loop = True
        self.alive = True
        self.ray_cast_value = False  # for shooting
        self.frame_counter = 0
        self.game = game

    def update(self):
        """
        Update method.

        :return: None
        :rtype: None
        """

        self.check_animation_time()
        self.get_sprite()
        self.logic()

    def logic(self):
        """
        Function that deals with the logic of the barrel

        :return: None
        :rtype: None
        """

        self.ray_cast_value = ray_cast_player_npc(self.game.player.pos, self.game.player.map_pos, self.map_pos, self.game.map.world_map, self.theta)
        self.check_if_hit()
        if self.alive:
            self.animate_idle()
        else:
            self.animate_death()
            self.loop_drop()
            self.gone = True

    def loop_drop(self):
        """
        Function that deals with loot drop logic

        :return: None
        :rtype: None
        """

        if not self.alive and self.drop_loop:
            loot_choice = choice(self.game.sprite_object.loot_type_list)
            self.game.object_handler.add_pick_sprites(SpriteObject(self.game, path=f'resources/sprites/collectables/{loot_choice}.png',
                                                                   pos=(self.map_pos[0] + 0.5, self.map_pos[1] + 0.5), scale=0.3, pick=True, type=loot_choice))
            self.drop_loop = False

    def animate_death(self):
        """
        Function that animates destruction of the barrel

        :return: None
        :rtype: None
        """

        if not self.alive:
            if self.game.global_trigger and self.frame_counter < len(self.death_images) - 1:
                self.death_images.rotate(-1)
                self.image = self.death_images[0]
                self.frame_counter += 1

    def animate_idle(self):
        """
        Function that animates idle of the barrel

        :return: None
        :rtype: None
        """

        if self.alive:
            self.animate(self.idle_images)

    def check_if_hit(self):
        """
        Function that checks if the object is hit or not.

        :return: None
        :rtype: None
        """

        height_shoot = math.isclose(self.player.half_height, HALF_HEIGHT, rel_tol=0.7)
        if self.game.player.shot and self.alive and self.ray_cast_value:
            # for shotgun
            check = HALF_WIDTH - self.sprite_half_width < self.screen_x < HALF_WIDTH + self.sprite_half_width and height_shoot
            if self.player.weapon_selected == "shotgun":
                if check:
                    self.game.player.shot = False
                    self.alive = False
                    self.game.sound.barrel_exploding.play()

            # for chainsaw
            if self.player.weapon_selected == "chainsaw":
                close_range = np.isclose(self.player.pos[1], self.map_pos[1], atol=1.6), np.isclose(self.player.pos[0], self.map_pos[0], atol=1.6)
                if check and close_range[0] and close_range[1] and self.game.weapon.vroom_vroom:
                    self.game.player.shot = True
                    self.alive = False
                    self.game.sound.barrel_exploding.play()

            if self.player.weapon_selected == "minigun":
                if check:
                    self.game.player.shot = True
                    self.alive = False
                    self.game.sound.barrel_exploding.play()

    @property
    def map_pos(self):
        """
        property method for objects position.

        :return: barrels position
        :rtype: int
        """

        return int(self.x), int(self.y)


def ray_cast_player_npc(player_position, player_map_position, self_map_position, game_map, theta):
    """
    Function for raycasting,

    It checks if the player has visual of the object. And determines if he can shoot it.

    :param player_position: The position of the player
    :type player_position: tuple
    :param player_map_position: The map tile position of the player
    :type player_map_position: tuple
    :param self_map_position: The map position of the object
    :type self_map_position: tuple
    :param game_map: The game map
    :type game_map: dict
    :param theta: theta angle
    :type theta: float
    :return: True or False
    :rtype: bool
    """

    if player_map_position == self_map_position:
        return True

    wall_dist_v, wall_dist_h = 0, 0
    player_dist_v, player_dist_h = 0, 0

    ox, oy = player_position
    x_map, y_map = player_map_position

    ray_angle = theta

    sin_a = np.sin(ray_angle)
    cos_a = np.cos(ray_angle)

    # horizontals
    y_hor, dy = (y_map + 1, 1) if sin_a > 0 else (y_map - 1e-6, -1)

    depth_hor = (y_hor - oy) / sin_a
    x_hor = ox + depth_hor * cos_a

    delta_depth = dy / sin_a
    dx = delta_depth * cos_a

    for i in range(MAX_DEPTH):
        tile_hor = int(x_hor), int(y_hor)
        if tile_hor == self_map_position:
            player_dist_h = depth_hor
            break
        if tile_hor in game_map:
            wall_dist_h = depth_hor
            break
        x_hor += dx
        y_hor += dy
        depth_hor += delta_depth

    # verticals
    x_vert, dx = (x_map + 1, 1) if cos_a > 0 else (x_map - 1e-6, -1)

    depth_vert = (x_vert - ox) / cos_a
    y_vert = oy + depth_vert * sin_a

    delta_depth = dx / cos_a
    dy = delta_depth * sin_a

    for i in range(MAX_DEPTH):
        tile_vert = int(x_vert), int(y_vert)
        if tile_vert == self_map_position:
            player_dist_v = depth_vert
            break
        if tile_vert in game_map:
            wall_dist_v = depth_vert
            break
        x_vert += dx
        y_vert += dy
        depth_vert += delta_depth

    player_dist = max(player_dist_v, player_dist_h)
    wall_dist = max(wall_dist_v, wall_dist_h)

    if 0 < player_dist < wall_dist or not wall_dist:
        return True
    return False
