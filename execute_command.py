import ev3dev.ev3 as ev3
import argparse

def execute_command(command):
    if command == 'go':
        ev3.Sound.speak('go forward.').wait()
    elif command == 'right':
        ev3.Sound.speak('go right.').wait()
    elif command == 'left':
        ev3.Sound.speak('go left.').wait()
    elif command == 'down':
        ev3.Sound.speak('go back.').wait()
    elif command == 'stop':
        ev3.Sound.speak('stop.').wait()
    else:
        ev3.Sound.speak('no valid command received.').wait()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--command', type=str, default='', help='command received.')
    args = parser.parse_args()
    #print('command: ' + args.command)
    execute_command(args.command)
