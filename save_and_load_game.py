import json
import os
import settings


class SaveGame:
    def __init__(self, game):
        self.game = game
        self.menu_state = {}

    def take_game_data(self):
        self.data = {}
        self.data['map'] = self.game.map.mini_map
        self.data['npc_positions'] = self.game.object_handler.update()[0]
        self.data['npc_type'] = self.game.object_handler.update()[1]
        self.data['pick_sprite_positions'] = self.game.object_handler.update()[2]
        self.data['sprite_list'] = self.game.object_handler.update()[3]
        self.data['player_pos'] = self.game.player.pos
        self.data['player_health'] = self.game.player.health
        self.data['player_armor'] = self.game.player.armor
        self.data['player_kills'] = self.game.player.frag_counter
        self.data['minigun_ammo'] = self.game.player.minigun_ammo
        self.data['shotgun_ammo'] = self.game.player.shotgun_ammo
        self.data['fuel'] = self.game.player.vruum_vruum_fuel
        self.data['weapon_selected'] = self.game.player.weapon_selected
        self.data['kill_condition'] = self.game.player.npc_kill_condition
        self.data['max_npc_kill'] = self.game.player.max_npc_kills
        self.data['win_time'] = self.game.player.win_time
        self.data['timer'] = self.game.player.elapsed
        self.data['difficulty'] = settings.DIFFICULTY


    def save_menu_state(self, i, date):
        self.menu_state[i] = date
        if os.path.exists('save_load_game/menu_state/menu_state_save_file.txt'):
            with open(f'save_load_game/menu_state/menu_state_save_file.txt', "r") as file:
                data = json.load(file)
                if i in data:
                    print(i)
                    self.menu_state[i] = date
                for b in data:
                    if b != i:
                        self.menu_state[b] = data[b]

        with open(f'save_load_game/menu_state/menu_state_save_file.txt', "w") as file:
            json.dump(self.menu_state, file)

    def delete_save_game(self, i):
        if os.path.exists('save_load_game/menu_state/menu_state_save_file.txt'):
            with open(f'save_load_game/menu_state/menu_state_save_file.txt', "r") as file:
                data = json.load(file)
                if i in data:
                    del data[i]
        with open(f'save_load_game/menu_state/menu_state_save_file.txt', "w") as file:
            json.dump(data, file)

    def save_options(self, game_options_data):
        with open(f'save_load_game/options_save/game_options.txt', "w") as file:
            json.dump(game_options_data, file)

    def save_game_data(self, i):
        with open(f'save_load_game/saved_games/{i}.txt', "w") as file:
            json.dump(self.data, file)


class LoadGame:
    def __init__(self, game=None):
        self.game = game
        self.loaded_data = {}

        self.load_game = False

    def open_game_data(self, name):
        if os.path.exists(f'save_load_game/saved_games/{name}.txt'):
            self.load_game = True
            self.game.load_game_menu.load_game_menu_trigger = False
            self.game.menu_trigger = False
            self.game.pause = False

            with open(f'save_load_game/saved_games/{name}.txt', 'r') as file:
                self.loaded_data = json.load(file)

            self.game.new_game()
        else:
            print("NO save")

    def open_menu_saving_data(self):
        if os.path.exists('save_load_game/menu_state/menu_state_save_file.txt'):
            with open('save_load_game/menu_state/menu_state_save_file.txt', 'r') as file:
                savings_data = json.load(file)
            return savings_data
        return ""

    def load_options(self):
        if os.path.exists(f'save_load_game/options_save/game_options.txt'):
            with open(f'save_load_game/options_save/game_options.txt', 'r') as file:
                resolution_data = json.load(file)
                return resolution_data
