import configparser
import curses
import os

# Directory of the python file
path = os.path.expanduser('~')

# Path to the config file
config_path = os.path.join(path, ".youtube-tui.config")
default_config = open(os.path.dirname(os.path.realpath(__file__)) + "/default-config", "r").read()
if not os.path.exists(config_path):
    open(config_path, "w").write(default_config)

def reset_bindings():
    """
    Resets the key bindings to the default one
    """
    open(config_path, "w").write(default_config)

def get_bindings():
    """
    Reads the config file and returns the bindings
    :return: A dictionary with all of the bindings
    """
    config = configparser.ConfigParser()
    config.read(config_path)

    return config["bindings"]


def convert_binding(binding: str):
    """
    Converts the binding to a key number that can be used with curses
    :param binding: The key binding in a single char string
    :return: An integer containing the key number. If the binding is invalid, returns -1
    """
    special_keys = {
        "TAB": 9,
        "ENTER": 10,
        "UP": 259,
        "DOWN": 258,
        "LEFT": 260,
        "RIGHT": 261
    }

    # If the binding is a special key,
    # convert it with the dictionary of special keys
    if binding in special_keys.keys():
        return special_keys.get(binding)

    # If the binding is only one character long,
    # convert the binding with the ord method
    if len(binding) == 1:
        return ord(binding)

    # If the binding is invalid,
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
        return convert_binding(shortcut)

def get_data_source():
    config = configparser.ConfigParser()
    config.read(config_path)
    return config['data']['source']

#get_data_source()

def get_api_key():
    config = configparser.ConfigParser()
    config.read(config_path)
    return config['api']['api-key'] 
#get_api_key()
