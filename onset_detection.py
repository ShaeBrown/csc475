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
        infile = "./static/test_data/kismet-tv_on_0-24/kismet-tv_on_0-24_without_effects.mp3"

    input_audio, sample_rate = librosa.load(infile)
    od = OnsetDetect(input_audio, sample_rate)
    print(od.get_times())


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
                                          backtrack=True)

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
        for i, sample in enumerate(librosa.core.time_to_samples(self.od_result, self.sample_rate)):
            clip = self.input_audio[sample: sample + sample_width]
            if len(clip) > 0:
                clips.append(clip)
            else:
                self.od_result.remove(i)
        return clips

if __name__ == "__main__":
    main()
