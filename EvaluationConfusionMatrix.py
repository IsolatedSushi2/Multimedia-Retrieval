# Evaluation

import QueryProcessor as query
from sklearn.metrics import confusion_matrix

import numpy as np
import seaborn as sn
import pandas as pd
import matplotlib.pyplot as plt
import json

# How does sklearn confusion_matrix work?
# We want to check, for every mesh, what shapes pop up when we retrieve K shapes (e.g. 5 or 10).
# Of all those, how many are of our own kind? We expect all = K, but might get only 2.
# Now, we don't just want this number 2/K, but per class, how many do we get? How often does a 
#   head / tube / airplane pop up when we query a snake? etc.
# Just sum this and put it in.

# Sklearn does it as follows: Give all results, it auto calculates the numbers.
# Say, we feed it: [EXPECTED, EXPECTED, EXPECTED], [RECEIVED, RECEIVED, RECEIVED] it sums it for you.
# Just pass it: [Airplane, Airplane, Airplane, Cat, Cat, Cat...], [Airplane, Airplane, Dog, Cat, Cat, Dog...]
# Do this for every mesh of an airplane (20x), and every result for each mesh (K times) resulting in K*20
#   times a single class in Expected.

# To obtain such results... use QueryProcessor!
# call... main?
# 1. Changed .json to .csv as there is no json there... But have to change the code to load that in
# Anyway, what WOULD I do? No need to load a mesh: just use the values of the .csv

# I would need to change his getSortedNeighbors slightly, as to return the guessed classes, not just the
# accuracy. Something like:


def classifySortedNeighbours(queryModel, features, k=10):
    
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

def calculateConfusionMatrix(features, k=10):
    # for feature in features
    # set this to queryModel and run classify
    y_true = []
    y_pred = []
    for queryModel in features.keys():
        # TODO is features a... dict? To run based on a path? Yes!
        # queryModel e.g. = "models_final\\Airplane\\64.off"
        # Just somehow get all paths, or... get all KEYS from the json! Then, run for all.

        yt, yp = classifySortedNeighbours(queryModel, features, k)
        y_true.append(yt)
        y_pred.append(yp)
    y_true = [i for sublist in y_true for i in sublist]
    y_pred = [i for sublist in y_pred for i in sublist]
    return y_true, y_pred


def main():
    # with open("./database/normalized_features.json", "r") as read_content:
    #     features = json.load(read_content)
    # y_true, y_pred = calculateConfusionMatrix(features, k=5)
    # labels = []
    # [labels.append(x) for x in y_true if x not in labels]
    # array = confusion_matrix(y_true, y_pred, labels=labels) # preferably y_true if all occur

    # obtained from the code above, pasted manually to test different font sizes, etc.
    # NOTE: THIS WAS y_pred ORDER, NOT y_true !! This means the order of labels and such may differ from the usual one
    labels = ['Airplane', 'Bird', 'Table', 'Human', 'Plier', 'Ant', 'Hand', 'FourLeg', 'Armadillo', 'Octopus', 'Fish', 'Glasses', 'Cup', 'Bearing', 'Chair', 'Teddy', 'Mech', 'Bust', 'Vase']
    array = [[148, 10, 1, 4,   11,   22,   2,   2,   0,  0,    0,   0,    0,   0,    0,    0,    0,   0,   0],
            [14,  72,    6,  15,    8,   23,   9,  11,  12,   7,    4,  10,    0,   4 ,   5,    0,    0,   0,   0],
            [15,  17,  105,   0,   12,    4,   2,   0,   5,   3,    0,  12,    7,   9 ,   5,    2,    0,   1,   1],
            [10,   4,    0,  78,    4,   28,   9,   4,   8,   2,   50,   0,    0,   3 ,   0,    0,    0,   0,   0],
            [16,   7,    0,  16,  157,    0,   0,   0,   0,   0,    0,   1,    0,   3 ,   0,    0,    0,   0,   0],
            [9 ,  8 ,   0 , 14 ,   0 , 116 , 23 , 24 ,  4 ,  1 ,   1 ,  0 ,   0 ,  0  ,  0 ,   0 ,   0 ,  0 ,  0],
            [7 ,  8 ,   0 ,  9 ,   0 ,  37 , 47 , 41 , 19 ,  6 ,  11 ,  0 ,   0 ,  0 ,   3 ,  12 ,   0 ,  0 ,  0],
            [3 ,  8 ,   0 ,  3 ,   0 ,  30 , 41 , 79 ,  8 ,  3 ,   4 ,  0 ,   0 ,  0 ,   2 ,  18 ,   0 ,  0 ,  1],
            [0 ,  3 ,   3 ,  7 ,   0 ,   2 , 16 ,  9 , 67 , 29 ,  13 ,  0 ,   1 ,  0 ,   8 ,  33 ,   0 ,  6 ,  3],
            [6 , 18 ,   1 ,  3 ,   0 ,  10 , 25 , 10 , 45 , 37 ,   7 ,  0 ,   2 ,  1 ,  18 ,  13 ,   0 ,  3 ,  1],
            [0 ,  0 ,   0 , 45 ,   0 ,   4 , 12 , 11 , 14 ,  2 , 108 ,  0 ,   0 ,  0 ,   0 ,   1 ,   0 ,  0 ,  3],
            [10,  30,   26,   8,   18,    0,   4,   2,   0,   0,    4,  95,    1,   2,    0,    0,    0,   0,   0],
            [0 ,  2 ,   6 ,  0 ,   0 ,   0 ,  1 ,  0 ,  4 ,  2 ,   0 ,  0 , 128 ,  0 ,   0 ,   0 ,  31 , 24 ,  2],
            [0 , 11 ,   2 , 26 ,  11 ,  15 , 17 ,  9 ,  8 ,  2 ,   8 ,  3 ,   0 , 58 ,   2 ,  17 ,   0 ,  5 ,  6],
            [0 ,  8 ,   2 ,  1 ,   0 ,   3 , 11 ,  7 , 12 ,  9 ,   0 ,  0 ,   0 ,  0 , 147 ,   0 ,   0 ,  0 ,  0],
            [0 ,  0 ,   0 ,  0 ,   0 ,   0 ,  7 , 10 , 25 ,  2 ,   0 ,  0 ,   0 ,  0 ,   0 , 139 ,   0 , 14 ,  3],
            [0 ,  0 ,   0 ,  0 ,   0 ,   0 ,  0 ,  0 ,  0 ,  0 ,   0 ,  0 ,  29 ,  0 ,   0 ,   0 , 136 , 26 ,  9],
            [0 ,  0 ,   1 ,  0 ,   0 ,   0 ,  1 ,  2 ,  6 ,  4 ,   0 ,  0 ,  23 ,  4 ,   0 ,  32 ,  25 , 80 , 22],
            [0 ,  0 ,   0 ,  0 ,   0 ,   1 , 10 ,  8 , 14 ,  5 ,   4 ,  0 ,   9 ,  3 ,   0 ,  31 ,  14 , 38 , 63]]
    # optionally: divide them all by 200 - 20 meshes in every category, k=10 for each.
    # note: only the rows or y-axis (y_real) sum to 200. The x-axis (y_pred) can sum to any number, as we can predict any class as much as desired

    x_dim = len(array)
    df_cm = pd.DataFrame(array, range(x_dim), range(x_dim))
    sn.set(font_scale=1) # for label size
    sn.heatmap(df_cm, cmap="blues", annot=True, annot_kws={"size": 10},fmt='d', xticklabels=labels, yticklabels=labels)

    print(df_cm)
    print(labels)

    plt.show()

    
if __name__ == "__main__":
    main()