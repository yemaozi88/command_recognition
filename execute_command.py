import ev3dev.ev3 as ev3
import argparse

def execute_command(command):
    if command == 'test':
        ev3.Sound.speak('test command.').wait()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--command', type=str, default='', help='command received.')
    args = parser.parse_args()
    print('command: '+args.command)
