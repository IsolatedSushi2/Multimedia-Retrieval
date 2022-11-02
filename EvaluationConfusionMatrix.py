# Evaluation

import QueryProcessor as query
from sklearn.metrics import confusion_matrix

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
    # y_true, y_pred = calculateConfusionMatrix(features, k=19)
    # labels = []
    # [labels.append(x) for x in y_true if x not in labels]
    # array = confusion_matrix(y_true, y_pred, labels=labels) # preferably y_true if all occur
    # s = sum(array[0]) # the index doesn't matter - all sum the same == 20*k
    # normalized_array = [[round(c*100/s) for c in row] for row in array]

    # this, to give a percentage or "acuracy". Is what Alex wanted, makes sense too - easier to interpret
    # note: only the rows or y-axis (y_real) sum to 200. The x-axis (y_pred) can sum to any number, as we can predict any class as much as desired


    # for k=19, round:
    normalized_array = [[57, 17, 0, 3, 6, 0, 1, 7, 1, 0, 0, 1, 0, 7, 0, 0, 0, 0, 1],
    [7, 42, 0, 19, 7, 0, 0, 0, 0, 0, 0, 2, 0, 7, 0, 1, 0, 1, 14],
    [9, 0, 28, 1, 13, 0, 1, 9, 17, 0, 0, 0, 2, 15, 0, 1, 2, 2, 1],
    [3, 19, 0, 17, 6, 0, 4, 0, 0, 7, 1, 9, 2, 3, 0, 4, 0, 7, 19],
    [7, 13, 0, 4, 29, 0, 1, 7, 0, 0, 0, 3, 1, 6, 0, 1, 0, 24, 3],
    [0, 0, 0, 0, 0, 57, 0, 0, 0, 0, 6, 0, 0, 0, 15, 0, 22, 0, 0],
    [2, 6, 0, 11, 3, 0, 14, 0, 1, 9, 0, 18, 2, 8, 2, 12, 1, 4, 8],
    [17, 0, 3, 0, 15, 0, 0, 58, 1, 0, 0, 0, 1, 3, 0, 0, 0, 0, 0],
    [7, 2, 7, 3, 0, 0, 2, 6, 40, 2, 0, 5, 6, 8, 1, 7, 3, 0, 1],
    [0, 0, 0, 5, 0, 0, 6, 0, 0, 52, 4, 18, 1, 0, 8, 0, 0, 0, 7],
    [0, 1, 0, 5, 1, 10, 4, 0, 0, 17, 24, 7, 1, 1, 18, 1, 4, 2, 4],
    [0, 2, 0, 10, 3, 0, 12, 0, 1, 18, 2, 27, 1, 2, 4, 7, 1, 5, 4],
    [1, 9, 3, 8, 14, 0, 1, 6, 2, 9, 2, 6, 17, 5, 2, 1, 0, 7, 7],
    [9, 11, 5, 6, 12, 0, 3, 4, 2, 0, 0, 6, 2, 24, 0, 3, 0, 6, 6],
    [0, 0, 0, 1, 0, 13, 3, 0, 0, 18, 10, 9, 2, 0, 29, 0, 13, 0, 1],
    [0, 2, 0, 9, 1, 0, 9, 0, 1, 0, 0, 10, 1, 5, 0, 59, 0, 1, 3],
    [0, 0, 1, 0, 0, 19, 1, 0, 4, 0, 2, 2, 1, 1, 16, 0, 54, 0, 0],
    [0, 2, 0, 8, 27, 0, 2, 0, 0, 1, 1, 6, 2, 3, 0, 0, 0, 42, 6],
    [1, 18, 0, 20, 2, 0, 3, 0, 0, 7, 1, 6, 0, 5, 1, 2, 0, 3, 30]]
    labels = ['Airplane', 'Ant', 'Glasses', 'Hand', 'Human', 'Mech', 'Octopus', 'Plier', 'Table', 'Teddy', 'Vase', 'Armadillo', 'Bearing', 'Bird', 'Bust', 'Chair', 'Cup', 'Fish', 'FourLeg']

    labelsize = 0.6
    size = 8

    x_dim = len(normalized_array)
    df_cm = pd.DataFrame(normalized_array, range(x_dim), range(x_dim))
    sn.set(font_scale=labelsize) # for label size
    sn.heatmap(df_cm, cmap="Blues", annot=True, annot_kws={"size": size},fmt='d', xticklabels=labels, yticklabels=labels)

    # print(df_cm)
    for row in df_cm.values.tolist():
        print(f"[{ ', '.join(list([str(r) for r in row])) }],")
    print(labels)
    plt.xlabel("Predicted class")
    plt.ylabel("Queried class")

    plt.show()

    
if __name__ == "__main__":
    main()