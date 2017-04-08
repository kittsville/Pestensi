import requests

if __name__ == '__main__':
    print "You're supposed to run client.py\nThis is just a library of functions!"

API_URL   = 'http://meston.localhost/api/v1/'
GAMES_URL = API_URL + 'games/'

class MestonException(Exception):
    pass

def new_game():
    """Creates and returns new 10 Minutes to Meston Game"""
    
    url = GAMES_URL + 'new/'
    
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
    
    return GAMES_URL + game_id + '/'

def do_command(game, user_command):
    """Tries to apply to command to Game"""
    
    url    = game_url(game) + 'state'
    params = {
        'key'     : game['key'],
        'command' : user_command,
    }
    
    response = requests.post(url, params)
    
    if response.status_code != 200:
        raise MestonException(response.text)
    
    return response.json()['messages']

def validate_game(game):
    game['id']
    game['seed']
    game['key']