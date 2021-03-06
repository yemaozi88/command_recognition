import sys
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
        sound.speak('stop')
    else:
        sound.speak('no valid command received')

if __name__ == '__main__':
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((default.host, default.port))
        s.listen()

        print('robot is waiting for the command...')
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            while True:
                command_ = conn.recv(1024)
                if not command_ == b'':
                    command = command_.decode('utf-8')
                    print('Received command: {}'.format(command))
                    execute_command(command)