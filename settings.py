import math
import pygame as pg
from pygame import key
from save_and_load_game import LoadGame

pg.init()
# screen resolution. Try in case there is no game_options.txt file
try:
    options_data = LoadGame().load_options()
    resolution_data = options_data['resolution']
    VALUE_SLIDER_DATA = resolution_data["slider_value"]
    if resolution_data['height'] == "fullscreen" and resolution_data['height'] == "fullscreen":
        WIDTH = pg.display.Info().current_w
        HEIGHT = pg.display.Info().current_h
    else:
        WIDTH, HEIGHT = resolution_data['width'], resolution_data['height']

    # game settings
    MAIN_VOLUME = options_data['volume']
    MOUSE_SENSITIVITY = options_data['mouse_sens']
    # player movement
    movement_dict = {int(x): y for x, y in options_data['movements'].items()}


except (TypeError, KeyError):
    WIDTH, HEIGHT = 1200, 800
    MAIN_VOLUME = 0.1
    MOUSE_SENSITIVITY = 0.0003
    movement_dict = {
         0: 119,
         1: 115,
         2: 100,
         3: 97
    }
    VALUE_SLIDER_DATA = 1

SCREEN_RESOLUTION = WIDTH, HEIGHT
fps = 0

HALF_WIDTH = WIDTH // 2
HALF_HEIGHT = HEIGHT // 2

PLAYER_POSITION = 15, 15
PLAYER_ANGLE = 0
PLAYER_SPEED = 0.004
PLAYER_ROTATION_SPEED = 0.002
PLAYER_SIZE_SCALE = 200

PLAYER_MAX_HEALTH = 999
PLAYER_MAX_ARMOR = 400
PLAYER_MAX_MINIGUN_AMMO = 300
PLAYER_MAX_SHOTGUN_AMMO = 100
PLAYER_MAX_CHAINSAW_FUEL = 300

# drops
DROP_FREQ = 0.5

MOUSE_MAX_REL = 40
MOUSE_BORDER_LEFT = 450
MOUSE_BORDER_RIGHT = WIDTH - MOUSE_BORDER_LEFT
MOUSE_BORDER_UP = 800
MOUSE_BORDER_DOWN = HEIGHT - MOUSE_BORDER_UP

FLOOR_COLOR = (30, 30, 30)

FOV = math.pi / 3
HALF_FOV = FOV / 2
NUM_RAYS = WIDTH // 2
HALF_NUM_RAYS = NUM_RAYS // 2
DELTA_ANGLE = FOV / NUM_RAYS
MAX_DEPTH = 20

SCREEN_DIST = HALF_WIDTH / math.tan(HALF_FOV)

SCALE = WIDTH // NUM_RAYS
TEXTURE_SIZE = 256
HALF_TEXTURE_SIZE = TEXTURE_SIZE // 2

# minimap settings
MINIMAP_TILE_SIZE = 5

# HUD
DIGIT_SIZE_SCALE = 32

# interections
DISAPPEAR_DELAY = 10000

# COLORS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 0, 0)
GREEN = (0, 80, 0)
BLUE = (0, 0, 255)
DARKGRAY = (40, 40, 40)
PURPLE = (120, 0, 120)
SKYBLUE = (0, 186, 255)
YELLOW = (220, 220, 0)
SANDY = (244, 164, 96)
DARKBROWN = (97, 61, 25)
DARKORANGE = (255, 140, 0)

# USER OPTIONS
NPC_KILL_CONDITION = False
MAX_NPC_KILLED = 4
WIN_TIME = 60
# world gen
LEVEL_SIZE = 30
# npc
NPC_COUNT = 10
DIFFICULTY = "hard"

FONT = pg.font.Font(None, 100)