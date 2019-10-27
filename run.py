import os
import sys
import struct
import wave
import tempfile

import tensorflow as tf
import pyaudio
from six.moves import queue
import matplotlib.pyplot as plt
import numpy as np

import defaultfiles as default
sys.path.append(default.tensorflow_examples_speech_commands_dir)

from label_wav import load_graph, load_labels


class CommandRecognizer:
    def __init__(self, labels_txt, graph_pb):
        # load command labels.
        self.labels = load_labels(labels_txt)
        # load graph, which is stored in the default session
        load_graph(graph_pb)

        # pyaudio settings.

        #RECORD_SECONDS = 3
        #INPUT_DEVICE_INDEX = 7

        self._rate     = 16000
        self._chunk    = 1024
        self._format   = pyaudio.paInt16
        self._channels = 1

        # copied from temsorflow/examples/command_recognition/label_wav.py
        self.input_layer_name  = 'wav_data:0'
        self.output_layer_name = 'labels_softmax:0'

        # initialize variables.
        self.predictions = []
        self.ranking = []

        # Create a thread-safe buffer of audio data
        self._buff = queue.Queue()
        self.closed = True


    def show_audio_devices_info(self):
        """ Provides information regarding different audio devices available.
        reference:
            {porcupine}/demo/python/porcupine_demo.py
        """
        pa = pyaudio.PyAudio()
        for i in range(pa.get_device_count()):
            info = pa.get_device_info_by_index(i)
            print('{0:2}: {1}'.format(info['index'], info['name']))
        pa.terminate()


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
        else:
            with open(wav_file, 'rb') as wav:
                wav_data = wav.read()
            self.predict_labels(wav_data)


    def save_to_wav(self, frames, wav_file):
        waveFile = wave.open(wav_file, 'wb')
        waveFile.setnchannels(self._channels)
        waveFile.setsampwidth(pa.get_sample_size(self._format))
        waveFile.setframerate(self._rate)
        waveFile.writeframes(b''.join(frames))
        waveFile.close()


    def buf2pcm(self, buf):
        pcm = []
        for i in buf:
            pcm_ = struct.unpack_from("h" * CHUNK, i)
            pcm.extend(list(pcm_))
        return pcm


    def pcm2buf(self, pcm):
        return [struct.pack("h" * len(pcm), *pcm)]


    def VAD(self, pcm, frame_seconds=1, shift_seconds=0.01):
        frame_size = self._rate * self._channels * frame_seconds
        shift_size = int(frame_size * shift_seconds / frame_seconds)

        frame_start = 0
        rms = 0
        for i in range(0, len(pcm)-frame_size, shift_size):
            pcm_ = np.array(pcm[i:i+frame_size])
            if np.mean(pcm_**2) > rms:
                frame_start = i

        return pcm[frame_start:frame_start+frame_size]


    def label_buf(self, buf):
        # convert buf into pcm (amplitude).
        pcm  = self.buf2pcm(buf)

        # Voice Activity Detection.
        pcm2 = self.VAD(pcm)

        # Voice Activity is converted back to buf.
        buf2 = self.pcm2buf(pcm2)

        # write buf to a wav file.
        wav_file = tempfile.NamedTemporaryFile(delete=False)
        wav_file.close()
        self.save_to_wav(buf2, wav_file.name)

        # recognize the wav file.
        # TODO: save & load wav file may not needed.
        self.label_wav_file(wav_file.name)

        # remove temporary file.
        os.remove(wav_file.name)


class MicrophoneStream(object):

    def __enter__(self):
        self._audio_interface = pyaudio.PyAudio()
        self._audio_stream = self._audio_interface.open(
            format=pyaudio.paInt16,
            # The API currently only supports 1-channel (mono) audio
            # https://goo.gl/z757pE
            channels=1, rate=self._rate,
            input=True, frames_per_buffer=self._chunk,
            # Run the audio stream asynchronously to fill the buffer object.
            # This is necessary so that the input device's buffer doesn't
            # overflow while the calling thread makes network requests, etc.
            stream_callback=self._fill_buffer,
        )

        self.closed = False

        return self

    def __exit__(self, type, value, traceback):
        self._audio_stream.stop_stream()
        self._audio_stream.close()
        self.closed = True
        # Signal the generator to terminate so that the client's
        # streaming_recognize method will not block the process termination.
        self._buff.put(None)
        self._audio_interface.terminate()

    def _fill_buffer(self, in_data, frame_count, time_info, status_flags):
        """Continuously collect data from the audio stream, into the buffer."""
        self._buff.put(in_data)
        return None, pyaudio.paContinue

    def generator(self):
        while not self.closed:
            # Use a blocking get() to ensure there's at least one chunk of
            # data, and stop iteration if the chunk is None, indicating the
            # end of the audio stream.
            chunk = self._buff.get()
            if chunk is None:
                return
            data = [chunk]

            # Now consume whatever other data's still buffered.
            while True:
                try:
                    chunk = self._buff.get(block=False)
                    if chunk is None:
                        return
                    data.append(chunk)
                except queue.Empty:
                    break

            yield b''.join(data)


if __name__ == '__main__':
    cr = CommandRecognizer(default.labels_txt, default.graph_pb)

    RATE = 16000
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    RECORD_SECONDS = 2
    INPUT_DEVICE_INDEX = 6
    CHANNELS = 1

    pa = pyaudio.PyAudio()
    stream = pa.open(
        rate=RATE,
        channels=CHANNELS,
        format=FORMAT,
        input=True,
        frames_per_buffer=CHUNK,
        input_device_index=INPUT_DEVICE_INDEX)

    print('recording...')

    #while stream.is_active():
    buf = []
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        buf_ = stream.read(CHUNK)
        buf.append(buf_)

    stream.stop_stream()
    stream.close()
    pa.terminate()

    cr.label_buf(buf)
    print('recognized as {}'.format(cr.labels[cr.ranking[0]]))
