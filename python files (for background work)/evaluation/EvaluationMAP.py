

# This file creates the Mean Average Precisions shown in the Evaluation section of the report.


import QueryProcessor as query
import ANN
import DimensionReduction as DR

import numpy as np
import json
from enum import Enum
from functools import reduce
from random import shuffle

# this gets the Average Precision given a queryModel path and a list of classes in ascending order of distance.
def getAP(y_true, sortedClasses):
    tp       = 0   # True Positives so far. For each added k, the tp only changes by at most 1
    avg_prec = 0
    no_of_k  = len(sortedClasses)-1

    # This calculates: 1/(no_of_k) * sum over k: [precision for k]
    for k in range(1,no_of_k): # SUM OVER K
        y_pred = sortedClasses[k+1] # +1 to avoid the first: always you.
        if y_pred == y_true:
            tp += 1
        precision = tp / k     # TP / (TP+FP)
        avg_prec += precision
    return avg_prec / no_of_k


# returns for ANN the average precision over all values of k, for a given queryModel.
def classifySortedNeighboursANN(queryModel, features, annoyIndex):
    indices, distances = ANN.queryAnnoyIndex(annoyIndex, ANN.featureToVector(features[queryModel]), k=len(features))
    distances = [(d, ANN.getFileNameFromIndex(i, features)) for (i,d) in list(zip(indices, distances))]
    sortedDistances = sorted(distances, key=lambda tup: tup[0])
    sortedClasses = [query.getClassFromPath(i[1]) for i in sortedDistances]
    y_true = query.getClassFromPath(queryModel)
    return getAP(y_true, sortedClasses)


# returns for DR the average precision over all values of k, for a given queryModel.
def classifySortedNeighboursDR(queryModel, features, annoyIndex, X_embedded_10n):
    index = ANN.getIndexFromFileName(queryModel, features)
    indices, distances = ANN.queryAnnoyIndex(annoyIndex, X_embedded_10n[index], k=len(features)) # contains (index, distance)
    distances = [(d, ANN.getFileNameFromIndex(i, features)) for (i,d) in list(zip(indices, distances))]
    sortedDistances = sorted(distances, key=lambda tup: tup[0])
    sortedClasses = [query.getClassFromPath(i[1]) for i in sortedDistances]
    y_true = query.getClassFromPath(queryModel)
    return getAP(y_true, sortedClasses)


def classifySortedNeighbours(queryModel, features):
    queryVector = features[queryModel]
    distances = [(query.getDistance(queryVector, features[meshPath]), meshPath) for meshPath in features]
    sortedDistances = sorted(distances, key=lambda tup: tup[0])
    sortedClasses = [query.getClassFromPath(i[1]) for i in sortedDistances]
    y_true = query.getClassFromPath(queryModel)
    return getAP(y_true, sortedClasses)
# Then run this for all queryModels! And append the result in one big list.


class Alg(Enum):
    default = 1
    ann     = 2
    dr      = 3


# aggregates the average precisions for each of the possible 380 queryModels
def calculateMAP(features, alg=Alg.default):
    # for feature in features
    # set this to queryModel and run classify

    mean_avg_prec = 0
    no_of_models = len(features.keys())
    print(no_of_models, " models.")
    if alg == Alg.default:
        for queryModel in features.keys():  # SUM OVER MODELS
            avg_prec = classifySortedNeighbours(queryModel, features)
            mean_avg_prec += avg_prec
            # print(avg_prec, " average precision.")
    elif alg == Alg.ann:
        data = [ANN.featureToVector(feature) for feature in features.values()]
        annoyIndex = ANN.createAnnoyIndex(data)
        for queryModel in features.keys():  # SUM OVER MODELS
            avg_prec = classifySortedNeighboursANN(queryModel, features, annoyIndex)
            mean_avg_prec += avg_prec
            # print(avg_prec, " average precision.")
    elif alg == Alg.dr:
        allData = [ANN.featureToVector(features[filename]) for filename in features]
        data = np.array(allData)
        classes = [query.getClassFromPath(path) for path in features]
        dimensions = 2

        X_embedded_10n = DR.createTSNEObject(data, dimensions)
        annoyIndex = ANN.createAnnoyIndex(X_embedded_10n, dimensions)
        for queryModel in features.keys():  # SUM OVER MODELS
            avg_prec = classifySortedNeighboursDR(queryModel, features, annoyIndex, X_embedded_10n)
            mean_avg_prec += avg_prec
            # print(avg_prec, " average precision.")

    return mean_avg_prec / no_of_models


