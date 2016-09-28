import requests
from HTMLParser import HTMLParser
from sys import exit
from sys import argv
from re  import search

print 'Pestensi - 10 Minutes to Meston Python Client v0.1'

BASE_URL = 'http://meston.localhost/api/v1/'

def displayError(text):
    errorSearch = search('<span class="exception_message">(.*)</span>', text)
    
    if errorSearch:
        h     = HTMLParser()
        loc   = search('in <a title="(.*)" ondblclick', text).group(1)
        error = errorSearch.group(1)
        print loc
        print h.unescape(error)
    else:
        print text

def newGame():
    response = requests.post(BASE_URL + 'games/new')

    if response.status_code != 201:
        print 'Oh noes, something went wrong!'
        exit()

    game = response.json()
    gameId = str(game['id'])
    auth = {'key' : game['key']}
    
    print 'Game created with ID ' + gameId
    
    return gameId, auth

def doCommand(commandName, gameId, auth):
    response = requests.post(BASE_URL + 'games/' + gameId + '/commands/' + commandName, auth)
    
    if response.status_code != 200:
        print 'Oh noes, something went wrong!'
        displayError(response.text)
        exit()
    
    try:
        for message in response.json()['messages']:
            print message
    except ValueError:
        print 'Invalid response:'
        displayError(response.text)

if len(argv) == 3:
    gameId = argv[1]
    auth   = {'key' : argv[2]}
    print 'Loaded game with ID ' + gameId
else:
    gameId, auth = newGame()

while True:
    command = raw_input('Enter command: ')
    
    if command == 'exit':
        exit()
    else:
        doCommand(command, gameId, auth)