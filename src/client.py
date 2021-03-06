from sys import argv, exit
import pestensi

print 'Pestensi - 10 Minutes to Meston Python Client v0.1'

if len(argv) == 3:
    print 'Loading game...'
    game = pestensi.load_game(argv[1], argv[2])
else:
    print 'Creating new game...'
    game = pestensi.new_game()

print 'Game created!'

# Command loop
while True:
    user_input = raw_input('Enter Command: ').strip()
    
    if user_input == 'exit':
        exit()
    else:
        messages = pestensi.do_command(game, user_input)
        
        for message in messages:
            print message
