import os.path
import re
import librosa
import numpy as np
from feature_extraction import FeatureExtraction
from onset_detection import OnsetDetect
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import KFold
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn import metrics
from sklearn.externals import joblib
from tabulate import tabulate

classes = ["Bass drum", "Hi-hat closed", "Hi-hat open", "Snare drum"]

def get_total_events(train_folder):
    total = 0
    for folder in os.listdir(train_folder):
        for file in os.listdir(os.path.join(train_folder, folder)):
            if file.endswith(".txt"):
                with open(os.path.join(train_folder, folder, file)) as f:
                    for i, line in enumerate(f):
                        pass
                    total += i + 1
    return total


def get_truth(folder, time):
    truth = []
    time = round(time, 0)
    for c in classes:
        path = os.path.join(folder, c + ".txt")
        if os.path.isfile(path):
            with open(path, "r") as file:
                for line in file:
                    for t in re.findall("\d+\.\d+", line):
                        if round(float(t), 0) == time:
                            truth.append(c)
                            break
    return truth


def get_data():
    train_folder = "./static/test_data"
    X = []
    y = []
    for folder in os.listdir(train_folder):
        for file in os.listdir(os.path.join(train_folder, folder)):
            if file.endswith(".wav") or file.endswith(".mp3"):
                print("Training on file {}".format(file))
                song, sr = librosa.core.load(os.path.join(train_folder, folder, file))
                onset = OnsetDetect(song, sr)
                nyq = sr/2
                f = FeatureExtraction(onset.get_onset_clips(0.01), sr)\
                    .with_spectral_centroid()\
                    .with_zero_crossing_rate()\
                    .with_rms()\
                    .with_rms_of_filter(np.divide([49, 50], nyq), np.divide([0.01, 2000], nyq), 0.01, 62)\
                    .with_rms_of_filter(np.divide([200, 201], nyq), np.divide([1, 1300], nyq), 0.01, 20)\
                    .with_rms_of_filter(np.divide([5100, 16300], nyq), np.divide([65, 22000],nyq), 0.05, 60)\
                    .with_spectral_kurtosis()\
                    .with_spectral_skewness()\
                    .with_spectral_rolloff()\
                    .with_spectral_flatness()\
                    .with_mfcc()\
                    .get_feature_matrix()
                t = []
                total_matches = 0
                for time in onset.get_times():
                    truth = get_truth(os.path.join(train_folder, folder), time)
                    t.append(truth)
                    total_matches += len(truth)
                X.extend(f)
                y.extend(t)
                break
    y = MultiLabelBinarizer(classes=classes).fit_transform(y)
    print("Onset detection captured {0} out of {1} training data events".format(total_matches, \
                                                                                get_total_events(train_folder)))
    return np.array(X), y


def print_report(truth, pred, folds=10):
    print("Using cross validation with ", folds, "folds")
    print("Label ranking average precision: ",  metrics.label_ranking_average_precision_score(truth, pred))
    print("Coverage error", metrics.coverage_error(truth, pred))
    print("Ranking loss", metrics.label_ranking_loss(truth, pred))
    class_results = []
    for i, c in enumerate(classes):
        c_truth = np.array(truth)[:, i]
        c_pred = np.array(pred)[:, i]
        results = [c, "%.3f" % metrics.accuracy_score(c_truth, c_pred)]
        if np.sum(c_pred) == 0:
            results.append("n/a")
        else:
            results.append("%.3f" % metrics.precision_score(c_truth, c_pred))
        if np.sum(c_truth) == 0:
            results.append("n/a")
        else:
            results.append("%.3f" % metrics.recall_score(c_truth, c_pred))
        results.append(np.sum(c_truth))
        class_results.append(results)
    print(tabulate(class_results, headers=["Class", "Accuracy", "Precision", "Recall", "Samples"]))


def test_model(clf, X, y, folds=10):
    skf = KFold(n_splits=folds)
    truth = []
    pred = []
    for train_index, test_index in skf.split(X):
        X_train, X_test = X[train_index], X[test_index]
        y_train, y_test = y[train_index], y[test_index]
        clf.fit(X_train, y_train)
        p = clf.predict(X_test)
        truth.extend(y_test)
        pred.extend(p)
    return truth, pred


def train():
    X, y = get_data()
    clf = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(15,))
    truth, pred = test_model(clf, X, y)
    print_report(truth, pred)
    print("Would you like to export this trained model? [y/n]")
    export = input().lower().strip() == "y"
    if export:
        print("Enter file name")
        file = input()
        clf.fit(X, y)
        joblib.dump(clf, './trained_models/' + file + '.pkl')
        print("Exported model " + file + " in trained models")


if __name__ == '__main__':
    train()