# returns the MAP
def main():
    with open("./database/normalized_features.json", "r") as read_content:
        features = json.load(read_content)

    alg = Alg.ann

    _map = calculateMAP(features, alg=alg)
    print("MeanAveragePrecision: ", _map)

if __name__ == "__main__":
    main()

# returns the MAP score for a system returning random models.
def getRandomMAP():
    runs = 100
    averagedMAP = 0
    for run in range(runs):
        mean_avg_prec = 0
        results = reduce(lambda x,y: x+y, [[i]*20 for i in range(19)]) # 20*[0] + 20*[1] + ... + 20*[19]
        for i in results:
            randomResults = reduce(lambda x,y: x+y, [[i]*20 for i in range(19)])
            shuffle(randomResults)
            avg_prec = getAP(i, randomResults)
            mean_avg_prec += avg_prec
        print(run, mean_avg_prec / len(results))
        averagedMAP += mean_avg_prec / len(results)
    print()
    return averagedMAP / runs


# Speed up trick: we can compute it for every k simultaniously.
# For a single model: compute for every k.

# Originally:  1/(no_of_k) * sum over all k: [1/(no_of_models) * sum over all models: [precision]]
# Which is decomposable as: 1/(no_of_k * no_of_models) * sum over all models: [sum over all k: [precision]]



#                           RESULTS



    # All of these are deterministic and consistent over many runs, except DR, which is shown here for 5 individual attempts
    # ~5 min:         Precision on default of    0.1193861667214884
    # ~5 sec:         Precision on ANN of        0.12660509068608447     WAT, HIGHER??
    # on average:     Precision of DR of         0.1270279169232986      WAT, THE HIGHEST?!

    # ~1 min + 5 sec: Precision of DR of         0.12812498448102028
    # ~1 min + 5 sec: Precision of DR of         0.12639746594344672
    # ~1 min + 5 sec: Precision of DR of         0.1266413316176563
    # ~1 min + 5 sec: Precision of DR of         0.12669472400049922
    # ~1 min + 5 sec: Precision of DR of         0.12728107857387053


    # To normalize between 0 and 1
    # we only conside 379 values for k, of which the first 19 show 1 optimally.
# best_aps = [1]*19 + [19/(19+i) for i in range(20, 380)] # best average precisions
# best_map = sum(best_aps)/len(best_aps)                  # best mean average precision
    # BEST:  0.16729131090269925
# worst_aps = [0]*(379-19) + [i/(19+i) for i in range(380-19, 380)] # worst average precisions
# worst_map = sum(worst_aps)/len(worst_aps)                         # worst mean average precision
    # WORST: 0.047682837427910414
    # NOW MAP EVERYTHING BETWEEN   0.047682837427910414   AND   0.16729131090269925

# max = 0.16729131090269925
# min = 0.047682837427910414
# def p(v):
#     return (v - min) / (max - min)
    # >>> p(0.1193861667214884)
    # 0.5994836921707863
    # >>> p(0.12660509068608447)
    # 0.6598383121644752
    # >>> p(0.1270279169232986)
    # 0.6633733981406643

    # That is, given that we have some pretty sucky classes, not at all bad!!
    # However, you should note that this score is only really bad if our desired results are somewhere at the end of the results.
    # As long as our results are somewhat close, this score will likely be quite decent.