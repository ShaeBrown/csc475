import os.path
import re
import pickle
import librosa
import numpy as np
from drum_annotation import DrumAnnotation
from onset_detection import OnsetDetect
from sklearn.model_selection import cross_val_predict
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn import metrics
from sklearn.externals import joblib
from tabulate import tabulate

classes = ["Bass drum", "Hi-hat closed", "Hi-hat open", "Snare drum"]
X_file = "./static/test_data/X.p"
y_file = "./static/test_data/y.p"


def get_total_events(train_folder):
    total = 0
    for folder in os.listdir(train_folder):
        if os.path.isdir(os.path.join(train_folder, folder)):
            times = set()
            for file in os.listdir(os.path.join(train_folder, folder)):
                if file.endswith(".txt") and file.startswith(tuple(classes)):
                    with open(os.path.join(train_folder, folder, file)) as f:
                        for line in f:
                            for t in re.findall(r"\d+\.\d+", line):
                                times.add(t)
            total += len(times)
    return total


def get_truth(folder, time):
    truth = []
    for c in classes:
        path = os.path.join(folder, c + ".txt")
        if os.path.isfile(path):
            with open(path, "r") as file:
                for line in file:
                    for t in re.findall(r"\d+\.\d+", line):
                        if abs(float(t) - time) < 0.1:
                            truth.append(c)
                            break
    return truth


def load_data():
    train_folder = "./static/test_data"
    X = []
    y = []
    total_matches = 0
    for folder in os.listdir(train_folder):
        if os.path.isdir(os.path.join(train_folder, folder)):
            for file in os.listdir(os.path.join(train_folder, folder)):
                if file.endswith(".wav") or file.endswith(".mp3"):
                    print("Training on file {}".format(file))
                    song, sr = librosa.core.load(os.path.join(train_folder, folder, file))
                    onset = OnsetDetect(song, sr)
                    f = DrumAnnotation.get_features(onset.get_onset_clips(0.05), sr)
                    t = []
                    for time in onset.get_times():
                        truth = get_truth(os.path.join(train_folder, folder), time)
                        t.append(truth)
                        if len(truth) > 0:
                            total_matches += 1
                    X.extend(f)
                    y.extend(t)
    y = MultiLabelBinarizer(classes=classes).fit_transform(y)
    print("Onset detection captured {0} out of {1} training data events".format(total_matches,
                                                                                get_total_events(train_folder)))
    pickle.dump(np.array(X), open(X_file, "wb"))
    pickle.dump(y, open(y_file, "wb"))
    print("Exported data as pickle file")
    return np.array(X), y


def get_data():
    if os.path.exists(X_file) and os.path.exists(y_file):
        print("Would you like to re-preform onset detection and feature extraction? [y/n]")
        ans = input()
        if ans == "y":
            return load_data()
        else:
            X = pickle.load(open(X_file, "rb"))
            y = pickle.load(open(y_file, "rb"))
            print("Loaded data from pickle files")
            return np.array(X), np.array(y)
    else:
        return load_data()


def print_report(truth, pred, folds=10):
    print("Using cross validation with ", folds, "folds")
    print("Label ranking average precision: ", metrics.label_ranking_average_precision_score(truth, pred))
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


def train():
    X, y = get_data()
    clf = DecisionTreeClassifier()
    #plot_feature_importance(clf, X, y)
    pred = cross_val_predict(clf, X, y, cv=10)
    print_report(y, pred, folds=10)
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
