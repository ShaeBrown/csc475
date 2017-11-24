import librosa
import numpy as np
import sys
from scipy import signal
from scipy import stats
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
            crossing_rate.append(crossings[0][0])
        self.features.append(crossing_rate)
        return self

    def with_spectral_centroid(self):
        spectral_centroid = []
        for onset in self.audio_clips:
            sc = librosa.feature.spectral_centroid(y=onset, sr=self.sr, hop_length=len(onset))
            spectral_centroid.append(sc[0][0])
        self.features.append(spectral_centroid)
        return self

    def with_rms(self):
        rms = []
        for onset in self.audio_clips:
            r = librosa.feature.rmse(y=onset, frame_length=len(onset))
            rms.append(r[0][0])
        self.features.append(rms)
        return self

    def with_rms_of_filter(self, wp, ws, gpass, gstop):
        n, wn = signal.buttord(wp, ws, gpass, gstop)
        b, a = signal.butter(n, wn[0])
        rms = []
        for onset in self.audio_clips:
            y = signal.lfilter(b, a, onset)
            r = librosa.feature.rmse(y=y, frame_length=len(onset))
            rms.append(r[0][0])
        self.features.append(rms)
        return self

    def with_crest_factor(self):
        crest = []
        for onset in self.audio_clips:
            max_abs = np.max(np.abs(onset))
            r = librosa.feature.rmse(y=onset, frame_length=len(onset))
            crest.append(max_abs/r[0])
        self.features.append(crest)
        return self

    def with_spectral_kurtosis(self):
        kurtosis = []
        for onset in self.audio_clips:
            ps = np.abs(np.fft.fft(onset)) ** 2
            k = stats.kurtosis(ps, fisher=True)
            kurtosis.append(k)
        self.features.append(kurtosis)
        return self

    def with_spectral_skewness(self):
        skewness = []
        for onset in self.audio_clips:
            ps = np.abs(np.fft.fft(onset)) ** 2
            s = stats.skew(ps)
            skewness.append(s)
        self.features.append(skewness)
        return self

    def with_spectral_rolloff(self):
        rolloff = []
        for onset in self.audio_clips:
            roll = librosa.feature.spectral_rolloff(y=onset, sr=self.sr, hop_length=len(onset))
            rolloff.append(roll[0][0])
        self.features.append(rolloff)
        return self

    def with_spectral_flatness(self):
        flatness = []
        for onset in self.audio_clips:
            ps = np.abs(np.fft.fft(onset)) ** 2
            f = stats.gmean(ps)/np.mean(ps)
            flatness.append(f)
        self.features.append(flatness)
        return self

    def with_mfcc(self):
        mfcc = []
        for onset in self.audio_clips:
            c = librosa.feature.mfcc(y=onset, sr=self.sr, n_mfcc=1)
            mfcc.append(c[0][0])
        self.features.append(mfcc)
        return self

    def get_feature_matrix(self):
        return np.transpose(np.array(self.features))

if __name__ == "__main__":
    infile = sys.argv[1]
    audio, sample_rate = librosa.load(infile)
    onset_clips = OnsetDetect(audio, sample_rate).get_onset_clips(0.001)
    nyq = sample_rate/2
    X = FeatureExtraction(onset_clips, sample_rate)\
        .with_spectral_centroid()\
        .with_zero_crossing_rate()\
        .with_rms()\
        .with_rms_of_filter(np.divide([49, 50], nyq), np.divide([0.01, 2000], nyq), 0.01, 62)\
        .with_rms_of_filter(np.divide([200, 201], nyq), np.divide([1, 1300], nyq), 0.01, 20)\
        .with_rms_of_filter(np.divide([5100, 16300], nyq), np.divide([65, 22000], nyq), 0.05, 60)\
        .with_spectral_kurtosis()\
        .with_spectral_skewness()\
        .with_spectral_rolloff()\
        .with_spectral_flatness()\
        .with_mfcc()\
        .get_feature_matrix()
    print(X)






