import os
import sys

tensorflow_examples_speech_commands_dir = r'home/aki/PycharmProjects/tensorflow/tensorflow/examples/speech_commands'
model_dir = r'model'
labels_txt = os.path.join(model_dir, 'conv_labels.txt')
graph_pb   = os.path.join(model_dir, 'my_frozen_graph.pb')

record_seconds = 3
input_device_index = 6
input_device_rate = 44100
latency = 1