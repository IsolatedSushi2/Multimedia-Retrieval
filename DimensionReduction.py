import json
import numpy as np
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
from QueryProcessor import getClassFromPath
import seaborn as sns
import ANN
import colorcet as cc

from collections import defaultdict

def createTSNEObject(data, n_components=2):
    X_embedded = TSNE(n_components=n_components, method="exact", learning_rate='auto',
                  init='random', perplexity=40).fit_transform(data)

    return X_embedded

def plotTSNE(X_embedded, classes):
    palette = sns.color_palette(cc.glasbey, n_colors=len(set(classes)))
    colorMapper = dict(zip(set(classes), palette))
    x = X_embedded[:, 0]
    y = X_embedded[:, 1]

    print(colorMapper)

    dataDict = defaultdict(list)

    for currX, currY, currClass in zip(x,y, classes):
        dataDict[currClass].append((currX, currY))

    for currClass in dataDict:
        currX, currY = zip(*dataDict[currClass])
        plt.scatter(currX, currY, color=colorMapper[currClass], label=currClass)

    plt.legend()
    plt.show()

#Create the main function
def main():
    with open("./database/normalized_features.json", "r") as read_content:
        features = json.load(read_content)

    # Get all the data
    allData = [ANN.featureToVector(features[filename]) for filename in features]
    data = np.array(allData)
    classes = [getClassFromPath(path) for path in features]

    # # Perform an ANN with the dimension reduction
    # dimensions = 10
    # X_embedded_10n = createTSNEObject(data, dimensions)
    # annIndex = ANN.createAnnoyIndex(X_embedded_10n, dimensions)
    # index = ANN.getIndexFromFileName("models_final\\Airplane\\64.off", features)
    # neighbours = ANN.queryAnnoyIndex(annIndex, X_embedded_10n[index])
    # ANN.printQueryResults(neighbours, features)



    # Plot the 2d TSNE dimension reduction
    x_embedded_2n = createTSNEObject(data, 2)
    plotTSNE(x_embedded_2n, classes)



if __name__ == "__main__":
    main()