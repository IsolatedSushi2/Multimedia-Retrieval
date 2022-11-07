import json
import numpy as np
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
from QueryProcessor import getClassFromPath
import seaborn as sns
import ANNDemo
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
def DRDemo(filepath, k):
    with open("./database/normalized_features.json", "r") as read_content:
        features = json.load(read_content)

    # Get all the data
    allData = [ANNDemo.featureToVector(features[filename]) for filename in features]
    data = np.array(allData)
    classes = [getClassFromPath(path) for path in features]

    # Perform an ANN with the dimension reduction
    dimensions = 2
    X_embedded_2n = createTSNEObject(data, dimensions)
    annIndex = ANNDemo.createAnnoyIndex(X_embedded_2n, dimensions)
    index = ANNDemo.getIndexFromFileName(filepath, features)
    neighbours = ANNDemo.queryAnnoyIndex(annIndex, X_embedded_2n[index], k+1)
    guesslist, accuracy, meshlist  = ANNDemo.printQueryResults(neighbours, features, k)



    # Plot the 2d TSNE dimension reduction
    #plotTSNE(X_embedded_2n, classes)
    return guesslist, accuracy, meshlist, X_embedded_2n, classes


if __name__ == "__main__":
    DRDemo("models_final\\Airplane\\64.off", k = 10)