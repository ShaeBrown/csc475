import librosa
import numpy as np
import sys
from onset_detection import OnsetDetect


class FeatureExtraction:
    def __init__(self, audio_clips, sr):
        self.audio_clips = audio_clips
        self.sr = sr
        self.features = []

    def with_zero_crossing_rate(self):
        crossing_rate = []
        for onset in self.audio_clips:
            crossings = librosa.feature.zero_crossing_rate(y=onset,
                                                           frame_length=len(onset))
            crossing_rate.append(crossings[0])
        self.features.append(crossing_rate)
        return self

    def with_spectral_centroid(self):
        spectral_centroid = []
        for onset in self.audio_clips:
            sc = librosa.feature.spectral_centroid(y=onset, sr=self.sr, hop_length=len(onset))
            spectral_centroid.append(sc[0][0])
        self.features.append(spectral_centroid)
        return self

    def get_feature_matrix(self):
        # TODO: normalize each row in a consistent way
        # transpose so each row is a onset time, and each column is a feature
        return np.transpose(np.array(self.features))

if __name__ == "__main__":
    infile = sys.argv[1]
    audio, sample_rate = librosa.load(infile)
    onset_clips = OnsetDetect(audio, sample_rate).get_onset_clips(0.001)
    X = FeatureExtraction(onset_clips, sample_rate)\
        .with_spectral_centroid().\
        with_zero_crossing_rate().\
        get_feature_matrix()

    print(X)






