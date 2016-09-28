import requests
from json_parser import json_parser
from re          import search
from HTMLParser  import HTMLParser

if __name__ == '__main__':
    print "You're supposed to run client.py\nThis is just a library of functions!"

API_URL   = 'http://meston.localhost/api/v1/'

class MestonException(Exception):
    pass

class CommandException(Exception):
    def __init__(self, command_name):
        self.command_name = command_name
    
    def __str__(self):
        return 'Game does not have command "{}"'.format(self.command_name)

def new_game():
    """Creates and returns new 10 Minutes to Meston Game"""
    
    url = games_url() + 'new/'
    
    response = requests.post(url)
    
    if response.status_code != 201:
        raise MestonException(response.text)
    
    game = response.json()
    
    validate_game(game)
    
    return game
    
def load_game(game_id, game_key):
    """Loads a game from its ID and key, if the game still exists"""
    url    = game_url(game_id)
    params = {'key' : game_key}

    response = requests.get(url, params)
    
    if response.status_code != 200:
        raise MestonException(response.text)
    
    game = response.json()
    
    validate_game(game)
    
    return game

def games_url():
    """Returns the URL to access all Games"""
    return API_URL + 'games/'

def game_url(arg):
    """Returns the URL to access a Game"""
    
    if isinstance(arg, str):
        game_id = arg
    elif isinstance(arg, int):
        game_id = str(arg)
    elif isinstance(arg, dict):
        game_id = str(arg['id'])
    else:
        raise ValueError("Must be given Game object or a Game's ID")
    
    return games_url() + game_id + '/'

def get_commands(game):
    """Gets currently available Commands to use in a Game"""
    url    = game_url(game) + 'commands/'
    params = {'key' : game['key']}
    
    response = requests.get(url, params)
    
    if response.status_code != 200:
        raise MestonException(response.text)
    
    commands = response.json()
    
    # Verifies commands contain necessary properties
    for command in commands:
        command['game_id']
        command['name']
        command['id']
    
    return commands

def is_command(commands, text):
    """Checks if the given text is a valid command for the current 10MtM game"""
    return any(command['name'] == text for command in commands)

def do_command(game, command):
    """Tries to apply to command to Game"""
    url    = game_url(game) + 'commands/' + command
    params = {'key' : game['key']}
    
    response = requests.post(url, params)
    
    if response.status_code != 200:
        raise MestonException(response.text)
    
    json_response = response.json()
    
    commands = json_response['commands']
    
    return commands, json_response['messages']

def validate_game(game):
    game['id']
    game['seed']
    game['key']