import pygame as pg
import sys
import settings
from settings import *
from map import *
from player import *
from raycasting import *
from renderer import *
from sprite_object import *
from object_handler import *
from weapons import *
from sound import *
from hud import *
from raycasting import *
from sprite_object import *
from interactions import *
from path_find_bfs import *
from main_menu import *
from save_and_load_game import *

pg.init()


class Game:
    def __init__(self):
        self.load = LoadGame(self)
        # self.screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
        self.screen = pg.display.set_mode(SCREEN_RESOLUTION)
        self.clock = pg.time.Clock()  # get clock
        self.delta_time = 1
        self.global_trigger = False  # for npc death animation
        self.global_event = pg.USEREVENT + 0  # assign it to the pygame custom events
        pg.time.set_timer(self.global_event, 40)  # timer again for the npc death animations
        self.menu_trigger = True
        self.pause = False  # for pausing the game

        self.main_menu = MainMenu(self)
        self.new_game_menu = NewGame(self)
        self.save_game_menu = SaveGameMenu(self)
        self.load_game_menu = LoadGameMenu(self)
        self.options_game_menu = Options(self)
        self.final_score_menu = FinalScore(self)
        self.save = SaveGame(self)

        self.menu()
        self.new_game()

    def menu(self):
        pg.mouse.set_visible(True)

        self.main_menu.run()

    def new_game(self):

        self.map = Map(self)
        self.player = Player(self)
        self.object_renderer = ObjectRenderer(self)
        self.raycasting = RayCasting(self)
        self.object_handler = ObjectHandler(self)
        # this is done for fast weapon switch code optimization maybe :d
        self.weapon = Chainsaw(self)
        self.weapon1 = Chainsaw(self)
        self.weapon2 = Shotgun(self)
        self.weapon3 = Minigun(self)
        # for minigun not to forget
        self.sound = Sound(self)
        self.hud = Hud(self)
        self.npc = NPC(self)
        self.sc_map = pg.Surface((self.map.cols * MINIMAP_TILE_SIZE, self.map.rows * MINIMAP_TILE_SIZE))
        self.sprite_object = SpriteObject(self)
        self.interactions = ObjectInteraction(self)
        self.path = PathFindingBFS(self)

        pg.mixer.music.play(-1)
        self.run()

    def update(self):

        pg.mouse.set_visible(False)
        self.player.update()
        self.raycasting.update()
        self.object_handler.update()
        self.weapon.update()
        self.sound.update()
        # showing minimap on the screen
        self.screen.blit(self.sc_map, (WIDTH - self.map.cols * MINIMAP_TILE_SIZE, 0))

        pg.display.flip()
        self.delta_time = self.clock.tick(60)
        pg.display.set_caption(f'{self.clock.get_fps() :.1f}')

        self.save.take_game_data()

    def draw(self):
        self.sc_map.fill(DARKGRAY)
        self.object_renderer.draw()
        # drawing the minimap
        self.map.draw()
        self.player.draw()
        self.object_handler.draw()

    def check_events(self):
        # shooting logic and event logic
        self.global_trigger = False
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == self.global_event:
                self.global_trigger = True
            self.player.single_fire_event(event)  # this is for shooting logic
            self.player.weapon_selection(event)  # weapon selection

    def run(self):
        while True and not self.pause:
            self.check_events()
            self.draw()
            self.update()


if __name__ == '__main__':
    game = Game()
    # game.main_menu.run()
