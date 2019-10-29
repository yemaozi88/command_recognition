import time

import ev3dev.ev3 as ev3
import argparse

motorR = ev3.LargeMotor('outB')
motorL = ev3.LargeMotor('outC')

def execute_command(command):
    if command == 'go':
        ev3.Sound.speak('go forward.').wait()
        #motorR.run_to_rel_pos(position_sp=360, speed_sp=900, stop_action="hold")
        #motorL.run_to_rel_pos(position_sp=360, speed_sp=900, stop_action="hold")
    elif command == 'right':
        #ev3.Sound.speak('turn right.').wait()
        motorL.run_to_rel_pos(position_sp=360, speed_sp=900, stop_action="hold")
    elif command == 'left':
        #ev3.Sound.speak('turn left.').wait()
        motorR.run_to_rel_pos(position_sp=360, speed_sp=900, stop_action="hold")
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
