import settings
import pygame as pg


class Sound:
    def __init__(self, game):
        self.game = game
        pg.mixer.init(buffer=2048)
        self.path = 'resources/sound/'
        self.shotgun = pg.mixer.Sound(self.path + 'shotgun.wav')
        self.npc_pain = pg.mixer.Sound(self.path + 'npc_pain.wav')
        self.npc_death = pg.mixer.Sound(self.path + 'npc_death.wav')
        self.player_pain = pg.mixer.Sound(self.path + 'player_pain.wav')
        self.theme = pg.mixer.music.load(self.path + 'theme.mp3')
        self.chainsaw_fire = pg.mixer.Sound(self.path + 'fire_chainsaw.wav')
        self.minigun_fire = pg.mixer.Sound(self.path + 'dspistol.wav')
        self.barrel_exploding = pg.mixer.Sound(self.path + 'barrel_exploding.wav')


    def update(self):
        pg.mixer.music.set_volume(settings.MAIN_VOLUME)  # for volume
        self.chainsaw_fire.set_volume(settings.MAIN_VOLUME)
        self.minigun_fire.set_volume(settings.MAIN_VOLUME)
        self.barrel_exploding.set_volume(settings.MAIN_VOLUME)
        self.npc_pain.set_volume(settings.MAIN_VOLUME)
        self.npc_death.set_volume(settings.MAIN_VOLUME)
        self.player_pain.set_volume(settings.MAIN_VOLUME)
        self.shotgun.set_volume(settings.MAIN_VOLUME)
