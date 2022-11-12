import json
import os
import settings
from json.decoder import JSONDecodeError


class SaveGame:
    def __init__(self, game):
        self.game = game
        self.menu_state = {}

    def take_game_data(self):
        """
        Function for taking the game data

        Taking all the data that is needed to make a successful save

        :return: None
        :rtype: None
        """

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
        """
        Function fot save and load menus status. For showing the saved games.

        :param i: number
        :type i: int
        :param date: date of the file
        :type date: date
        :return: None
        :rtype: None
        """

        self.menu_state[i] = date
        if os.path.exists('save_load_game/menu_state/menu_state_save_file.txt'):
            with open(f'save_load_game/menu_state/menu_state_save_file.txt', "r") as file:
                data = json.load(file)
                if i in data:
                    self.menu_state[i] = date
                for b in data:
                    if b != i:
                        self.menu_state[b] = data[b]

        with open(f'save_load_game/menu_state/menu_state_save_file.txt', "w") as file:
            json.dump(self.menu_state, file)

    def delete_save_game(self, i):
        """
        Function for deleting the saved games

        :param i: number of game to delete
        :type i: int
        :return: None
        :rtype: None
        """

        if os.path.exists('save_load_game/menu_state/menu_state_save_file.txt'):
            with open(f'save_load_game/menu_state/menu_state_save_file.txt', "r") as file:
                data = json.load(file)
                if i in data:
                    del data[i]
        with open(f'save_load_game/menu_state/menu_state_save_file.txt', "w") as file:
            json.dump(data, file)

    def save_options(self, game_options_data):
        """
        Function for saving the game options

        :param game_options_data: dict of game options save
        :type game_options_data: dict
        :return: None
        :rtype: None
        """

        with open(f'save_load_game/options_save/game_options.txt', "w") as file:
            json.dump(game_options_data, file)

    def save_game_data(self, i):
        """
        Function for saving the games

        :param i:  saved game number
        :type i: int
        :return: None
        :rtype: None
        """

        with open(f'save_load_game/saved_games/{i}.txt', "w") as file:
            json.dump(self.data, file)


class LoadGame:
    """
    Class load game

    """
    def __init__(self, game=None):
        """
        Init method of class LoadGame

        :param game: Optional parameter
        :type game: self
        """

        self.game = game
        self.loaded_data = {}
        self.load_game = False

    def open_game_data(self, name):
        """
        Function for loading the game data

        :param name: name
        :type name: str
        :return: None
        :rtype: None
        """

        try:
            if os.path.exists(f'save_load_game/saved_games/{name}.txt'):
                self.load_game = True
                self.game.load_game_menu.load_game_menu_trigger = False
                self.game.menu_trigger = False
                self.game.pause = False

                with open(f'save_load_game/saved_games/{name}.txt', 'r') as file:
                    self.loaded_data = json.load(file)

                self.game.new_game()
            else:
                print("No save")
        except JSONDecodeError:
            self.load_game = False
            print("map file is corrupted")

    def open_menu_saving_data(self):
        """
        Function for loading the save and load menu if there are saved games


        :return: dict of saved menu state
        :rtype: dict
        """

        if os.path.exists('save_load_game/menu_state/menu_state_save_file.txt'):
            with open('save_load_game/menu_state/menu_state_save_file.txt', 'r') as file:
                savings_data = json.load(file)
            return savings_data
        return ""

    def load_options(self):
        """
        Function for loading the saved options

        :return: None
        :rtype: None
        """
        if os.path.exists(f'save_load_game/options_save/game_options.txt'):
            with open(f'save_load_game/options_save/game_options.txt', 'r') as file:
                resolution_data = json.load(file)
                return resolution_data
