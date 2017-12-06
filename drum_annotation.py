from sklearn.externals import joblib
import numpy as np
from onset_detection import OnsetDetect
from feature_extraction import FeatureExtraction
import librosa

classes = ["Bass drum", "Hi-hat closed", "Hi-hat open", "Snare drum"]


class DrumAnnotation:
    def __init__(self, trained_model):
        self.clf = joblib.load(trained_model)

    def get_drum_prediction_times(self, song, sr):
        onset = OnsetDetect(song, sr)
        X = self.get_features(onset.get_onset_clips(0.05), sr)
        y = self.clf.predict(X)
        return self.__get_class_times(onset.get_times(), y)

    @staticmethod
    def get_features(onset_clips, sr):
        nyq = sr / 2
        return FeatureExtraction(onset_clips, sr) \
            .with_spectral_centroid() \
            .with_zero_crossing_rate() \
            .with_rms() \
            .with_rms_of_filter(np.divide([49, 50], nyq), np.divide([0.01, 2000], nyq), 0.01, 62)\
            .with_rms_of_filter(np.divide([200, 201], nyq), np.divide([1, 1300], nyq), 0.01, 20)\
            .with_rms_of_filter(np.divide([5100, 16300], nyq), np.divide([65, 22000], nyq), 0.05, 60)\
            .with_crest_factor() \
            .with_spectral_bandwith() \
            .with_spectral_kurtosis() \
            .with_spectral_skewness() \
            .with_spectral_rolloff() \
            .with_spectral_flatness() \
            .with_mfcc() \
            .with_row_operation(3, 2, np.subtract) \
            .with_row_operation(4, 2, np.subtract) \
            .with_row_operation(5, 2, np.subtract) \
            .with_row_operation(3, 4, np.subtract) \
            .with_row_operation(3, 5, np.subtract) \
            .with_row_operation(4, 5, np.subtract) \
            .get_feature_matrix()

    @staticmethod
    def __get_class_times(times, y):
        class_times = {}
        for i, drum_class in enumerate(classes):
            class_times[drum_class] = times[np.nonzero(y[:, i])].tolist()
        return class_times

if __name__ == '__main__':
    D = DrumAnnotation('trained_models/nov26.pkl')
    song, sr = librosa.core.load('static/test_data/fort_minor-remember_the_name_127-145/fort_minor-remember_the_name_127-145_with_effects.wav')
    print(D.get_drum_prediction_times(song, sr))