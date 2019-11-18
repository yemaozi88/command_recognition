import sys
import argparse
import socket

import ev3dev2.motor as ev3
from ev3dev2.sound import Sound

import defaultfiles as default
sys.path.append(default.ev3dev_lang_python_dir)

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

if __name__ == '__main__':
    #parser = argparse.ArgumentParser()
    #parser.add_argument(
    #    '--command', type=str, default='', help='command received.')
    #args = parser.parse_args()
    #print('command: ' + args.command)
    #execute_command(args.command)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((default.host, default.port))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            while True:
                command = conn.recv(1024)
                #if not command:
                #    break
                print(str(command))