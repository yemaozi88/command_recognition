import os

tensorflow_examples_speech_commands_dir = r'/home/aki/PycharmProjects/tensorflow/tensorflow/examples/speech_commands'
model_dir = r'model'
labels_txt = os.path.join(model_dir, 'conv_labels.txt')
graph_pb   = os.path.join(model_dir, 'my_frozen_graph.pb')

# recording.
record_seconds = 4
input_device_index = 5
input_device_rate = 44100
latency = 3

# ev3dev
ev3dev_lang_python_dir  = r'/home/robot/ev3dev_lang_python'
command_recognition_dir = r'/home/robot/command_recognition/tmp'
speed_percent = 50
rotation = -3

# socket
host = 'ev3dev.local'  # The server's hostname or IP address
port = 65432     # The port used by the server
