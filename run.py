import os
import sys
import wave
import struct
from time import sleep
import socket

import pyaudio
import numpy as np
import tensorflow as tf

import defaultfiles as default
sys.path.append(default.tensorflow_examples_speech_commands_dir)
print(default.tensorflow_examples_speech_commands_dir)
from label_wav import load_graph, load_labels


class CommandRecognizer:
    def __init__(self, labels_txt, graph_pb):
        # load command labels.
        self.labels = load_labels(labels_txt)
        # load graph, which is stored in the default session
        load_graph(graph_pb)

        # pyaudio settings.
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
        #self._buff = queue.Queue()
        #self.closed = True

        # temporary files.
        self._wav_file     = 'input.wav'
        self._wav_file_16k = 'input_16k.wav'


    def show_audio_devices_info(self):
        """ Provides information regarding different audio devices available.
        reference:
            {porcupine}/demo/python/porcupine_demo.py
        """
        pa = pyaudio.PyAudio()
        for i in range(pa.get_device_count()):
            info = pa.get_device_info_by_index(i)
            #info = pa.get_device_info_by_host_api_device_index(i)
            print('{0:2}: {1}'.format(info['index'], info['name']))
        pa.terminate()


    def check_supported_sample_rate(self):
        import sounddevice as sd
        samplerates = 16000, 32000, 44100, 48000, 96000
        supported_samplerates = []
        for fs in samplerates:
            try:
                sd.check_output_settings(device=default.input_device_index, samplerate=fs)
            except Exception as e:
                #print(fs, e)
                pass
            else:
                supported_samplerates.append(fs)
        #print(supported_samplerates)
        return supported_samplerates


    def open_audio_stream(self, input_device_index):
        self._audio_interface = pyaudio.PyAudio()
        audio_stream = self._audio_interface.open(
            #rate=self._rate,
            rate=default.input_device_rate,
            channels=self._channels,
            format=self._format,
            input=True,
            frames_per_buffer=self._chunk,
            input_device_index=input_device_index)
        return audio_stream


    def record_audio(self, audio_stream, record_seconds):
        buf = []
        for i in range(0, int(default.input_device_rate / self._chunk * record_seconds)):
            buf_ = audio_stream.read(self._chunk, exception_on_overflow=False)
            buf.append(buf_)
        return buf


    def buf2pcm(self, buf):
        pcm = []
        for i in buf:
            pcm_ = struct.unpack_from("h" * self._chunk, i)
            pcm.extend(list(pcm_))
        return pcm


    def pcm2buf(self, pcm):
        return [struct.pack("h" * len(pcm), *pcm)]


    def VAD(self, pcm, frame_seconds=1, shift_seconds=0.01):
        frame_size = default.input_device_rate * self._channels * frame_seconds
        shift_size = int(frame_size * shift_seconds / frame_seconds)

        frame_start = 0
        rms = 0
        for i in range(0, len(pcm)-frame_size, shift_size):
            pcm_ = np.array(pcm[i:i+frame_size])
            if np.mean(pcm_**2) > rms:
                frame_start = i
                rms = np.mean(pcm_**2)

        return pcm[frame_start:frame_start+frame_size]


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
        waveFile.setsampwidth(self._audio_interface.get_sample_size(self._format))
        waveFile.setframerate(default.input_device_rate)
        waveFile.writeframes(b''.join(frames))
        waveFile.close()


    def downsample(self, input_wav, output_wav):
        os.system('sox ' + input_wav + ' -r ' + str(self._rate) + ' ' + output_wav)


    def label_buf(self, buf):
        # convert buf into pcm (amplitude).
        pcm  = self.buf2pcm(buf)

        # Voice Activity Detection.
        pcm2 = self.VAD(pcm)

        # Voice Activity is converted back to buf.
        buf2 = self.pcm2buf(pcm2)

        # write buf to a wav file.
        self.save_to_wav(buf2, self._wav_file)

        # downsampling.
        self.downsample(self._wav_file, self._wav_file_16k)

        # recognize the wav file.
        # TODO: save & load wav file may not needed.
        self.label_wav_file(self._wav_file_16k)


    def close(self, audio_stream):
        audio_stream.stop_stream()
        audio_stream.close()
        # self.closed = True
        # Signal the generator to terminate so that the client's
        # streaming_recognize method will not block the process termination.
        # self._buff.put(None)
        self._audio_interface.terminate()

        # remove temporary file.
        os.remove(self._wav_file)
        os.remove(self._wav_file_16k)



if __name__ == '__main__':
    cr = CommandRecognizer(default.labels_txt, default.graph_pb)

    # check sound device.
    print('[List of Input Devices]')
    cr.show_audio_devices_info()
    print('\n')
    print('>>> device {} is chosen as an input device.'.format(default.input_device_index))
    print('[Device Info]')
    pa = pyaudio.PyAudio()
    print(pa.get_device_info_by_index(default.input_device_index))

    audio_stream = cr.open_audio_stream(default.input_device_index)

    # listening command.
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((default.host, default.port))
        while audio_stream.is_active():
            print('==========')
            print('>>> listening...')
            buf = cr.record_audio(audio_stream, default.record_seconds)
            cr.save_to_wav(buf, 'sample.wav')
            cr.label_buf(buf)
            command = cr.labels[cr.ranking[0]]
            print('>>> recognized as {}'.format(command))

            print('sending command to the robot...')
            s.sendall(bytes(command, 'utf-8'))

        sleep(default.latency)

    # termination process.
    cr.close(audio_stream)