import configparser
import curses
import os

# Directory of the python file
path = os.path.expanduser('~')

# Path to the config file
config_path = os.path.join(path, ".youtube-tui.config")


def reset_shortcuts():
    """
    Resets the shortcuts to the default one
    :return: A list of dictionary's containing the shortcuts
    """
    config = configparser.ConfigParser()
    config["shortcuts"] = {
        "switch_tabs": "TAB",
        "search": "ENTER",
        "select_video": "ENTER",
        "scroll_up": "UP",
        "scroll_down": "DOWN",
        "quit": "q"
    }

    config_file = open(config_path, "w")
    config.write(config_file)

    return config


def get_shortcuts():
    """
    Reads the config file and returns the shortcuts
    :return: A dictionary with all of the shortcuts
    """
    config = configparser.ConfigParser()
    config.read(config_path)

    return config["shortcuts"]


def convert_shortcut(shortcut: str):
    """
    Converts the shortcut to a key number that can be used with curses
    :param shortcut: The shortcut in a string
    :return: An integer containing the key number. If the shortcut is invalid, returns -1
    """
    special_keys = {
        "TAB": 9,
        "ENTER": 10,
        "UP": 259,
        "DOWN": 258,
        "LEFT": 260,
        "RIGHT": 261
    }

    # If the shortcut is a special key,
    # convert it with the dictionary of special keys
    if shortcut in special_keys.keys():
        return special_keys.get(shortcut)

    # If the shortcut is only one character long,
    # convert the shortcut with the ord method
    if len(shortcut) == 1:
        return ord(shortcut)

    # If the shortcut is invalid,
    # return -1
    return -1


def get_binding(name:str, config:dict):
    """
    Gets a key binding from a config dict and convert's it into a number
    :param name: The name of the binding
    :param config: The config dict read from the config file
    :return: An integer containing the key number
    """
    shortcut = config.get(name, None)
    if shortcut:
        return convert_shortcut(shortcut)
