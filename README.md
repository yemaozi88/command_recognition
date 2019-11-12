These codes are designed to control a LEGO car with your voice. 
When you give command "right", "left", "go" and "down", the LEGO car will go right / left / forward / back.
Please see the [demo](https://www.youtube.com/watch?v=iytcUZL1_Pg).

[WARNING] _Currently the reaction speed is quite slow. The car only reacts 1 commands per 10 sec._

# Requisite
- [LEGO MINDSTORMS EV3](https://www.lego.com/en-us/product/lego-mindstorms-ev3-31313).
- USB Wi-Fi dongle. A LEGO MINDSTORMS EV3 Intelligent Brick does not have Wi-Fi adapter. 
- A microSD or microSDHC card (2GB or larger). microSDXC is not supported on the EV3. All cards larger than 32GB will not work with the EV3!
- A (Linux) computer with an adapter for the SD card, and a microphone input. You will need administrator user permissions on this computer.
The codes are tested on Python 3.6 on Ubuntu 18.04.

# How it works
1. You will talk to a microphone attached to the laptop. 
2. The input speech is recognized as one of "right", "left", "go", "down", "silence" or "unknown" by run.py on the laptop. 
3. The recognized command is sent to the robot car. 
4. The Lego car executes the command by execute_command.py.

# How to set up
## The laptop
1. Install the following packages if not exist - Tensorflow, pyaudio and paramiko.
1. Clone [Tensorflow](https://github.com/tensorflow/tensorflow).
1. Clone this repository.
1. Edit {command_recognition}/defaultfiles.py according to your environment.

## The Lego Car
The Lego Car only receives a command from the laptop. 
1. Following [the official instruction](https://www.ev3dev.org/docs/getting-started/), install ev3dev on the LEGO MINDSTORMS EV3 Intelligent Brick and set up network connection.
1. To check if above step is completed, please [connect to ev3dev with SSH](https://www.ev3dev.org/docs/tutorials/connecting-to-ev3dev-with-ssh/). 
1. Build a your favorite LEGO car. My husband made a [SUP3R car](https://www.smallrobots.it/introducing-the-sup3r-car/) for me. Be careful about the position of the WiFi dongle.
1. Clone this repository.
1. Edit {command_recognition}/defaultfiles.py according to your environment.

Now everything is ready. Please execute run.py on your laptop.
When you see "listening..." please give commands to the Lego car! 

# Please let us know your ideas.
This is a preliminary project.
We plan to improve the codes in future. 
If you have questions, opinions or ideas, please let us know (<428968@gmail.com>)! 
Your feedback will be appreciated. 
