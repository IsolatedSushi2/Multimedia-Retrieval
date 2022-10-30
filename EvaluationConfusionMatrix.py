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
    with open("./database/normalized_features.json", "r") as read_content:
        features = json.load(read_content)
    y_true, y_pred = calculateConfusionMatrix(features, k=5)
    labels = []
    [labels.append(x) for x in y_true if x not in labels]
    array = confusion_matrix(y_true, y_pred, labels=labels) # preferably y_true if all occur

    # optionally: divide them all by 200 - 20 meshes in every category, k=10 for each.
    # note: only the rows or y-axis (y_real) sum to 200. The x-axis (y_pred) can sum to any number, as we can predict any class as much as desired

#     0   1   2   3   4   5   6   7   8   9   10  11  12  13  14  15  16  17  18
# 0   88   7   0   0   0   0   0   3   0   0   0   0   0   2   0   0   0   0   0
# 1    3  66   0  11   7   0   0   0   0   0   0   0   0   5   0   0   0   0   8
# 2    0   0  78   0   1   0   0   6   3   0   0   0   1  11   0   0   0   0   0
# 3    5  14   0  30   4   0   1   0   0   3   0  10   0   4   0   2   0   5  22
# 4    4  11   0   4  48   0   1   0   0   0   0   7   0   2   0   0   0  22   1
# 5    0   0   0   0   0  74   0   0   0   0   3   0   0   0  15   0   8   0   0
# 6    3   7   0  10   3   0  25   0   1   2   1  25   1  10   1   7   0   2   2
# 7    3   0   0   0   4   0   0  90   0   0   0   0   0   3   0   0   0   0   0
# 8    9   2   4   0   0   0   1   4  61   1   1   2   2   5   1   2   5   0   0
# 9    0   0   0   3   0   0   0   0   0  83   1   3   0   0   7   0   0   0   3
# 10   0   1   0   4   0   6   3   0   0  13  36   6   2   0  23   0   1   3   2
# 11   0   1   0   8   4   0  10   0   1   9   3  51   0   3   2   0   0   6   2
# 12   0   4   0   7   8   0   1   4   0   5   2   4  50   5   4   0   0   6   0
# 13   4  10   2   3   8   0   2   2   2   0   0   3   4  50   0   4   0   1   5
# 14   0   0   0   0   0  13   1   0   0  17   9   3   2   0  48   0   7   0   0
# 15   0   1   0   2   1   0   4   0   1   0   0   6   0   0   0  81   0   0   4
# 16   0   0   0   0   0   8   2   0   3   0   1   1   0   0   8   0  77   0   0
# 17   0   1   0   6  18   0   0   0   0   0   2   5   0   0   0   0   0  64   4
# 18   1  10   0  24   2   0   3   0   0   8   1   1   0   2   0   1   0   1  46
# ['Airplane', 'Ant', 'Glasses', 'Hand', 'Human', 'Mech', 'Octopus', 'Plier', 'Table', 'Teddy', 'Vase', 'Armadillo', 'Bearing', 'Bird', 'Bust', 'Chair', 'Cup', 'Fish', 'FourLeg']

    labelsize = 0.6
    size = 8

    x_dim = len(array)
    df_cm = pd.DataFrame(array, range(x_dim), range(x_dim))
    sn.set(font_scale=labelsize) # for label size
    sn.heatmap(df_cm, cmap="Blues", annot=True, annot_kws={"size": size},fmt='d', xticklabels=labels, yticklabels=labels)

    print(df_cm)
    print(labels)
    plt.xlabel("Predicted class")
    plt.ylabel("Queried class")

    plt.show()

    
if __name__ == "__main__":
    main()