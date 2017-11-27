from feature_extraction import FeatureExtraction
from onset_detection import OnsetDetect
from drum_annotation import DrumAnnotation
import librosa
import matplotlib.pyplot as plt
import numpy as np

debug_file = 'static/test_data/sargon-silenci_22-37/sargon-silenci_22-37_with_effects.mp3'

audio, sr = librosa.core.load(debug_file)


od = OnsetDetect(audio, sr)
onsets = od.get_times()
onset_clips = od.get_onset_clips(0.02)

#fe = FeatureExtraction(onset_clips, sr)

nyq = sr/2
X = FeatureExtraction(onset_clips, sr)\
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

annotator = DrumAnnotation("./trained_models/nov26.pkl")
predict = annotator.get_drum_prediction_times(audio, sr)
print(predict)
librosa.display.waveplot(audio, sr=sr)
plt.vlines(onsets, -audio.max(), audio.max(), color='r', alpha=0.9,
                   linestyle='--', label='Onsets')
plt.vlines(predict["Bass drum"], -audio.max(), audio.max(), color='b', alpha=0.5)
plt.vlines(predict["Hi-hat closed"], -audio.max(), audio.max(), color='g', alpha=0.5)
plt.vlines(predict["Hi-hat open"], -audio.max(), audio.max(), color='g', alpha=0.5)
plt.vlines(predict["Snare drum"], -audio.max(), audio.max(), color='y', alpha=0.5)

plt.show()