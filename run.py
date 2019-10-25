import os
import sys

import tensorflow as tf

import defaultfiles as default
sys.path.append(default.tensorflow_examples_speech_commands_dir)

from label_wav import load_graph, load_labels

# load command labels.
labels = load_labels(default.labels_txt)
# load graph, which is stored in the default session
load_graph(default.graph_pb)
input_layer_name  = 'wav_data:0'
output_layer_name = 'labels_softmax:0'
num_top_predictions = 3

def label_wav(wav):
    if not wav or not tf.gfile.Exists(wav):
        tf.logging.fatal('Audio file does not exist %s', wav)

    with open(wav, 'rb') as wav_file:
        wav_data = wav_file.read()

    with tf.Session() as sess:
        # Feed the audio data as input to the graph.
        #   predictions  will contain a two-dimensional array, where one
        #   dimension represents the input image count, and the other has
        #   predictions per class
        softmax_tensor = sess.graph.get_tensor_by_name(output_layer_name)
        predictions,   = sess.run(softmax_tensor, {input_layer_name: wav_data})

        # Sort to show labels in order of confidence
        top_k = predictions.argsort()[-num_top_predictions:][::-1]
        for node_id in top_k:
            human_string = labels[node_id]
            score = predictions[node_id]
            print('%s (score = %.5f)' % (human_string, score))


if __name__ == '__main__':
    #-graph = / home / aki / Data / my_frozen_graph.pb -
    # -labels = / home / aki / Data / speech_commands_train / conv_labels.txt -
    # -wav = / home / aki / Data / speech_dataset / left / a5d485dc_nohash_0.wav
    wav_file = r'/home/aki/Data/speech_dataset/left/a5d485dc_nohash_0.wav'
    label_wav(wav_file)
