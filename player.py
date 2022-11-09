import pygame as pg
from settings import *
import settings
from collections import deque
from weapons import *
import math
from random import randrange
from timeit import default_timer as timer


class Player:
    def __init__(self, game):

        self.starting_pos = None
        self.game = game
        self.clock = pg.time.Clock()
        self.x, self.y = self.place_player()
        self.angle = PLAYER_ANGLE
        self.half_height = HALF_HEIGHT
        self.shot = False
        self.health = PLAYER_MAX_HEALTH
        self.armor = PLAYER_MAX_ARMOR
        self.rel = 0

        self.health_recovery_delay = 50
        self.time_prev = pg.time.get_ticks()
        self.shotgun_ammo = 10
        self.minigun_ammo = 999
        self.vruum_vruum_fuel = PLAYER_MAX_CHAINSAW_FUEL
        self.vruum_vruum_fuel_consumption = False
        self.minigun_ammo_fires = False
        self.ammo_to_show = 0
        self.weapon_selected = "chainsaw"
        self.weapons_list = deque(["chainsaw", "shotgun", "minigun"])
        self.elapsed = 0
        self.win_time = settings.WIN_TIME
        self.max_npc_kills = settings.MAX_NPC_KILLED
        self.npc_kill_condition = settings.NPC_KILL_CONDITION
        self.time_now = 0

        # for final score

        self.total_damage_delt = 0
        self.total_damage_received = 0
        self.total_ammo_fired = 0
        self.frag_counter = 0
        self.total_score = 0
        self.win = True

        self.load()

    def score(self):
        self.total_score = self.total_ammo_fired + self.frag_counter

    def load(self):
        if self.game.load.load_game:
            player_pos = self.game.load.loaded_data['player_pos']
            self.x = player_pos[0]
            self.y = player_pos[1]
            self.health = self.game.load.loaded_data['player_health']
            self.armor = self.game.load.loaded_data['player_armor']
            self.minigun_ammo = self.game.load.loaded_data['minigun_ammo']
            self.shotgun_ammo = self.game.load.loaded_data['shotgun_ammo']
            self.vruum_vruum_fuel = self.game.load.loaded_data['fuel']
            self.npc_kill_condition = self.game.load.loaded_data['kill_condition']
            self.win_time = self.game.load.loaded_data['win_time']
            self.elapsed = self.game.load.loaded_data['timer']
            self.frag_counter = self.game.load.loaded_data['player_kills']
            self.max_npc_kills = self.game.load.loaded_data['max_npc_kill']

    def win_condition(self):

        """" Win condition on npc killed or on time passed"""
        if self.npc_kill_condition:
            if self.max_npc_kills == self.frag_counter:
                self.game.object_renderer.win()
                pg.display.flip()
                pg.time.delay(1500)

                self.game.pause = True
                self.game.final_score_menu.final_score_menu_trigger = True
                self.game.final_score_menu.run()
        else:
            if not self.game.menu_trigger and not self.game.pause:
                self.elapsed += self.game.clock.get_time()
                if self.elapsed > self.win_time:
                    self.game.object_renderer.win()
                    pg.display.flip()
                    pg.time.delay(1500)

                    self.game.pause = True
                    self.game.final_score_menu.final_score_menu_trigger = True
                    self.game.final_score_menu.run()

    def check_game_over(self):
        """Checking for game over condition"""
        if self.health < 1:
            self.game.object_renderer.game_over()
            pg.display.flip()
            pg.time.delay(1500)
            self.win = False
            self.game.pause = True
            self.game.final_score_menu.final_score_menu_trigger = True
            self.game.final_score_menu.run()

    def place_player(self):
        """A function where we randomly place the player on the map if the tile is free. If we
        don't do that from time to time the player will be placed in a wall which will make the game to freeze"""
        while True:
            self.starting_pos = (randrange(self.game.map.cols), randrange(self.game.map.rows))
            if self.starting_pos in self.game.map.world_map:
                self.starting_pos = (randrange(self.game.map.cols), randrange(self.game.map.rows))

            else:
                break

        return self.starting_pos[0] + 0.2, self.starting_pos[1] + 0.2

    def fuel_consumption_chainsaw(self):
        """"Function that checks the fuel consumption of the chainsaw and if there is no fuel it
        stops the chainsaw"""
        try:
            if self.vruum_vruum_fuel_consumption:
                self.vruum_vruum_fuel -= self.game.weapon.fuel_consumption
                self.ammo_to_show -= self.game.weapon.fuel_consumption
                self.total_ammo_fired += self.game.weapon.fuel_consumption
                self.check_ammo()
                if self.vruum_vruum_fuel <= 0:
                    self.game.weapon.vroom_vroom = False
                    self.game.sound.chainsaw_fire.stop()
        except AttributeError:
            pass

    def minigun_ammo_consumption(self):
        """"Function that checks the ammo consumption of the minigun and if there is no ammo it
        stops the chainsaw"""
        try:
            if self.minigun_ammo_fires:
                self.minigun_ammo -= self.game.weapon.ammo
                self.ammo_to_show -= self.game.weapon.minigun_shoot
                self.total_ammo_fired += self.game.weapon.minigun_shoot
                self.check_ammo()
                if self.minigun_ammo <= 0:
                    self.game.weapon.minigun_shoot = False
                    self.game.sound.minigun_fire.stop()
        except AttributeError:
            pass

    def check_ammo(self):
        """"Simple function to check if ammo is negative if it is negative make it to 0"""
        if self.ammo_to_show <= 0:
            self.ammo_to_show = 0
        if self.vruum_vruum_fuel <= 0:
            self.vruum_vruum_fuel = 0
        if self.shotgun_ammo <= 0:
            self.shotgun_ammo = 0
        if self.minigun_ammo <= 0:
            self.minigun_ammo = 0

    def weapon_selector(self):
        """"Weapon selector secondary function for """
        if self.weapon_selected == "chainsaw":
            self.ammo_to_show = self.vruum_vruum_fuel
            self.game.weapon = self.game.weapon1

        if self.weapon_selected == "shotgun":
            self.ammo_to_show = self.shotgun_ammo
            self.game.weapon = self.game.weapon2

        if self.weapon_selected == "minigun":
            self.ammo_to_show = self.minigun_ammo
            self.game.weapon = self.game.weapon3

    def weapon_selection(self, event):
        """"Weapon selection based on 1,2,3 keys and mouse wheel"""
        if self.weapon_selected == "chainsaw":
            self.ammo_to_show = self.vruum_vruum_fuel
        if self.weapon_selected == "shotgun":
            self.ammo_to_show = self.shotgun_ammo
        if self.weapon_selected == "minigun":
            self.ammo_to_show = self.minigun_ammo

        keys = pg.key.get_pressed()
        if keys[pg.K_1]:
            self.weapon_selected = "chainsaw"
            self.weapon_selector()

        if keys[pg.K_2]:
            self.weapon_selected = "shotgun"
            self.weapon_selector()

        if keys[pg.K_3]:
            self.weapon_selected = "minigun"
            self.weapon_selector()

        if event.type == pg.MOUSEWHEEL:
            if event.x:
                self.weapons_list.rotate(-1)
                self.weapon_selected = self.weapons_list[0]
                self.weapon_selector()

            elif event.y:
                self.weapons_list.rotate(-1)
                self.weapon_selected = self.weapons_list[0]
                self.weapon_selector()

    def recover_health(self):
        """"Health recovery"""
        if self.check_health_recovery_delay() and self.health < PLAYER_MAX_HEALTH:
            self.health += 1

    def check_health_recovery_delay(self):
        """Recovery delay for player"""
        time_now = pg.time.get_ticks()
        if time_now - self.time_prev > self.health_recovery_delay:
            self.time_prev = time_now
            return True

    def get_damage(self, damage):
        """Taking damage from NPC,
        and taking from armor as well
        the armor reduces the damage
        rendering the damage effect and sound
        checking if player is alive"""
        self.total_damage_received += damage
        if self.armor > 0:
            self.armor -= damage
            if self.armor < 0:
                self.armor = 0
        else:
            self.health -= damage
            if self.health <= 0:
                self.health = 0
            self.game.object_renderer.player_damage()
            self.game.sound.player_pain.play()
            self.check_game_over()

    def single_fire_event(self, event):
        """"Logic for shooting, when chainsaw selected to shoot until mouse button up,
        when shotgun selected shoot and animate,
        when minigun selected shoot like chainsaw
        and ammo restrictions"""
        if event.type == pg.MOUSEBUTTONDOWN:
            # shotgun
            if self.weapon_selected == "shotgun":
                if event.button == 1 and not self.shot and not self.game.weapon.reloading and self.shotgun_ammo > 0:
                    self.game.sound.shotgun.play()
                    self.shot = True
                    self.game.weapon.reloading = True  # for animation
                    self.shotgun_ammo -= 1
                    self.ammo_to_show -= 1
                    self.total_ammo_fired += 1
                    self.check_ammo()

            # chainsaw
            if self.weapon_selected == "chainsaw" and self.vruum_vruum_fuel > 0:
                if event.button == 1:
                    self.game.weapon.vroom_vroom = True  # for animation
                    self.shot = True
                    self.vruum_vruum_fuel_consumption = True
                    if self.shot:
                        self.game.sound.chainsaw_fire.play(-1)
                    if self.vruum_vruum_fuel <= 0:
                        self.game.weapon.vroom_vroom = False

            if self.weapon_selected == "minigun" and self.minigun_ammo > 0:

                if event.button == 1:
                    self.game.weapon.minigun_shoot = True  # for animation
                    self.shot = True
                    if self.shot:
                        self.minigun_ammo_fires = True
                        self.game.sound.minigun_fire.play(-1)
                    if self.minigun_ammo_fires <= 0:
                        self.game.weapon.minigun_shoot = False

        if event.type == pg.MOUSEBUTTONUP and event.button == 1:
            self.game.sound.chainsaw_fire.stop()
            self.game.sound.minigun_fire.stop()
            self.game.weapon.vroom_vroom = False
            self.game.weapon.minigun_shoot = False
            self.vruum_vruum_fuel_consumption = False
            self.minigun_ammo_fires = False
            self.shot = False

    def movement(self):
        """"Player movement. Fist we calculate the increments
        because we are on 2D using the functions of sin and cos
        Used for the player direction angle.
        And getting out to the menu.
        """
        self.mx, self.my = self.map_pos  # for minimap

        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        dx, dy = 0, 0
        speed = PLAYER_SPEED * self.game.delta_time
        speed_sin = speed * sin_a
        speed_cos = speed * cos_a

        keys = pg.key.get_pressed()

        if keys[pg.K_ESCAPE]:
            self.game.menu_trigger = True
            self.game.pause = True
            self.game.menu()

        if self.game.raycasting.show_raycast:
            if keys[pg.K_r]:
                self.game.raycasting.show_raycast = False
        else:
            if keys[pg.K_r]:
                self.game.raycasting.show_raycast = True

        if keys[settings.movement_dict[0]]:
            dx += speed_cos
            dy += speed_sin

        if keys[settings.movement_dict[1]]:
            dx += -speed_cos
            dy += -speed_sin

        if keys[settings.movement_dict[3]]:
            dx += speed_sin
            dy += -speed_cos

        if keys[settings.movement_dict[2]]:
            dx += -speed_sin
            dy += speed_cos

        self.wall_collision(dx, dy)

        self.angle %= math.tau

    def wall_check(self, x, y):
        """"Checking where are the walls in the map"""
        return (x, y) not in self.game.map.world_map

    def wall_collision(self, dx, dy):
        """"Check for wall collision"""
        scale = PLAYER_SIZE_SCALE / self.game.delta_time
        if self.wall_check(int(self.x + dx * scale), int(self.y)):
            self.x += dx
        if self.wall_check(int(self.x), int(self.y + dy * scale)):
            self.y += dy

    def mouse_control(self):
        """Mouse control with restriction look up and down"""
        self.mx, self.my = pg.mouse.get_pos()

        if self.mx < MOUSE_BORDER_LEFT or self.mx > MOUSE_BORDER_RIGHT:
            pg.mouse.set_pos([HALF_WIDTH, HALF_HEIGHT])
        if self.my < MOUSE_BORDER_DOWN or self.my > MOUSE_BORDER_UP:
            pg.mouse.set_pos([HALF_WIDTH, HALF_HEIGHT])

        self.rel, self.rel1 = pg.mouse.get_rel()
        self.rel = max(-MOUSE_MAX_REL, min(MOUSE_MAX_REL, self.rel))
        self.angle += self.rel * settings.MOUSE_SENSITIVITY * self.game.delta_time

        self.rel1 = max(-MOUSE_MAX_REL, min(MOUSE_MAX_REL, self.rel1))
        self.half_height -= self.rel1 * settings.MOUSE_SENSITIVITY * self.game.delta_time * 1000

        if self.half_height > HALF_HEIGHT * 1.5:
            self.half_height = HALF_HEIGHT * 1.5
        if self.half_height < HALF_HEIGHT * 0.5:
            self.half_height = HALF_HEIGHT * 0.5

    def update(self):
        self.score()
        self.movement()
        self.mouse_control()
        self.fuel_consumption_chainsaw()
        self.minigun_ammo_consumption()
        self.win_condition()

    def draw(self):
        """Drawing the player on the minimap"""
        pg.draw.circle(self.game.sc_map, 'green', (self.x * MINIMAP_TILE_SIZE, self.y * MINIMAP_TILE_SIZE), 3)

    @property
    def pos(self):
        """Getting the player position"""
        return self.x, self.y

    @property
    def map_pos(self):
        """Getting the tile possition the player is"""
        return int(self.x), int(self.y)
