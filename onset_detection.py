#!/usr/bin/python3
import librosa
import librosa.display
import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks_cwt

FIXED_DELAY = 0.04 # 40 ms in s

def main():
    # if we need this to be more versatile can use argparse library
    if len(sys.argv) == 2:
        infile = sys.argv[1]
    else:
        infile = "../MASS/kismet-tv_on (indie-rock)/kismet-tv_on_0-24_without_effects.wav"

    input_audio, sample_rate = librosa.load(infile)
    od = OnsetDetect(input_audio, sample_rate)
    print(od.get_times())
    od.visualize()


class OnsetDetect(object):
    ''' Right now, I'm just using the librosa implementation
    In the future we can use this paper to implement, if we think it wil lgather better results
    http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.67.5843&rep=rep1&type=pdf
    '''
    def __init__(self, audio, sr):
        self.input_audio = audio
        self.sample_rate = sr
        self.od_result = self._run_detection()

    def _run_detection(self):
        ''' Perform acual detection here '''
        onset_env = librosa.onset.onset_strength(y=self.input_audio,
                                                 sr=self.sample_rate,
                                                 aggregate=np.mean)
        return librosa.onset.onset_detect(onset_envelope=onset_env,
                                          units='time',
                                          sr=self.sample_rate,
                                          backtrack=False)

    def get_times(self):
        ''' Returns the onset detection peaks as a 1-d array (in seconds)'''
        return self.od_result

    def get_onset_clips(self, duration):
        """
        Get audio clips in length duration (seconds) following detected onsets
        :param duration: length of clip in seconds
        :return: array of audio clips
        """
        sample_width = int(librosa.core.time_to_samples([duration], self.sample_rate)[0])
        clips = []
        for sample in librosa.core.time_to_samples(self.od_result):
            clips.append(self.input_audio[sample: sample + sample_width])
        return clips

    def visualize(self):
        ''' Show the detected events in a pyplot window '''
        o_env = librosa.onset.onset_strength(self.input_audio, sr=self.sample_rate)
        times = librosa.frames_to_time(np.arange(len(o_env)), sr=self.sample_rate)

        event_frames = librosa.core.time_to_frames(self.get_times(), sr=self.sample_rate)
        D = librosa.stft(self.input_audio)

        plt.figure()
        ax1 = plt.subplot(2, 1, 1)
        librosa.display.specshow(librosa.amplitude_to_db(D, ref=np.max),
                                 x_axis='time', y_axis='log')
        plt.title('Power spectrogram')
        plt.subplot(2, 1, 2, sharex=ax1)

        plt.plot(times, o_env, label='Onset strength')
        plt.vlines(times[event_frames], 0, o_env.max(), color='r', alpha=0.9,
                   linestyle='--', label='Onsets')

        plt.axis('tight')
        plt.legend(frameon=True, framealpha=0.75)

        plt.show()

if __name__ == "__main__":
    main()
