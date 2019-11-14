import sys
import argparse

import defaultfiles as default
sys.path.append(default.ev3dev_lang_python_dir)
import ev3dev2.motor as ev3
from ev3dev2.sound import Sound

steer = ev3.MoveSteering(ev3.OUTPUT_B, ev3.OUTPUT_C)
sound = Sound()

def execute_command(command):
    if command == 'go':
        steer.on_for_rotations(0, ev3.SpeedPercent(default.speed_percent), default.rotation)
    elif command == 'right':
        steer.on_for_rotations(100, ev3.SpeedPercent(default.speed_percent), default.rotation)
    elif command == 'left':
        steer.on_for_rotations(-100, ev3.SpeedPercent(default.speed_percent), default.rotation)
    elif command == 'down':
        steer.on_for_rotations(0, ev3.SpeedPercent(default.speed_percent), -default.rotation)
    elif command == 'stop':
        sound.speak('stop.').wait()
    else:
        sound.speak('no valid command received.').wait()
