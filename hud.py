from collections import deque
from settings import *
import os

WIDTH = WIDTH
HEIGHT = HEIGHT


class Hud:
    """"Class hud everython that is showed on the screen like ammo, weapon selections, small player sprite animations,
    without the weapons they are in a different class Weapons and the minimap."""

    def __init__(self, game):
        self.game = game
        # getting the hud image and transforming it to size
        self.hud_image = pg.image.load("resources/HUD/HUD.png")
        self.hud_size = self.hud_image.get_size()
        self.hud_image = pg.transform.scale(self.hud_image, (WIDTH, self.hud_size[1]))

        # load small player sprites:
        self.player_small_sprite = self.get_images("resources/HUD/player_sprite")
        self.player_small_sprite_transformed = deque()
        for i in self.player_small_sprite:
            self.player_small_sprite_transformed.append(pg.transform.scale(i, (WIDTH // 8, self.hud_size[1])))
        self.small_player_image_size = self.player_small_sprite_transformed[0].get_size()

        # load weapon icons
        self.weapons_transformed = []
        self.weapons = self.get_images("resources/HUD/weapons")
        for i in self.weapons:
            self.weapons_transformed.append(pg.transform.rotate(pg.transform.scale(i, (WIDTH // 10, HEIGHT // 10)), 35))

        # get the time for player animation
        self.time_prev = pg.time.get_ticks()
        self.wait = 2500

    def get_images(self, path):
        """"Getting the hud images and converting them to transparent"""
        images = deque()
        for file_name in os.listdir(path):
            if os.path.isfile(os.path.join(path, file_name)):
                img = pg.image.load(path + '/' + file_name).convert()
                img.set_colorkey("white")
                images.append(img.convert_alpha())
        return images

    def animate_player_hud_sprite(self):
        """"Animation function for the small player sprite in the
        middle of the hud"""
        time_now = pg.time.get_ticks()
        if time_now - self.time_prev > self.wait:
            self.time_prev = time_now
            self.player_small_sprite_transformed.rotate(-1)

    def helper_for_hud_selected_weapon_view(self):
        """"Basically the function name explains itself :D"""
        if self.game.player.weapon_selected == "chainsaw":
            self.game.screen.blit(self.weapons_transformed[1], (0, 0))
        else:
            self.game.screen.blit(self.weapons_transformed[0], (0, 0))

        if self.game.player.weapon_selected == "shotgun":
            self.game.screen.blit(self.weapons_transformed[5], (0, self.weapons_transformed[5].get_size()[1]))
        else:
            self.game.screen.blit(self.weapons_transformed[4], (0, self.weapons_transformed[1].get_size()[1]))

        if self.game.player.weapon_selected == "minigun":
            self.game.screen.blit(self.weapons_transformed[3], (0, self.weapons_transformed[3].get_size()[1] * 2))
        else:
            self.game.screen.blit(self.weapons_transformed[2], (0, self.weapons_transformed[1].get_size()[1] * 1.8))

    def draw(self):
        # showing on the screen
        self.game.screen.blit(self.hud_image, (0, HEIGHT - self.hud_image.get_size()[1]))
        self.animate_player_hud_sprite()
        self.game.screen.blit(self.player_small_sprite_transformed[0], (HALF_WIDTH - self.small_player_image_size[0] // 2, HEIGHT - self.hud_size[1]))
        # weapons
        self.helper_for_hud_selected_weapon_view()
