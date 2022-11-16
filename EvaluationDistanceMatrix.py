

# This file creates the Distance-Matrices shown in the Evaluation section of the report.


import QueryProcessor as query

import numpy as np
import seaborn as sn
import pandas as pd
import matplotlib.pyplot as plt
import json
import os.path


# returns the distances from the queryModel to each other model (actually only to the subset of models we look at).
def distanceSortedNeighbours(queryModel, features):
    queryVector = features[queryModel]
    distances = [sum(query.getDistance(queryVector, features[meshPath])) for meshPath in features]
    return distances


# aggregates the distances for each of the possible 380 queryModels.
def calculateDistanceMatrix(features):
    return [distanceSortedNeighbours(queryModel, features) for queryModel in features.keys()]


# actually prints the distance matrix.
def main():
    str1 = "Chair"
    str2 = "Teddy"

    with open("./database/normalized_features.json", "r") as read_content:
        features = json.load(read_content)
        # now subset all models to only look at e.g. Chairs and Teddies.
        features = {k:v for k,v in features.items() if query.getClassFromPath(k) in (str1, str2)}
    array = calculateDistanceMatrix(features)
    labels = [os.path.join(os.path.basename(os.path.dirname(s)),os.path.basename(s)) for s in features.keys()]

    labelsize = 0.6
    size = 6

    x_dim = len(array)
    df_cm = pd.DataFrame(array, range(x_dim), range(x_dim))
    sn.set(font_scale=labelsize) # for label size
    sn.heatmap(df_cm, cmap="Blues", annot=True, annot_kws={"size": size}, fmt='.0f', xticklabels=labels, yticklabels=labels)

    plt.show()

    
if __name__ == "__main__":
    main()