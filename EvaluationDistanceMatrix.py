# Evaluation

import QueryProcessor as query
from sklearn.metrics import confusion_matrix

import numpy as np
import seaborn as sn
import pandas as pd
import matplotlib.pyplot as plt
import json
import os.path

def distanceSortedNeighbours(queryModel, features):
    queryVector = features[queryModel]
    distances = [query.getDistance(queryVector, features[meshPath]) for meshPath in features]
    return distances


# Now do this only for...
# FISH + HUMAN - if you query a HUMAN you get a lot of FISH.
# Print for all Human+fish what you get ONLY for humans+fishes. Sum those (will not sum to 200 anymore!)
# you get a nice confusion-matrix. Or wait... a DISTANCE matrix! Showing the distances to them!


def calculateDistanceMatrix(features):
    return [distanceSortedNeighbours(queryModel, features) for queryModel in features.keys()]

def main():
    str1 = "Chair"
    str2 = "Teddy"

    with open("./database/normalized_features.json", "r") as read_content:
        features = json.load(read_content)
        # BUT NOW ONLY FISH + HUMANS
        features = {k:v for k,v in features.items() if query.getClassFromPath(k) in (str1, str2)}
    # print(features.keys())
    array = calculateDistanceMatrix(features)
    labels = [os.path.join(os.path.basename(os.path.dirname(s)),os.path.basename(s)) for s in features.keys()]

    # optionally: divide them all by 200 - 20 meshes in every category, k=10 for each.
    # note: only the rows or y-axis (y_real) sum to 200. The x-axis (y_pred) can sum to any number, as we can predict any class as much as desired

    labelsize = 0.6
    size = 6

    x_dim = len(array)
    df_cm = pd.DataFrame(array, range(x_dim), range(x_dim))
    sn.set(font_scale=labelsize) # for label size
    sn.heatmap(df_cm, cmap="Blues", annot=True, annot_kws={"size": size}, fmt='.0f', xticklabels=labels, yticklabels=labels)

    plt.show()

    
if __name__ == "__main__":
    main()