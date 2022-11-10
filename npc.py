from sprite_object import *
from random import randint, random, choice
import numpy as np
import settings

try:
    from pathfinding.core.grid import Grid
    from pathfinding.finder.a_star import AStarFinder

    library = True
except ImportError:
    library = False


# TODO more comments

class NPC(AnimatedSprite):
    def __init__(self, game, path='resources/sprites/npc/soldier/0.png', pos=(10.5, 5.5),
                 scale=0.6, shift=0.38, animation_time=180, gone=False):
        super().__init__(game, path, pos, scale, shift, animation_time, gone)
        self.attack_images = self.get_images(self.path + '/attack')
        self.death_images = self.get_images(self.path + '/death')
        self.idle_images = self.get_images(self.path + '/idle')
        self.pain_images = self.get_images(self.path + '/pain')
        self.walk_images = self.get_images(self.path + '/walk')
        # check what is the difficulty if the game is loaded or not
        if self.game.load.load_game:
            self.difficulty = self.game.load.loaded_data['difficulty']
        else:
            self.difficulty = settings.DIFFICULTY
        if self.difficulty == "easy":
            self.attack_dist = randint(3, 6)
            self.speed = 0.03
            self.health = 100
            self.attack_damage = 20
            self.accuracy = 0.15
            self.drop = 0.5

        elif self.difficulty == "hard":
            self.attack_dist = randint(6, 10)
            self.speed = 0.03
            self.health = 150
            self.attack_damage = 40
            self.accuracy = 0.20
            self.drop = 0.1

        self.pos = pos
        self.size = 20
        self.drop_loop = True
        self.alive = True
        self.pain = False
        self.gone = gone
        self.ray_cast_value = False  # for shooting
        self.frame_counter = 0
        self.player_search_trigger = False
        self.game = game

    def update(self):
        """Update method"""
        self.check_animation_time()
        self.get_sprite()
        self.run_logic()

    def check_wall(self, x, y):
        """Helper for the collision returns the tiles that are occupied by walls"""
        return (x, y) not in self.game.map.world_map

    def check_wall_collision(self, dx, dy):
        """Checking for wall collision. Using the size of the npcs sprite"""
        if self.check_wall(int(self.x + dx * self.size), int(self.y)):
            self.x += dx
        if self.check_wall(int(self.x), int(self.y + dy * self.size)):
            self.y += dy

    def path_find(self, start, goal, mini_map):
        """Helper function for A star algorithm of the path finding library"""
        grid = Grid(matrix=mini_map, inverse=True)
        finder = AStarFinder()
        path, runs = finder.find_path(grid.node(start[0], start[1]), grid.node(goal[0], goal[1]), grid)
        return path[-1]

    def movement(self):
        """This function is responsible for the NPC movement if the pathfinding library is installed
        the movement is done by A star algorithm, else BFS"""
        if library:
            self.next_pos = self.path_find(self.map_pos, self.game.player.map_pos, self.game.map.mini_map)
        else:
            self.next_pos = self.game.path.get_path(self.map_pos, self.game.player.map_pos)

        next_x, next_y = self.next_pos

        if self.next_pos not in self.game.object_handler.npc_positions:
            # calculates the angle math.atan2 is measuring the clockwise angle. We are getting the next positions
            # then incrementing them 0.5 for not going into wall and subtracting the position that the npc is in.
            # calculate the increments and check if there is a wall or not.
            angle = math.atan2(next_y + 0.5 - self.y, next_x + 0.5 - self.x)
            dx = math.cos(angle) * self.speed
            dy = math.sin(angle) * self.speed
            self.check_wall_collision(dx, dy)

    def attack(self):
        """"Attacks the player with some random accuracy"""
        if self.animation_trigger:
            if random() < self.accuracy:
                self.game.player.get_damage(self.attack_damage)

    def loop_drop(self):
        """"Dropping loot logic"""
        if not self.alive and self.drop_loop:
            if random() < self.drop:
                loot_choice = choice(self.game.sprite_object.loot_type_list)
                self.game.object_handler.add_pick_sprites(SpriteObject(self.game, path=f'resources/sprites/collectables/{loot_choice}.png',
                                                                       pos=(self.map_pos[0] + 0.5, self.map_pos[1] + 0.5), scale=0.3, pick=True, type=loot_choice))
            self.drop_loop = False

    def animate_death(self):
        """Death animation with frame counter not to continue animate it"""
        if not self.alive:
            if self.game.global_trigger and self.frame_counter < len(self.death_images) - 1:
                self.death_images.rotate(-1)
                self.image = self.death_images[0]
                self.frame_counter += 1

    def animate_pain(self):
        """"Pain animation"""
        self.animate(self.pain_images)
        if self.animation_trigger:
            self.pain = False

    def check_hit_in_npc(self):
        """"Checking if we hit the NPC and checking the health of NPC to see if it is alive
        With this we can increase the difficulty
        Reduces the NPC health"""
        height_shoot = math.isclose(self.player.half_height, HALF_HEIGHT, rel_tol=0.7)
        check = HALF_WIDTH - self.sprite_half_width < self.screen_x < HALF_WIDTH + self.sprite_half_width and height_shoot
        if self.ray_cast_value and self.game.player.shot:
            # for shotgun
            if self.player.weapon_selected == "shotgun":
                if check:
                    # self.game.sound.npc_pain.play()
                    self.game.player.shot = False
                    self.pain = True
                    self.health -= self.game.weapon.damage
                    self.check_health()

            # for chainsaw
            if self.player.weapon_selected == "chainsaw":
                close_range = np.isclose(self.player.pos[1], self.map_pos[1], atol=1.6), np.isclose(self.player.pos[0], self.map_pos[0], atol=1.6)
                if check and close_range[0] and close_range[1] and self.game.weapon.vroom_vroom:
                    # self.game.sound.npc_pain.play()
                    self.game.player.shot = True
                    self.pain = True
                    self.health -= self.game.weapon.damage
                    self.check_health()

            if self.player.weapon_selected == "minigun":
                if check:
                    # self.game.sound.npc_pain.play()
                    self.game.player.shot = True
                    self.pain = True
                    self.health -= self.game.weapon.damage
                    self.check_health()

            self.game.player.total_damage_delt += self.game.weapon.damage

    def check_health(self):
        """"Function for checking health"""
        if self.health < 1:
            self.alive = False
            self.player.frag_counter += 1
            self.game.sound.npc_death.play()

    def run_logic(self):
        """"Simple run logic for the npc"""
        if self.alive:
            self.ray_cast_value = self.ray_cast_player_npc()
            self.check_hit_in_npc()
            if self.pain:
                self.animate_pain()

            elif self.ray_cast_value:
                self.player_search_trigger = True

                if self.dist < self.attack_dist:
                    self.animate(self.attack_images)
                    self.attack()
                else:
                    self.animate(self.walk_images)
                    self.movement()

            elif self.player_search_trigger:
                self.animate(self.walk_images)
                self.movement()

            else:
                self.animate(self.idle_images)
        else:
            self.loop_drop()
            self.animate_death()
            self.gone = True  # option for user to choose if True fast disappear if false no disappear of corpses

    @property
    def map_pos(self):
        return int(self.x), int(self.y)

    def ray_cast_player_npc(self):
        """Ray casting for npc to check if the player and the enemy are on site.
        Returns true else False remove bug when shooting through walls"""
        if self.game.player.map_pos == self.map_pos or self.game.player.map_pos == self.game.interactions.map_pos:
            return True

        wall_dist_v, wall_dist_h = 0, 0
        player_dist_v, player_dist_h = 0, 0

        ox, oy = self.game.player.pos
        x_map, y_map = self.game.player.map_pos

        ray_angle = self.theta

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
            if tile_hor == self.map_pos:
                player_dist_h = depth_hor
                break
            if tile_hor in self.game.map.world_map:
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
            if tile_vert == self.map_pos:
                player_dist_v = depth_vert
                break
            if tile_vert in self.game.map.world_map:
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


class SoldierNPC(NPC):
    def __init__(self, game, path='resources/sprites/npc/soldier/0.png', pos=(10.5, 5.5),
                 scale=0.6, shift=0.38, animation_time=180):
        super().__init__(game, path, pos, scale, shift, animation_time)


class CyberDemonNPC(NPC):
    def __init__(self, game, path='resources/sprites/npc/cyber_demon/0.png', pos=(11.5, 6.0),
                 scale=1.0, shift=0.04, animation_time=210):
        super().__init__(game, path, pos, scale, shift, animation_time)
        self.gone = False
        if self.difficulty == "easy":
            self.attack_dist = 5
            self.health = 250
            self.attack_damage = 60
            self.speed = 0.055
            self.accuracy = 0.25

        elif self.difficulty == "hard":
            self.attack_dist = 6
            self.health = 300
            self.attack_damage = 70
            self.speed = 0.04
            self.accuracy = 0.3
