from sprite_object import *
from npc import *
from random import choices, randrange
from interactions import *
import settings


# TODO Write comments

class ObjectHandler:
    def __init__(self, game):
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
        """Spawingn the npc is loaded is True or not"""
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
        """Spawning the loot boxes"""
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
        "Spawning the animated sprites"
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
        """Updating. Here we are spawning npc, getting the sprites positions on the map and updating them.
        Returns the lists with the positions and npc sprites"""
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
        """drawing the npc on minimap"""
        if self.npc_positions:
            for i in self.npc_positions:
                pg.draw.circle(self.game.sc_map, 'red', (i[0] * MINIMAP_TILE_SIZE, i[1] * MINIMAP_TILE_SIZE), 3)
        for i in self.pick_sprites_positions:
            pg.draw.circle(self.game.sc_map, 'yellow', (i[0] * MINIMAP_TILE_SIZE, i[1] * MINIMAP_TILE_SIZE), 3)

    # Methods s adding sprites to lists
    def add_npc(self, npc):
        self.npc_list.append(npc)

    def add_sprite(self, sprite):
        self.sprite_list.append(sprite)

    def add_pick_sprites(self, sprite):
        self.pick_sprites_list.append(sprite)

    def add_interactables(self, sprite):
        self.interactable_list.append(sprite)
