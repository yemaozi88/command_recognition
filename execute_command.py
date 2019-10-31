import sys
import argparse

import defaultfiles as default
sys.path.append(default.ev3dev_lang_python_dir)
import ev3dev2.motor as ev3motor
import ev3dev2.sound as ev3sound

steer = ev3motor.MoveSteering(ev3motor.OUTPUT_B, ev3motor.OUTPUT_C)
def execute_command(command):
    if command == 'go':
        steer.on_for_rotations(0, ev3motor.SpeedPercent(default.speed_percent), default.rotation)
    elif command == 'right':
        steer.on_for_rotations(100, ev3motor.SpeedPercent(default.speed_percent), default.rotation)
    elif command == 'left':
        steer.on_for_rotations(-100, ev3motor.SpeedPercent(default.speed_percent), default.rotation)
    elif command == 'down':
        steer.on_for_rotations(0, ev3motor.SpeedPercent(default.speed_percent), -default.rotation)
    elif command == 'stop':
        ev3sound.speak('stop.').wait()
    else:
        ev3sound.speak('no valid command received.').wait()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--command', type=str, default='', help='command received.')
    args = parser.parse_args()
    #print('command: ' + args.command)
    execute_command(args.command)
