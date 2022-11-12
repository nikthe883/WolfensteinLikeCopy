from typing import List, Any

from sprite_object import *
from npc import *
from random import choices, randrange
from interactions import *
import settings


class ObjectHandler:
    """
    Class for handling the in game object. Animated sprites, npc, loot boxes.

    """

    def __init__(self, game):
        """
        Init method for the ObjectHandler class.

        :param game: gets self from class Game
        """
        self.game = game
        self.sprite_list = []
        self.npc_list = []
        self.npc_sprite_path = 'resources/sprites/npc/'
        self.static_sprite_path = 'resources/sprites/static_sprites/'
        self.anim_sprite_path = 'resources/sprites/animated_sprites/'
        self.npc_positions = {}
        self.pick_sprites_positions = {}
        self.pick_sprites_list = []
        self.interactable_list = []
        self.npc_types_list = []
        self.sprite_list_positions = []

        self.enemies = settings.NPC_COUNT  # npc count
        self.npc_types = ['SoldierNPC', 'CyberDemonNPC']
        self.weights = [80, 20]  # weight for npc spawning types
        self.restricted_area = {(i, j) for i in range(10) for j in range(10)}

        # spawn collectables
        self.collectable_number = TOTAL_NUMBER_COLLECTABLES
        self.spawn_collectables()

        # spawn sprites
        self.sprites_number = TOTAL_NUMBER_SPRITES
        self.spawn_sprites()

        self.spawn_npc()

    def spawn_npc(self):
        """Spawn function for npc objects.

        Adds the npc to the list on condition if the len of the npc_list is less than the desired one
        It checks if the load game parameter is true or not.
        If the load game boolean parameter is true then adds the npc according to their previously saved positions
        If the load game boolean parameter is false, the function randomly places the npc objects in the world

        :return: None
        """

        if len(self.npc_list) < self.enemies:
            # for loading the npc
            if self.game.load.load_game:
                pos = self.game.load.loaded_data['npc_positions']
                self.npc_types_list = self.game.load.loaded_data['npc_type']
                for i, v in enumerate(pos):
                    if self.npc_types_list[i] == "SoldierNPC":
                        self.add_npc(SoldierNPC(self.game, pos=(v[0] + 0.5, v[1] + 0.5)))
                    elif self.npc_types_list[i] == 'CyberDemonNPC':
                        self.add_npc(CyberDemonNPC(self.game, pos=(v[0] + 0.5, v[1] + 0.5)))
                    self.npc = self.npc_types_list[i]
                self.game.load.load_game = False
            else:
                self.npc = choices(self.npc_types, self.weights)[0]
                pos = x, y = randrange(self.game.map.cols), randrange(self.game.map.rows)
                while (pos in self.game.map.world_map) or (pos in self.restricted_area):
                    pos = x, y = randrange(self.game.map.cols), randrange(self.game.map.rows)
                if self.npc == "SoldierNPC":
                    self.add_npc(SoldierNPC(self.game, pos=(x + 0.5, y + 0.5)))
                elif self.npc == 'CyberDemonNPC':
                    self.add_npc(CyberDemonNPC(self.game, pos=(x + 0.5, y + 0.5)))
                self.npc_types_list.append(self.npc)

    def spawn_collectables(self):
        """Spawn function for collectable objects.

        It checks if the load game parameter is true or not.
        If the load game boolean parameter is true then adds the collectable according to their previously saved positions
        If the load game boolean parameter is false, the function randomly places the collectable objects in the world

        :return: None
        """

        if self.game.load.load_game:
            pos = self.game.load.loaded_data['pick_sprite_positions']
            for i in range(len(pos)):
                self.add_interactables(ObjectInteraction(self.game, pos=(pos[i][0] + 0.5, pos[i][1] + 0.5)))
        else:
            for i in range(self.collectable_number):
                pos = x, y = randrange(self.game.map.cols), randrange(self.game.map.rows)
                while pos in self.game.map.world_map:
                    pos = x, y = randrange(self.game.map.cols), randrange(self.game.map.rows)
                self.add_interactables(ObjectInteraction(self.game, pos=(x + 0.5, y + 0.5)))

    def spawn_sprites(self):
        """
        Spawn function for sprite objects.

        It checks if the load game parameter is true or not.
        If the load game boolean parameter is true then adds the sprites according to their previously saved positions
        If the load game boolean parameter is false, the function randomly places the sprites objects in the world

        :return: None
        """

        if self.game.load.load_game:
            pos = self.game.load.loaded_data['sprite_list']
            for i in range(len(pos)):
                self.add_sprite(AnimatedSprite(self.game, pos=(pos[i][0] + 0.5, pos[i][1] + 0.5)))
        else:
            for i in range(self.sprites_number):
                pos = x, y = randrange(self.game.map.cols), randrange(self.game.map.rows)
                while pos in self.game.map.world_map:
                    pos = x, y = randrange(self.game.map.cols), randrange(self.game.map.rows)
                self.add_sprite(AnimatedSprite(self.game, pos=(x + 0.5, y + 0.5)))

    def update(self):
        """
        Updating method that is spawning the npc, getting npc positions, sprite positions, pick sprites positions and updates the lists of npc and sprites.

        :return: npc_positions, npc_type_list, pick_sprites_positions, sprite_list_positions
        """

        self.spawn_npc()
        self.npc_positions = [npc.map_pos for npc in self.npc_list if npc.alive]
        self.sprite_list_positions = [sprite.map_pos for sprite in self.sprite_list]
        self.pick_sprites_positions = [sprite.map_pos for sprite in self.interactable_list if sprite.alive]

        [sprite.update() for sprite in self.sprite_list]
        [sprite.update() for sprite in self.pick_sprites_list if not sprite.picked]
        [sprite.update() for sprite in self.interactable_list if not sprite.gone]
        [npc.update() for npc in self.npc_list]

        for npc in self.npc_list:
            if npc.gone:
                self.npc_list.remove(npc)
                self.npc_types_list.remove(self.npc)

        return self.npc_positions, self.npc_types_list, self.pick_sprites_positions, self.sprite_list_positions

    def draw(self):
        """
        Drawing function for drawing the npc positions and the barrel positions on the minimap

        :return: None
        """
        if self.npc_positions:
            for i in self.npc_positions:
                pg.draw.circle(self.game.sc_map, 'red', (i[0] * MINIMAP_TILE_SIZE, i[1] * MINIMAP_TILE_SIZE), 3)
        for i in self.pick_sprites_positions:
            pg.draw.circle(self.game.sc_map, 'yellow', (i[0] * MINIMAP_TILE_SIZE, i[1] * MINIMAP_TILE_SIZE), 3)

    # Methods s adding sprites to lists
    def add_npc(self, npc):
        """
        Function for adding npc objects to the npc list.

        :param npc: npc object
        :return: None
        """
        self.npc_list.append(npc)

    def add_sprite(self, sprite):
        """
        Function for adding sprite objects to the sprite lists

        :param sprite: sprite object
        :return: None
        """
        self.sprite_list.append(sprite)

    def add_pick_sprites(self, sprite):
        """
        Function for adding pick sprites obejct to the pick sprites list

        :param sprite: sprite object
        :return: None
        """
        self.pick_sprites_list.append(sprite)

    def add_interactables(self, sprite):
        """
        Function for adding interactable objects to the interactables list

        :param sprite: sprite object
        :return: None
        """
        self.interactable_list.append(sprite)
