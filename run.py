import os
import sys

import tensorflow as tf

import defaultfiles as default
sys.path.append(default.tensorflow_examples_speech_commands_dir)

from label_wav import load_graph, load_labels


class CommandRecognizer:
    def __init__(self, labels_txt, graph_pb):
        # load command labels.
        self.labels = load_labels(labels_txt)
        # load graph, which is stored in the default session
        load_graph(graph_pb)

        # copied from temsorflow/examples/command_recognition/label_wav.py
        self.input_layer_name  = 'wav_data:0'
        self.output_layer_name = 'labels_softmax:0'

        # initialize variables.
        self.predictions = []
        self.ranking = []


    def predict_labels(self, wav_data):
        with tf.Session() as sess:
            # Feed the audio data as input to the graph.
            #   predictions  will contain a two-dimensional array, where one
            #   dimension represents the input image count, and the other has
            #   predictions per class
            softmax_tensor = sess.graph.get_tensor_by_name(self.output_layer_name)
            predictions, = sess.run(softmax_tensor, {self.input_layer_name: wav_data})
            self.predictions = predictions
            self.ranking = predictions.argsort()[:][::-1]
            return


    def label_wav_file(self, wav_file):
        if not wav_file or not tf.gfile.Exists(wav_file):
            tf.logging.fatal('wav file does not exist %s', wav_file)
        with open(wav_file, 'rb') as wav:
            wav_data = wav.read()
        self.predict_labels(wav_data)


if __name__ == '__main__':
    wav_file = r'/home/aki/Data/speech_dataset/left/a5d485dc_nohash_0.wav'

    cr = CommandRecognizer(default.labels_txt, default.graph_pb)
    cr.label_wav_file(wav_file)
    print('recognized as {}'.format(cr.labels[cr.ranking[0]]))
