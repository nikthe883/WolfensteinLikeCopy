import settings
from map import *


class ObjectRenderer:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.wall_textures = self.load_wall_textures()
        self.sky_image = self.get_textures('resources/textures/sky.png', (WIDTH, HEIGHT))
        self.sky_offset = 0
        self.blood_screen = self.get_textures('resources/textures/blood_screen.png', SCREEN_RESOLUTION)
        self.digit_size = WIDTH // DIGIT_SIZE_SCALE
        self.digit_images = [self.get_textures(f'resources/textures/digits/{i}.png', [self.digit_size] * 2)
                             for i in range(11)]
        self.digits = dict(zip(map(str, range(11)), self.digit_images))
        self.game_over_image = self.get_textures('resources/textures/game_over.png', SCREEN_RESOLUTION)
        self.win_image = self.get_textures('resources/textures/win.png', SCREEN_RESOLUTION)

    def draw_timer(self):
        """Function for drawing the timer if win condition by time is True"""
        if not self.game.player.npc_kill_condition:
            counting_time = int(self.game.player.win_time - self.game.player.elapsed)
            counting_seconds = str((counting_time // 1000))

            if int(counting_seconds) <= 0:
                counting_seconds = "0"
            for i, char in enumerate(counting_seconds):
                self.screen.blit(self.digits[char], ((i * self.digit_size) + HALF_WIDTH // 1.1, 0))

    def win(self):
        """"win condition when the player have collected enough enemy kills"""
        self.screen.blit(self.win_image, (0, 0))

    def game_over(self):
        """"Loose image blit when player lost the game"""
        self.screen.blit(self.game_over_image, (0, 0))

    def draw_player_ammo(self):
        """"Function for showing the player ammo on the screen
            It enumerates the int number that is given and appends the digit number
            to the given height and width"""

        ammo = str(self.game.player.ammo_to_show)
        for i, char in enumerate(ammo):
            if len(ammo) == 3:
                self.screen.blit(self.digits[char], ((i * self.digit_size) + HALF_WIDTH // 19.5, HEIGHT - self.game.hud.hud_size[1] + 20))
            else:
                self.screen.blit(self.digits[char], ((i * self.digit_size) + HALF_WIDTH // 8.8, HEIGHT - self.game.hud.hud_size[1] + 20))

    def draw_player_health(self):
        """"Function for showing the player health on the screen
            It enumerates the int number that is given and appends the digit number
            to the given height and width"""

        health = str(self.game.player.health)

        for i, char in enumerate(health):
            if len(health) == 3:
                self.screen.blit(self.digits[char], ((i * self.digit_size) + HALF_WIDTH // 2.7, HEIGHT - self.game.hud.hud_size[1] + 20))
            else:
                self.screen.blit(self.digits[char], ((i * self.digit_size) + HALF_WIDTH // 2.4, HEIGHT - self.game.hud.hud_size[1] + 20))

    def draw_frag_counter(self):
        """"Function for showing the player kills on the screen
            It enumerates the int number that is given and appends the digit number
            to the given height and width"""

        frag = str(self.game.player.frag_counter)
        for i, char in enumerate(frag):
            if len(frag) == 1:
                self.screen.blit(self.digits[char], ((i * self.digit_size) + HALF_WIDTH // 1.35, HEIGHT - self.game.hud.hud_size[1] + 20))
            elif len(frag) == 2:
                self.screen.blit(self.digits[char], ((i * self.digit_size) + HALF_WIDTH // 1.4, HEIGHT - self.game.hud.hud_size[1] + 20))
            else:
                self.screen.blit(self.digits[char], ((i * self.digit_size) + HALF_WIDTH // 1.47, HEIGHT - self.game.hud.hud_size[1] + 20))

    def draw_player_armor(self):
        """"Function for showing the player armor on the screen
        It enumerates the int number that is given and appends the digit number
        to the given height and width"""

        armour = str(self.game.player.armor)
        for i, num in enumerate(armour):
            if len(armour) == 3:
                self.screen.blit(self.digits[num], ((i * self.digit_size) + HALF_WIDTH * 1.18, HEIGHT - self.game.hud.hud_size[1] + 20))
            else:
                self.screen.blit(self.digits[num], ((i * self.digit_size) + HALF_WIDTH * 1.21, HEIGHT - self.game.hud.hud_size[1] + 20))

    def player_damage(self):
        """Bliting image when player gets damage"""
        self.screen.blit(self.blood_screen, (0, 0))

    def draw(self):
        """Drawing all the things in the renderer"""

        self.draw_background()
        self.render_game_object()
        self.game.weapon.draw()
        self.game.hud.draw()
        self.draw_player_health()
        self.draw_frag_counter()
        self.draw_player_armor()
        self.draw_player_ammo()
        self.draw_timer()

    def draw_background(self):
        """Drawing the background. Sky image with some offset to the player position"""
        self.sky_offset = (self.sky_offset * 4.5 * self.game.player.rel) * 10
        self.screen.blit(self.sky_image, (self.sky_offset, self.game.player.half_height - HEIGHT))
        rectangle = pg.rect.Rect(0, self.game.player.half_height, WIDTH, HEIGHT)
        pg.draw.rect(self.screen, FLOOR_COLOR, rectangle)

    def render_game_object(self):
        """Rendering the game textures from the ray casting module"""
        list_objects = sorted(self.game.raycasting.objects_to_render, key=lambda t: t[0], reverse=True)
        for depth, image, pos in list_objects:
            self.screen.blit(image, pos)

    @staticmethod
    def get_textures(path, res=(TEXTURE_SIZE, TEXTURE_SIZE)):
        """Static method for getting images and converting them"""
        texture = pg.image.load(path).convert_alpha()
        return pg.transform.scale(texture, res)

    def load_wall_textures(self):
        """Loading the textures of the wall"""
        return {
            1: self.get_textures('resources/textures/1.png')
        }
