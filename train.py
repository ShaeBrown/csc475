import os.path
import re
import librosa
import numpy as np
from drum_annotation import DrumAnnotation
from onset_detection import OnsetDetect
from sklearn.model_selection import KFold
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn import metrics
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.externals import joblib
from tabulate import tabulate
import matplotlib.pyplot as plt

classes = ["Bass drum", "Hi-hat closed", "Hi-hat open", "Snare drum"]


def get_total_events(train_folder):
    total = 0
    for folder in os.listdir(train_folder):
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


def get_data():
    train_folder = "./static/test_data"
    X = []
    y = []
    total_matches = 0
    for folder in os.listdir(train_folder):
        for file in os.listdir(os.path.join(train_folder, folder)):
            if file.endswith(".wav") or file.endswith(".mp3"):
                print("Training on file {}".format(file))
                song, sr = librosa.core.load(os.path.join(train_folder, folder, file))
                onset = OnsetDetect(song, sr)
                f = DrumAnnotation.get_features(onset.get_onset_clips(0.02), sr)
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
    return np.array(X), y


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


def plot_feature_importance(X, y):
    forest = ExtraTreesClassifier(n_estimators=250,
                              random_state=0)
    forest.fit(X, y)
    importances = forest.feature_importances_
    std = np.std([tree.feature_importances_ for tree in forest.estimators_],
         axis=0)
    indices = np.argsort(importances)[::-1]
    features = np.array(['s_c', '0_rate', 'rms', 'RMSb1', 'RMSb2', 'RMSb3', 'c_f',
                         's_b', 's_k', 's_s', 's_r', 's_f', 'mfcc', 'RMSb1Rel', 'RMSb2Rel', 'RMSb3Rel', 'RMSbRelComb12',
                         'RMSbRelComb13', 'RMSbRelComb23'])
    # Print the feature ranking
    print("Feature ranking:")
    for f in range(X.shape[1]):
        print("%d. %s (%f)" % (f + 1, features[indices[f]], importances[indices[f]]))

    # Plot the feature importances of the forest
    plt.figure()
    plt.title("Feature importances")
    plt.bar(range(X.shape[1]), importances[indices],
           color="r", yerr=std[indices], align="center")
    plt.xticks(range(X.shape[1]), features[indices])
    plt.xlim([-1, X.shape[1]])
    plt.show()


def train():
    X, y = get_data()
    plot_feature_importance(X, y)
    clf = MLPClassifier()
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
