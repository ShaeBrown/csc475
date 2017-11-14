#!/usr/bin/python3
import librosa
import sys
import numpy as np

FIXED_DELAY = 0.04 # 40 ms in s

def main():
    # if we need this to be more versatile can use argparse library
    if len(sys.argv) == 2:
        infile = sys.argv[1]
    else:
        #print("Usage: python onset_detection.py infile.wav")
        #sys.exit(0)
        infile = "../MASS/kismet-tv_on (indie-rock)/kismet-tv_on_0-24_without_effects.wav"
    input_audio, sample_rate = librosa.load(infile)
    print(OnsetDetect(input_audio, sample_rate).get_times())


class OnsetDetect(object):
    ''' Right now, I'm just using the librosa implementation
    In the future we can use this paper to implement, if we think it wil lgather better results
    http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.67.5843&rep=rep1&type=pdf
    '''
    def __init__(self, audio, sr):
        self.input_audio = audio
        self.sample_rate = sr
        self.od_result = librosa.onset.onset_detect(y=self.input_audio,
                                                    units='time',
                                                    sr=self.sample_rate,
                                                    backtrack=True)

    def get_times(self):
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

if __name__ == "__main__":
    main()
