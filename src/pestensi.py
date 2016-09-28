import requests

if __name__ == '__main__':
    print "You're supposed to run client.py\nThis is just a library of functions!"

API_URL   = 'http://meston.localhost/api/v1/'

class MestonException(Exception):
    pass

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
    return any(text == command['name'] or text.startswith(command['name'] + ' ') for command in commands)

def do_command(game, game_commands, user_command):
    """Tries to apply to command to Game"""
    
    # If user specified command with no additional text e.g. 'sleep'
    if any(game_command['name'] == user_command for game_command in game_commands):
        command = user_command
        text    = ''
    
    # User specified command with additional text e.g. 'grab mug'
    else: 
        possible_commands = []
        
        for game_command in game_commands:
            if user_command.startswith(game_command['name'] + ' '):
                possible_commands.append(game_command['name'])
        
        if len(possible_commands) == 0:
            raise ValueError('Text submitted does not start with a valid command')
        else:
            command = max(possible_commands, key=len) # Chooses the longest possible command
            text    = user_command[len(command) + 1:] # Gets text after command e.g. 'grab the mug' -> 'the mug'
    
    url    = game_url(game) + 'commands/' + command
    params = {'key' : game['key']}
    
    if text:
        params['text'] = text
    
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