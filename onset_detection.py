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

    print(OnsetDetect(infile))


class OnsetDetect(object):
    ''' Right now, I'm just using the librosa implementation
    In the future we can use this paper to implement, if we think it wil lgather better results
    http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.67.5843&rep=rep1&type=pdf
    '''
    def __init__(self, infile):
        input_audio, sample_rate = librosa.load(infile)
        self.input_audio = input_audio
        self.sample_rate = sample_rate
        self.od_result = librosa.onset.onset_detect(y=self.input_audio,
                                                    units='time',
                                                    sr=sample_rate,
                                                    backtrack=False)
        print(self.od_result)


if __name__ == "__main__":
    main()
