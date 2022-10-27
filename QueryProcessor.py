import json
import numpy as np
import scipy
from sklearn.neighbors import NearestNeighbors
from termcolor import colored
import random
import time

def getSortedNeighbours(queryModel, features, k=10):
    
    queryVector = features[queryModel]
    count = 0
    distances = [(getDistance(queryVector, features[meshPath]), meshPath) for meshPath in features]
    sortedDistances = sorted(distances, key=lambda tup: tup[0])

    for distance, path in sortedDistances[1:1 + k]:
        correctGuess = isNeighbourCorrect(queryModel, path)
        if(correctGuess):
            count += 1
        color = 'green' if correctGuess else 'red'
        print(colored(f'With a distance of {distance}. Guessed class {getClassFromPath(path)}', color))

    accuracy = count / k
    print(colored(f"Queried for mesh {queryModel}, accuracy {accuracy * 100}%", "yellow"))
    return accuracy

def getDistance(queryVector, otherVector):
    scalarKeys = ["surfaceArea", "compactness", "rectangularity", "diameter", "eccentricity"]
    descKeys = ["d1", "d2", "d3", "d4", "a3"]

    queryScalarvector = [queryVector[key] for key in scalarKeys]
    queryDescvector = [queryVector[key] for key in descKeys]

    otherScalarvector = [otherVector[key] for key in scalarKeys]
    otherDescvector = [otherVector[key] for key in descKeys]

    scalarDistance = scipy.spatial.distance.euclidean(queryScalarvector, otherScalarvector)
    descWeights = [100, 100, 100, 100, 100]
    descDistances = sum([scipy.stats.wasserstein_distance(queryDescvector[i], otherDescvector[i]) * descWeights[i] for i in range(len(queryDescvector))])

    return scalarDistance + descDistances
# def queryVector(featureVectors, nbrs):
#     index = random.randint(0, len(featureVectors))
#     #index = 79
#     distances, indices = getKNN(nbrs, featureVectors.iloc[index])
#     results = featureVectors.iloc[indices]

#     basePath = featureVectors.iloc[index].name
#     guessScores = [isNeighbourCorrect(basePath, i) for i in results.index]

#     print(colored(f'KNN for {basePath}, using the {nbrs.metric} distance', 'yellow'))
#     for i in zip(results.index, distances, guessScores):
#         color = 'green' if i[2] else 'red'
#         print(colored(f'With a distance of {i[1]}. Guessed class {getClassFromPath(i[0])}', color))
#     print(colored(f'{sum(guessScores)} guessses correct out of {len(guessScores)}', 'yellow', attrs=['underline']))

def getClassFromPath(path):
    return str(path).split('\\')[-2]

def isNeighbourCorrect(basePath, nnPath):
    return getClassFromPath(basePath) == getClassFromPath(nnPath)

def queryAllVectors(k, features):
    t = time.time()
    distances = [getSortedNeighbours("models_final\\Airplane\\64.off", features, k) ]
    # distances = [getSortedNeighboursFaiss(queryModel, features, k) for queryModel in features]
    print(colored(f"Queried {len(distances)} meshes with k={k}, with an average accuracy of {np.mean(distances)} which took {time.time() - t} seconds", "red"))

def getFeatureVectors(n, features):

    returnDict = {}
    for i in range(n):
        index = i % len(features)
        filename = list(features.keys())[index] + "copy" * int(i / len(features))
        returnDict[filename] = list(features.values())[index]
    return returnDict

def main():
    with open("./database/normalized_features.json", "r") as read_content:
        features = json.load(read_content)

    k = 5
    getSortedNeighbours("models_final\\Cup\\21.off", features, k)


if __name__ == "__main__":
    main()