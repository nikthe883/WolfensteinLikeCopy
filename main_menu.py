import pygame as pg
import sys
import os
import settings
from button import Button, Slider
from player import *
from datetime import datetime


class MainMenu:
    def __init__(self, game):

        self.game = game
        self.main_menu_image = pg.image.load('resources/menu/menu_images/main_menu_bg.jpg').convert_alpha()

        self.main_menu_image = pg.transform.scale(self.main_menu_image, (WIDTH * 2, HEIGHT))

        self.rotate_back = False
        self.main_menu_image_position = 0
        self.delta_time = 1
        self.clock = pg.time.Clock()

        self.resume_game_button = Button(self.game.screen, 'resources/menu/buttons/resume.png', 1.5, 1.9, action_lock=True)
        self.new_game_button = Button(self.game.screen, 'resources/menu/buttons/new_game.png', 1.5, 1.9)
        self.load_game_button = Button(self.game.screen, 'resources/menu/buttons/load_game.png', 1.5, 1.9)
        self.save_game_button = Button(self.game.screen, 'resources/menu/buttons/save_game.png', 1.5, 1.9)
        self.options_button = Button(self.game.screen, 'resources/menu/buttons/options.png', 1.5, 1.9)
        self.exit_button = Button(self.game.screen, 'resources/menu/buttons/exit.png', 1.5, 1.9)

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

    def start_new_game(self):
        if self.new_game_button.action():
            self.game.new_game_menu.new_game_trigger = True
            self.game.new_game_menu.run()

    def save_game(self):
        if self.save_game_button.action():
            self.game.save_game_menu.save_game_menu_trigger = True
            self.game.save_game_menu.run()

    def load_game(self):
        if self.load_game_button.action():
            self.game.load_game_menu.load_game_menu_trigger = True
            self.game.load_game_menu.run()

    def update(self):
        self.options()
        self.resume_game()
        self.load_game()
        self.save_game()
        self.start_new_game()
        self.delta_time = self.clock.tick(60)
        pg.display.set_caption(f'{self.clock.get_fps() :.1f}')
        pg.display.flip()


    def draw_background(self):
        """Function to draw background and to move the bg image from one side
        to the other side"""
        self.game.screen.blit(self.main_menu_image, (0, 0), (self.main_menu_image_position % WIDTH, 0, WIDTH, HEIGHT))
        if not self.rotate_back:
            self.main_menu_image_position += 0.5
            if self.main_menu_image_position == WIDTH:
                self.rotate_back = True
        if self.rotate_back:
            self.main_menu_image_position -= 0.5
            if self.main_menu_image_position == 0:
                self.rotate_back = False

    def exit_game(self):
        if self.exit_button.action():
            pg.quit()
            sys.exit()

    def resume_game(self):
        if self.resume_game_button.action():
            self.game.pause = False
            self.game.menu_trigger = False

    def options(self):
        if self.options_button.action():
            self.game.options_game_menu.options_menu_trigger = True
            self.game.options_game_menu.run()

    def draw(self):
        """Drawing function of the menu"""
        self.draw_background()
        if self.game.pause:
            self.resume_game_button.action_lock = False
            self.resume_game_button.draw(WIDTH // 2 - self.load_game_button.get_size[0], HEIGHT // 19)

        self.new_game_button.draw(WIDTH // 2 - self.load_game_button.get_size[0], HEIGHT // 5.2)
        self.load_game_button.draw(WIDTH // 2 - self.load_game_button.get_size[0], HEIGHT // 3)
        self.save_game_button.draw(WIDTH // 2 - self.save_game_button.get_size[0], HEIGHT // 2.1)
        self.options_button.draw(WIDTH // 2 - self.save_game_button.get_size[0], HALF_HEIGHT * 1.2)
        self.exit_button.draw(WIDTH // 2 - self.save_game_button.get_size[0], HALF_HEIGHT * 1.5)
        self.exit_game()
        self.start_new_game()

    def run(self):
        while self.game.menu_trigger:
            self.check_events()
            self.update()
            self.draw()


class NewGame:
    def __init__(self, game):
        self.game = game
        self.new_game_image = pg.image.load('resources/menu/menu_images/new_game_bg.jpg').convert_alpha()

        self.new_game_image = pg.transform.scale(self.new_game_image, (WIDTH * 2, HEIGHT))

        self.digit_size = WIDTH // DIGIT_SIZE_SCALE
        self.digit_images = [self.get_textures(f'resources/textures/digits/{i}.png', [self.digit_size] * 2)
                             for i in range(11)]
        self.digits = dict(zip(map(str, range(11)), self.digit_images))

        self.rotate_back = False
        self.new_game_image_position = 0
        self.delta_time = 1
        self.clock = pg.time.Clock()
        self.new_game_trigger = True

        self.start_game_button = Button(self.game.screen, 'resources/menu/buttons/start_game.png', 1, 1.2)
        self.win_condition_button = Button(self.game.screen, 'resources/menu/buttons/win_condition.png', 0.8, 0.8)
        self.kills_condition_button = Button(self.game.screen, 'resources/menu/buttons/kills_win_condition.png', 0.8, 1, option=False)
        self.time_condition_button = Button(self.game.screen, 'resources/menu/buttons/time_win_condition.png', 0.8, 1, option=False)

        self.easy_condition_button = Button(self.game.screen, 'resources/menu/buttons/easy.png', 0.8, 1, option=False)
        self.hard_condition_button = Button(self.game.screen, 'resources/menu/buttons/hard.png', 0.8, 1, option=False)

        self.enemy_number_button = Button(self.game.screen, 'resources/menu/buttons/enemy_number.png', 0.8, 0.8)
        self.difficulty_button = Button(self.game.screen, 'resources/menu/buttons/difficulty.png', 0.8, 0.8)
        self.level_size_button = Button(self.game.screen, 'resources/menu/buttons/level_size.png', 0.8, 0.8)
        self.options_button = Button(self.game.screen, 'resources/menu/buttons/options.png', 1, 1.2)
        self.back_button = Button(self.game.screen, 'resources/menu/buttons/back.png', 1, 1.2)

        self.kill_number_slider = Slider(self.game.screen, self.win_condition_button.get_size[0] * 2, HEIGHT // 4)
        self.tile_number_slider = Slider(self.game.screen, self.win_condition_button.get_size[0] * 2, HEIGHT // 3)
        self.number_of_enemy_slider = Slider(self.game.screen, self.win_condition_button.get_size[0] * 2, HEIGHT // 2.4)

        # options
        self.npc_kill_condition = True

    def get_textures(self, path, res=(TEXTURE_SIZE, TEXTURE_SIZE)):
        """Getting images and converting them"""
        texture = pg.image.load(path).convert_alpha()
        return pg.transform.scale(texture, res)

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

    def draw_background(self):
        """Function to draw background and to move the bg image from one side
        to the other side"""
        self.game.screen.blit(self.new_game_image, (0, 0), (self.new_game_image_position % WIDTH, 0, WIDTH, HEIGHT))
        if not self.rotate_back:
            self.new_game_image_position += 0.5
            if self.new_game_image_position == WIDTH:
                self.rotate_back = True
        if self.rotate_back:
            self.new_game_image_position -= 0.5
            if self.new_game_image_position == 0:
                self.rotate_back = False

    def update(self):
        self.start_new_game()
        self.win_condition_options()
        self.enemy_count_options()
        self.map_generation_options()
        self.game_difficulty_options()
        self.delta_time = self.clock.tick(60)
        self.kill_number_slider.update()
        self.tile_number_slider.update()
        self.number_of_enemy_slider.update()

        pg.display.set_caption(f'{self.clock.get_fps() :.1f}')
        pg.display.flip()

    def back_main_menu(self):
        if self.back_button.action():
            self.new_game_trigger = False

    def draw_numbers(self, number, width, height):
        """Drawing numbers for the kills or the time variables"""
        for i, char in enumerate(str(number)):
            self.game.screen.blit(self.digits[char], ((i * self.digit_size) + width, height))

    def win_condition_options(self):
        if self.kills_condition_button.action():
            self.time_condition_button.option = False
            self.kills_condition_button.option = True
            settings.NPC_KILL_CONDITION = True

        if self.kills_condition_button.option:
            settings.MAX_NPC_KILLED = 10 + self.kill_number_slider.get_slider_value * 2
            self.draw_numbers(settings.MAX_NPC_KILLED, self.kill_number_slider.get_position[0] * 1.7, HEIGHT // 4)

        if self.time_condition_button.action():
            self.kills_condition_button.option = False
            self.time_condition_button.option = True
            settings.NPC_KILL_CONDITION = False

        if self.time_condition_button.option:
            settings.WIN_TIME = 9999 + 9999 * self.kill_number_slider.get_slider_value
            self.draw_numbers(settings.WIN_TIME // 1000, self.kill_number_slider.get_position[0] * 1.7, HEIGHT // 4)

    def game_difficulty_options(self):
        if self.easy_condition_button.action():
            self.hard_condition_button.option = False
            self.easy_condition_button.option = True
            settings.DIFFICULTY = "easy"
        if self.hard_condition_button.action():
            self.hard_condition_button.option = True
            self.easy_condition_button.option = False
            settings.DIFFICULTY = "hard"

    def map_generation_options(self):
        settings.LEVEL_SIZE = 30 + self.tile_number_slider.get_slider_value // 5
        self.draw_numbers(settings.LEVEL_SIZE, self.kill_number_slider.get_position[0] * 1.7, HEIGHT // 3)

    def enemy_count_options(self):
        settings.NPC_COUNT = 5 + self.number_of_enemy_slider.get_slider_value // 2
        self.draw_numbers(settings.NPC_COUNT, self.kill_number_slider.get_position[0] * 1.7, HEIGHT // 2.4)

    def start_new_game(self):
        if self.start_game_button.action():
            self.new_game_trigger = False
            self.game.menu_trigger = False
            self.game.pause = False
            self.game.new_game()

    def draw(self):
        """Drawing function of the menu"""
        # drawing bg
        self.draw_background()
        # starting the game
        self.start_game_button.draw(WIDTH - self.start_game_button.get_size[0] * 1.2, 1.2)
        # winning conditions
        self.win_condition_button.draw(0, HEIGHT // 4)
        self.kills_condition_button.draw(self.win_condition_button.get_size[0], HEIGHT // 4)
        self.time_condition_button.draw(self.win_condition_button.get_size[0] * 1.5, HEIGHT // 4)
        self.kill_number_slider.draw()
        # map gen
        self.level_size_button.draw(0, HEIGHT // 3)
        self.tile_number_slider.draw()
        # enemy number
        self.enemy_number_button.draw(0, HEIGHT // 2.4)
        self.number_of_enemy_slider.draw()
        # difficulty
        self.difficulty_button.draw(0, HEIGHT // 2.1)
        self.easy_condition_button.draw(self.win_condition_button.get_size[0], HEIGHT // 2.1)
        self.hard_condition_button.draw(self.win_condition_button.get_size[0] * 1.5, HEIGHT // 2.1)
        # for going back
        self.back_button.draw(1.2, 1.2)
        self.back_main_menu()

    def run(self):
        while self.new_game_trigger:
            self.check_events()
            self.update()
            self.draw()


class SaveGameMenu:
    def __init__(self, game):
        self.game = game
        self.new_game_image = pg.image.load('resources/menu/menu_images/save_game_bg.jpg').convert_alpha()

        self.new_game_image = pg.transform.scale(self.new_game_image, (WIDTH * 2, HEIGHT))

        self.rotate_back = False
        self.new_game_image_position = 0
        self.delta_time = 1
        self.clock = pg.time.Clock()
        self.save_game_menu_trigger = True
        self.dt_string = ""
        self.blit_date_height_pos = 0
        self.draw_date_no_error = True
        self.update_list = True

        self.save_game_button = Button(self.game.screen, 'resources/menu/buttons/save_game.png', 1, 1.2)
        self.delete_save_game_button = Button(self.game.screen, 'resources/menu/buttons/delete.png', 1, 1.2)
        self.empty_slot_list = []

        for i in range(7):
            self.empty_slot_list.append(Button(self.game.screen, 'resources/menu/buttons/empty_slot.png', 1, 1.2, option=False))

        self.date_images_dict = {}
        for i in os.listdir('resources/menu/date_images'):
            i = i.split(".png")
            self.date_images_dict[i[0]] = self.get_textures(f'resources/menu/date_images/{i[0]}.png', 0.8)

        self.empty_slot_list_placement = [
            (0, HEIGHT // 4),
            (0, HEIGHT // 3),
            (0, HEIGHT // 2.4),
            (0, HEIGHT // 2),
            (0, HEIGHT // 1.7),
            (0, HEIGHT // 1.5),
            (0, HEIGHT // 1.34),
        ]
        self.digit_size = WIDTH // DIGIT_SIZE_SCALE

        self.date_images_list_blit = []
        self.back_button = Button(self.game.screen, 'resources/menu/buttons/back.png', 1, 1.2)
        self.show_saved_game_slots()

    def show_saved_game_slots(self):
        savings_data = self.game.load.open_menu_saving_data()
        for i in range(len(self.empty_slot_list)):
            if str(i) in savings_data:
                self.empty_slot_list[i] = Button(self.game.screen, 'resources/menu/buttons/saved_game.png', 1, 1.2)

    def get_textures(self, path, scale):
        """Getting images and converting them"""
        image_load = pg.image.load(path).convert_alpha()
        width = image_load.get_width()
        height = image_load.get_height()
        image = pg.transform.scale(image_load, (int(width * scale), int(height * scale)))
        return image

    def draw_background(self):
        """Function to draw background and to move the bg image from one side
        to the other side"""
        self.game.screen.blit(self.new_game_image, (0, 0), (self.new_game_image_position % WIDTH, 0, WIDTH, HEIGHT))
        if not self.rotate_back:
            self.new_game_image_position += 0.5
            if self.new_game_image_position == WIDTH:
                self.rotate_back = True
        if self.rotate_back:
            self.new_game_image_position -= 0.5
            if self.new_game_image_position == 0:
                self.rotate_back = False

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

    def back_main_menu(self):
        if self.back_button.action():
            self.save_game_menu_trigger = False

    def choose_slot(self):
        for i in range(len(self.empty_slot_list)):
            if self.empty_slot_list[i].action():
                self.empty_slot_list[i].option = True
                button_list_option_false = self.empty_slot_list[:i] + self.empty_slot_list[i + 1:]
                for c in button_list_option_false:
                    c.option = False

    def draw_date(self, height, data):
        for i, char in enumerate(str(data)):
            if char == "/":
                self.game.screen.blit(self.date_images_dict['back_slash'], ((i * self.digit_size) + self.empty_slot_list[0].get_size[0] * 1.3, height))
            elif char == ":":
                self.game.screen.blit(self.date_images_dict['colon'], ((i * self.digit_size) + self.empty_slot_list[0].get_size[0] * 1.3, height))
            else:
                self.game.screen.blit(self.date_images_dict[char], ((i * self.digit_size) + self.empty_slot_list[0].get_size[0] * 1.3, height))

    def save_game(self):

        if self.save_game_button.action():
            for i in range(len(self.empty_slot_list)):
                if self.empty_slot_list[i].option:
                    try:
                        self.empty_slot_list[i] = Button(self.game.screen, 'resources/menu/buttons/saved_game.png', 1, 1.2, option=False)
                        now = datetime.now()
                        self.dt_string = now.strftime("%d/%m/%Y::%H:%M:%S")
                        self.game.save.save_game_data(i)
                        self.draw_date_no_error = True
                        self.game.save.save_menu_state(str(i), self.dt_string)



                    except AttributeError:
                        print("You can't save not existing game")
                        self.draw_date_no_error = False

    def show_saved_games(self):
        savings_data = self.game.load.open_menu_saving_data()
        for i in range(len(self.empty_slot_list)):
            if str(i) in savings_data:
                self.draw_date(self.empty_slot_list_placement[i][1], savings_data[str(i)])

    def delete_saved_games(self):
        if self.delete_save_game_button.action():
            for i in range(len(self.empty_slot_list)):
                if self.empty_slot_list[i].option:
                    self.game.save.delete_save_game(str(i))
                    self.empty_slot_list[i] = Button(self.game.screen, 'resources/menu/buttons/empty_slot.png', 1, 1.2, option=False)

    def draw(self):
        """Drawing function of the menu"""
        # drawing bg
        self.draw_background()
        # saving the game
        self.save_game_button.draw(WIDTH - self.save_game_button.get_size[0] * 1.2, 1.2)
        self.delete_save_game_button.draw(HALF_WIDTH - self.delete_save_game_button.get_size[0], 1.2)
        # save game slots
        for i in range(len(self.empty_slot_list)):
            self.empty_slot_list[i].draw(self.empty_slot_list_placement[i][0], self.empty_slot_list_placement[i][1])

        # for going back
        self.back_button.draw(1.2, 1.2)
        self.back_main_menu()

    def update(self):
        self.save_game()
        self.choose_slot()
        self.delete_saved_games()
        if self.update_list:
            self.show_saved_games()
        self.delta_time = self.clock.tick(60)
        pg.display.set_caption(f'{self.clock.get_fps() :.1f}')
        pg.display.flip()

    def run(self):
        while self.save_game_menu_trigger:
            self.check_events()
            self.update()
            self.draw()


class LoadGameMenu:
    def __init__(self, game):
        self.game = game
        self.load_game_bg_image = pg.image.load('resources/menu/menu_images/load_menu_bg.jpg').convert_alpha()

        self.load_game_bg_image = pg.transform.scale(self.load_game_bg_image, (WIDTH * 2, HEIGHT))

        self.rotate_back = False
        self.new_game_image_position = 0
        self.delta_time = 1
        self.clock = pg.time.Clock()
        self.load_game_menu_trigger = True
        self.dt_string = ""
        self.blit_date_height_pos = 0
        self.draw_date_no_error = True

        self.load_game_button = Button(self.game.screen, 'resources/menu/buttons/load_game.png', 1, 1.2)
        self.empty_slot_list = []

        for i in range(7):
            self.empty_slot_list.append(Button(self.game.screen, 'resources/menu/buttons/empty_slot.png', 1, 1.2, option=False))

        self.date_images_dict = {}
        for i in os.listdir('resources/menu/date_images'):
            i = i.split(".png")
            self.date_images_dict[i[0]] = self.get_textures(f'resources/menu/date_images/{i[0]}.png', 0.8)

        self.empty_slot_list_placement = [
            (0, HEIGHT // 4),
            (0, HEIGHT // 3),
            (0, HEIGHT // 2.4),
            (0, HEIGHT // 2),
            (0, HEIGHT // 1.7),
            (0, HEIGHT // 1.5),
            (0, HEIGHT // 1.34),
        ]
        self.digit_size = WIDTH // DIGIT_SIZE_SCALE

        self.date_images_list_blit = []
        self.back_button = Button(self.game.screen, 'resources/menu/buttons/back.png', 1, 1.2)
        self.show_loaded_game_slots()

    def show_loaded_game_slots(self):
        savings_data = self.game.load.open_menu_saving_data()
        for i in range(len(self.empty_slot_list)):
            if str(i) in savings_data:
                self.empty_slot_list[i] = Button(self.game.screen, 'resources/menu/buttons/saved_game.png', 1, 1.2)

    def get_textures(self, path, scale):
        """Getting images and converting them"""
        image_load = pg.image.load(path).convert_alpha()
        width = image_load.get_width()
        height = image_load.get_height()
        image = pg.transform.scale(image_load, (int(width * scale), int(height * scale)))
        return image

    def draw_background(self):
        """Function to draw background and to move the bg image from one side
        to the other side"""
        self.game.screen.blit(self.load_game_bg_image, (0, 0), (self.new_game_image_position % WIDTH, 0, WIDTH, HEIGHT))
        if not self.rotate_back:
            self.new_game_image_position += 0.5
            if self.new_game_image_position == WIDTH:
                self.rotate_back = True
        if self.rotate_back:
            self.new_game_image_position -= 0.5
            if self.new_game_image_position == 0:
                self.rotate_back = False

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

    def back_main_menu(self):
        if self.back_button.action():
            self.load_game_menu_trigger = False

    def choose_slot(self):
        for i in range(len(self.empty_slot_list)):
            if self.empty_slot_list[i].action():
                self.empty_slot_list[i].option = True
                button_list_option_false = self.empty_slot_list[:i] + self.empty_slot_list[i + 1:]
                for c in button_list_option_false:
                    c.option = False

    def draw_date(self, height, data):
        for i, char in enumerate(str(data)):
            if char == "/":
                self.game.screen.blit(self.date_images_dict['back_slash'], ((i * self.digit_size) + self.empty_slot_list[0].get_size[0] * 1.3, height))
            elif char == ":":
                self.game.screen.blit(self.date_images_dict['colon'], ((i * self.digit_size) + self.empty_slot_list[0].get_size[0] * 1.3, height))
            else:
                self.game.screen.blit(self.date_images_dict[char], ((i * self.digit_size) + self.empty_slot_list[0].get_size[0] * 1.3, height))

    def load_game(self):
        if self.load_game_button.action():
            for i in range(len(self.empty_slot_list)):
                if self.empty_slot_list[i].option:
                    self.game.load.open_game_data(str(i))

    def show_load_games(self):
        savings_data = self.game.load.open_menu_saving_data()
        for i in range(len(self.empty_slot_list)):
            if str(i) in savings_data:
                self.draw_date(self.empty_slot_list_placement[i][1], savings_data[str(i)])

    def draw(self):
        """Drawing function of the menu"""
        # drawing bg
        self.draw_background()
        # saving the game
        self.load_game_button.draw(WIDTH - self.load_game_button.get_size[0] * 1.2, 1.2)
        # save game slots
        for i in range(len(self.empty_slot_list)):
            self.empty_slot_list[i].draw(self.empty_slot_list_placement[i][0], self.empty_slot_list_placement[i][1])

        # for going back
        self.back_button.draw(1.2, 1.2)
        self.back_main_menu()

    def update(self):
        self.show_load_games()
        self.choose_slot()
        self.load_game()
        self.delta_time = self.clock.tick(60)
        pg.display.set_caption(f'{self.clock.get_fps() :.1f}')
        pg.display.flip()

    def run(self):
        while self.load_game_menu_trigger:
            self.check_events()
            self.update()
            self.draw()


class Options:
    def __init__(self, game):
        self.screen_resolution_dict = None
        self.game = game
        self.options_menu_bg = pg.image.load('resources/menu/menu_images/options_menu_bg.jpg').convert_alpha()

        self.options_menu_bg = pg.transform.scale(self.options_menu_bg, (WIDTH * 2, HEIGHT))

        self.res_images = {}
        for i in os.listdir('resources/menu/date_images'):
            i = i.split(".png")
            self.res_images[i[0]] = self.get_textures(f'resources/menu/date_images/{i[0]}.png', 0.8)

        self.options_data = {}

        self.rotate_back = False
        self.options_menu_bg_position = 0
        self.delta_time = 1
        self.clock = pg.time.Clock()
        self.options_menu_trigger = True

        self.digit_size = WIDTH // DIGIT_SIZE_SCALE

        self.apply_changes = Button(self.game.screen, 'resources/menu/buttons/apply_changes.png', 0.6, 0.6)
        self.save_button = Button(self.game.screen, 'resources/menu/buttons/save.png', 1, 1.2)
        self.resolution_button = Button(self.game.screen, 'resources/menu/buttons/resolution.png', 0.8, 0.8)
        self.fullscreen_image = Button(self.game.screen, 'resources/menu/buttons/fullscreen.png', 0.8, 0.8)
        self.volume = Button(self.game.screen, 'resources/menu/buttons/volume.png', 0.8, 0.8)
        self.mouse_sensitivity = Button(self.game.screen, 'resources/menu/buttons/mouse_sens.png', 0.8, 0.8)

        self.forwards = Button(self.game.screen, 'resources/menu/buttons/forward.png', 0.8, 1)
        self.backwards = Button(self.game.screen, 'resources/menu/buttons/back.png', 0.8, 1)
        self.left = Button(self.game.screen, 'resources/menu/buttons/left.png', 0.8, 1)
        self.right = Button(self.game.screen, 'resources/menu/buttons/right.png', 0.8, 1)

        self.back_button = Button(self.game.screen, 'resources/menu/buttons/back.png', 1, 1.2)

        self.resolution_slider = Slider(self.game.screen, self.resolution_button.get_size[0] * 1.2, HEIGHT // 5, saving=True,
                                        value=settings.VALUE_SLIDER_DATA * 20)
        self.volume_slider = Slider(self.game.screen, self.resolution_button.get_size[0] * 1.2, HEIGHT // 3.5, saving=True,
                                    value=settings.MAIN_VOLUME * 100)
        self.mouse_sensitivity_slider = Slider(self.game.screen, self.resolution_button.get_size[0] * 1.2, HEIGHT // 2.7, saving=True,
                                               value=settings.MOUSE_SENSITIVITY * 10000)

        self.key_binding_buttons_list = [self.forwards, self.backwards, self.left, self.right]
        self.buttons_vertical_placement = [HEIGHT / 1.97, HEIGHT / 1.73, HEIGHT / 1.53, HEIGHT / 1.39]

        self.options_data['movements'] = settings.movement_dict

    def get_textures(self, path, scale):
        """Getting images and converting them"""
        image_load = pg.image.load(path).convert_alpha()
        width = image_load.get_width()
        height = image_load.get_height()
        image = pg.transform.scale(image_load, (int(width * scale), int(height * scale)))
        return image

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

            if event.type == pg.KEYDOWN:
                for i in range(len(self.key_binding_buttons_list)):
                    if self.key_binding_buttons_list[i].option:
                        settings.movement_dict[i] = event.key

    def draw_background(self):
        """Function to draw background and to move the bg image from one side
        to the other side"""
        self.game.screen.blit(self.options_menu_bg, (0, 0), (self.options_menu_bg_position % WIDTH, 0, WIDTH, HEIGHT))
        if not self.rotate_back:
            self.options_menu_bg_position += 0.5
            if self.options_menu_bg_position == WIDTH:
                self.rotate_back = True
        if self.rotate_back:
            self.options_menu_bg_position -= 0.5
            if self.options_menu_bg_position == 0:
                self.rotate_back = False

    def update(self):
        self.key_bindings()
        self.mouse_sensitivity_option()
        self.volume_option()
        self.save_options()
        self.resolution_option()
        self.delta_time = self.clock.tick(60)
        self.resolution_slider.update()
        self.volume_slider.update()
        self.mouse_sensitivity_slider.update()

        pg.display.set_caption(f'{self.clock.get_fps() :.1f}')
        pg.display.flip()

    def back_main_menu(self):
        if self.back_button.action():
            self.options_menu_trigger = False

    def draw_numbers(self, number, width, height):
        for i, char in enumerate(str(number)):
            if char == "/":
                self.game.screen.blit(self.res_images['back_slash'], ((i * self.digit_size) + width, height))
            elif char == ":":
                pass
            else:
                self.game.screen.blit(self.res_images[char], ((i * self.digit_size) + width, height))

    def resolution_option(self):
        res_data = {
            0: "1280/800",
            1: "1360/768",
            2: "1440/900",
            3: "1600/900",
            4: "fullscreen"
        }
        resolution_image = ''
        res = int(self.resolution_slider.get_slider_value / 20)

        if res in res_data:
            resolution_image = res_data[res]

        if resolution_image == 'fullscreen':
            self.fullscreen_image.draw(self.resolution_slider.get_position[0] * 2.5, HEIGHT // 5)
            self.options_data['resolution'] = {
                "height": "fullscreen",
                "width": "fullscreen",
                "slider_value": res
            }

        else:
            self.draw_numbers(resolution_image, self.resolution_slider.get_position[0] * 2.5, HEIGHT // 5)
            height = int(resolution_image.split("/")[1])
            width = int(resolution_image.split("/")[0])
            self.options_data['resolution'] = {
                "height": height,
                "width": width,
                "slider_value": res
            }

    def volume_option(self):
        self.volume_number = self.volume_slider.get_slider_value
        self.draw_numbers(self.volume_number, self.resolution_slider.get_position[0] * 2.5, HEIGHT // 3.5)

    def mouse_sensitivity_option(self):
        self.sensitivity = self.mouse_sensitivity_slider.get_slider_value
        self.draw_numbers(self.sensitivity, self.resolution_slider.get_position[0] * 2.5, HEIGHT // 2.7)


    def save_options(self):
        if self.save_button.action():
            settings.MAIN_VOLUME = self.volume_number / 100
            self.options_data['volume'] = self.volume_number / 100
            settings.MOUSE_SENSITIVITY = 0.00001 + self.sensitivity / 100000
            self.options_data['mouse_sens'] = 0.00001 + self.sensitivity / 100000
            self.game.save.save_options(self.options_data)



    def draw_inputs_helper(self, key_binding, width, height):
        text = settings.FONT.render(pg.key.name(key_binding), True, settings.RED)
        text_rect = text.get_rect()
        text_rect.center = (width, height)
        self.game.screen.blit(text, text_rect)

    def draw_inputs(self):
        for i in range(len(self.key_binding_buttons_list)):
            self.draw_inputs_helper(settings.movement_dict[i], self.forwards.get_size[0] * 1.7, self.buttons_vertical_placement[i] + 20)

    def key_bindings(self):
        for i in range(len(self.key_binding_buttons_list)):
            if self.key_binding_buttons_list[i].action():
                self.key_binding_buttons_list[i].option = True
                button_list_option_false = self.key_binding_buttons_list[:i] + self.key_binding_buttons_list[i + 1:]
                for c in button_list_option_false:
                    c.option = False

    def draw(self):
        """Drawing function of the menu"""

        # drawing bg
        self.draw_background()
        # saving the options
        self.save_button.draw(WIDTH - self.save_button.get_size[0] * 1.1, 1.2)
        # apply changes need restart picture
        self.apply_changes.draw(0, HEIGHT - self.apply_changes.get_size[1])
        # resolution settings
        self.resolution_button.draw(0, HEIGHT // 5)
        self.resolution_slider.draw()
        # sound settings
        self.volume.draw(0, HEIGHT // 3.4)
        self.volume_slider.draw()
        # mouse sensitivity
        self.mouse_sensitivity.draw(0, HEIGHT // 2.7)
        self.mouse_sensitivity_slider.draw()
        # player controls
        for i in range(len(self.key_binding_buttons_list)):
            self.key_binding_buttons_list[i].draw(0, self.buttons_vertical_placement[i])
        # for going back
        self.back_button.draw(1.2, 1.2)
        self.back_main_menu()

        self.draw_inputs()

    def run(self):
        while self.options_menu_trigger:
            self.check_events()
            self.update()
            self.draw()


class FinalScore:

    def __init__(self, game):

        self.game = game
        self.options_menu_bg = pg.image.load('resources/menu/menu_images/final_score_bg.jpg').convert_alpha()

        self.options_menu_bg = pg.transform.scale(self.options_menu_bg, (WIDTH * 2, HEIGHT))

        self.res_images = {}
        for i in os.listdir('resources/menu/date_images'):
            i = i.split(".png")
            self.res_images[i[0]] = self.get_textures(f'resources/menu/date_images/{i[0]}.png', 0.8)

        self.rotate_back = False
        self.options_menu_bg_position = 0
        self.delta_time = 1
        self.clock = pg.time.Clock()
        self.final_score_menu_trigger = True
        self.dt_string = ""
        self.blit_date_height_pos = 0
        self.draw_date_no_error = True
        self.digit_size = WIDTH // DIGIT_SIZE_SCALE

        self.win_image = Button(self.game.screen, 'resources/menu/buttons/you_win.png', 0.8, 0.8)
        self.lost_image = Button(self.game.screen, 'resources/menu/buttons/you_lost.png', 0.8, 0.8)

        self.score_image = Button(self.game.screen, 'resources/menu/buttons/score.png', 0.8, 0.8)
        self.enemy_killed_image = Button(self.game.screen, 'resources/menu/buttons/enemy_killed.png', 0.8, 0.8)
        self.damage_dealt_image = Button(self.game.screen, 'resources/menu/buttons/damage_dealt.png', 0.8, 0.8)
        self.damage_received_image = Button(self.game.screen, 'resources/menu/buttons/damage_received.png', 0.8, 0.8)
        self.ammo_image = Button(self.game.screen, 'resources/menu/buttons/ammo_fired.png', 0.8, 0.8)

        self.back_button = Button(self.game.screen, 'resources/menu/buttons/back.png', 1, 1.2)

    def get_textures(self, path, scale):
        """Getting images and converting them"""
        image_load = pg.image.load(path).convert_alpha()
        width = image_load.get_width()
        height = image_load.get_height()
        image = pg.transform.scale(image_load, (int(width * scale), int(height * scale)))
        return image

    def draw_background(self):
        """Function to draw background and to move the bg image from one side
        to the other side"""
        self.game.screen.blit(self.options_menu_bg, (0, 0), (self.options_menu_bg_position % WIDTH, 0, WIDTH, HEIGHT))
        if not self.rotate_back:
            self.options_menu_bg_position += 0.5
            if self.options_menu_bg_position == WIDTH:
                self.rotate_back = True
        if self.rotate_back:
            self.options_menu_bg_position -= 0.5
            if self.options_menu_bg_position == 0:
                self.rotate_back = False

    def draw_numbers(self, number, width, height):
        """Drawing numbers for the kills or the time variables"""
        for i, char in enumerate(str(number)):
            if char == "/":
                self.game.screen.blit(self.res_images['back_slash'], ((i * self.digit_size) + width, height))
            elif char == ":":
                pass
            else:
                self.game.screen.blit(self.res_images[char], ((i * self.digit_size) + width, height))

    def back_main_menu(self):
        if self.back_button.action():
            self.final_score_menu_trigger = False
            self.game.pause = False
            self.game.menu_trigger = True
            self.game.menu()

    def update(self):
        pg.mixer.music.stop()
        self.game.sound.minigun_fire.stop()
        self.game.sound.chainsaw_fire.stop()
        pg.mouse.set_visible(True)
        self.back_main_menu()
        self.delta_time = self.clock.tick(60)
        pg.display.set_caption(f'{self.clock.get_fps() :.1f}')
        pg.display.flip()

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

    def draw(self):
        """Drawing function of the menu"""
        # drawing bg
        self.draw_background()
        # loose or win
        if self.game.player.win:
            self.win_image.draw(0, HEIGHT / 6.2)
        else:
            self.lost_image.draw(0, HEIGHT / 6.2)
        # score
        self.score_image.draw(0, HEIGHT / 4)
        self.draw_numbers(self.game.player.total_score, self.damage_received_image.get_size[0], HEIGHT // 4)
        # enemy kills
        self.enemy_killed_image.draw(0, HEIGHT // 3.1)
        self.draw_numbers(self.game.player.frag_counter, self.damage_received_image.get_size[0], HEIGHT // 3.1)
        # damage dealt
        self.damage_dealt_image.draw(0, HEIGHT // 2.4)
        self.draw_numbers(self.game.player.total_damage_delt, self.damage_received_image.get_size[0], HEIGHT // 2.5)
        # damage received
        self.damage_received_image.draw(0, HEIGHT / 2.1)
        self.draw_numbers(self.game.player.total_damage_received, self.damage_received_image.get_size[0], HEIGHT / 2.1)
        # ammo fired
        self.ammo_image.draw(0, HEIGHT / 1.8)
        self.draw_numbers(self.game.player.total_ammo_fired, self.damage_received_image.get_size[0], HEIGHT / 1.8)
        # for going back
        self.back_button.draw(1.2, 1.2)

    def run(self):
        while self.final_score_menu_trigger:
            self.check_events()
            self.update()
            self.draw()
