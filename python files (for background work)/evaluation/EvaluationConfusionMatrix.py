

# This file creates the Confusion-Matrices shown in the Evaluation section of the report.


import QueryProcessor as query
import ANN
import DimensionReduction as DR

from sklearn.metrics import confusion_matrix
import numpy as np
import seaborn as sn
import pandas as pd
import matplotlib.pyplot as plt
import json
from enum import Enum


# returns for ANN the expected predictions [class labels] (y_true) and obtained predictions (y_pred) for a given queryModel and k.
def classifySortedNeighboursANN(queryModel, features, k, annoyIndex):
    indices, distances = ANN.queryAnnoyIndex(annoyIndex, ANN.featureToVector(features[queryModel]), k=k+1)

    y_true = [query.getClassFromPath(queryModel)] * k
    y_pred = []
    for index, distance in list(zip(indices, distances))[1:1 + k]: # to avoid the first: always you.
        guess = query.getClassFromPath(ANN.getFileNameFromIndex(index, features))
        y_pred.append(guess)

    return y_true, y_pred


# returns for DR the expected predictions [class labels] (y_true) and obtained predictions (y_pred) for a given queryModel and k.
def classifySortedNeighboursDR(queryModel, features, k, annoyIndex, X_embedded_10n):
    index = ANN.getIndexFromFileName(queryModel, features)
    indices, distances = ANN.queryAnnoyIndex(annoyIndex, X_embedded_10n[index], k=k+1)

    y_true = [query.getClassFromPath(queryModel)] * k
    y_pred = []
    for index, distance in list(zip(indices, distances))[1:1 + k]: # to avoid the first: always you.
        guess = query.getClassFromPath(ANN.getFileNameFromIndex(index, features))
        y_pred.append(guess)

    return y_true, y_pred


# returns for Default the expected predictions [class labels] (y_true) and obtained predictions (y_pred) for a given queryModel and k.
def classifySortedNeighbours(queryModel, features, k):
    queryVector = features[queryModel]
    distances = [(query.getDistance(queryVector, features[meshPath]), meshPath) for meshPath in features]
    sortedDistances = sorted(distances, key=lambda tup: tup[0])

    y_true = [query.getClassFromPath(queryModel)] * k
    y_pred = []
    for distance, path in sortedDistances[1:1 + k]: # to avoid the first: always you.
        guess = query.getClassFromPath(path)
        y_pred.append(guess)

    return y_true, y_pred

# Then run this for all queryModels! And append the result in one big list.

class Alg(Enum):
    default = 1
    ann     = 2
    dr      = 3


# aggregates all predictions for all possible 380 queryModels into two big lists and returns those.
def calculateConfusionMatrix(features, k=10, alg=Alg.default):
    # for feature in features
    # set this to queryModel and run classify
    y_true = []
    y_pred = []

    if alg == Alg.default:
        for queryModel in features.keys():
            yt, yp = classifySortedNeighbours(queryModel, features, k)
            y_true.append(yt)
            y_pred.append(yp)
    elif alg == Alg.ann:
        data = [ANN.featureToVector(feature) for feature in features.values()]
        annoyIndex = ANN.createAnnoyIndex(data)
        for queryModel in features.keys():
            yt, yp = classifySortedNeighboursANN(queryModel, features, k, annoyIndex)
            y_true.append(yt)
            y_pred.append(yp)
    elif alg == Alg.dr:
        allData = [ANN.featureToVector(features[filename]) for filename in features]
        data = np.array(allData)
        classes = [query.getClassFromPath(path) for path in features]
        dimensions = 2
        X_embedded_10n = DR.createTSNEObject(data, dimensions)
        annoyIndex = ANN.createAnnoyIndex(X_embedded_10n, dimensions)
        for queryModel in features.keys():
            yt, yp = classifySortedNeighboursDR(queryModel, features, k, annoyIndex, X_embedded_10n)
            y_true.append(yt)
            y_pred.append(yp)

    y_true = [i for sublist in y_true for i in sublist] # to make it one big list and not a list of lists
    y_pred = [i for sublist in y_pred for i in sublist]
    return y_true, y_pred


# Actually prints the Confusion Matrix
def main():
    with open("./database/normalized_features.json", "r") as read_content:
        features = json.load(read_content)

    alg = Alg.default
    k   = 5

    y_true, y_pred = calculateConfusionMatrix(features, k=k, alg=alg)
    labels = []
    [labels.append(x) for x in y_true if x not in labels]
    array = confusion_matrix(y_true, y_pred, labels=labels) # preferably y_true if all occur
    s = sum(array[0]) # the index doesn't matter - all sum the same == 20*k
    normalized_array = [[round(c*100/s) for c in row] for row in array]

    # this, to give a percentage or "acuracy". Is what Alex wanted, makes sense too - easier to interpret
    # note: only the rows or y-axis (y_real) sum to a consistent number.
    # The x-axis (y_pred) can sum to any number, as we can predict any class as much as desired

    labelsize = 0.6
    size = 8

    x_dim = len(normalized_array)
    df_cm = pd.DataFrame(normalized_array, range(x_dim), range(x_dim))
    sn.set(font_scale=labelsize) # for label size
    sn.heatmap(df_cm, cmap="Blues", annot=True, annot_kws={"size": size},fmt='d', xticklabels=labels, yticklabels=labels)

    for row in df_cm.values.tolist():
        print(f"[{ ', '.join(list([str(r) for r in row])) }],")
    print(labels)
    plt.xlabel("Predicted class")
    plt.ylabel("Queried class")

    plt.show()

    
if __name__ == "__main__":
    main()