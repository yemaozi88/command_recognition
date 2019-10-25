import os
import sys

tensorflow_examples_speech_commands_dir = r'home/aki/PycharmProjects/tensorflow/tensorflow/examples/speech_commands'
speech_command_train_dir = r'/home/aki/Data/speech_commands_train'
labels_txt = os.path.join(speech_command_train_dir, 'conv_labels.txt')
graph_pb   = os.path.join(speech_command_train_dir, 'my_frozen_graph.pb')
