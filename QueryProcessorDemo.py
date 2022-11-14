import json
from attr import NOTHING
import numpy as np
import scipy
from sklearn.neighbors import NearestNeighbors
from termcolor import colored
import random
import time
import open3d as o3d
from FeatureExtractorDemo import *

def viewMesh(path, meshnr):
    mesh = o3d.io.read_triangle_mesh(".\\" + str(path))
    if meshnr == 0:
        mesh.paint_uniform_color([1,0,0])
        mesh.translate([-5,0,0])
    else:
        mesh.translate([(3*((meshnr-1)%8)) ,-(3*(int((meshnr-1)/8))) ,0])
     
    return mesh



def getSortedNeighbours(queryModel, features, Filebool, k=10):
    guessList = []
    o3dList = []
    o3dList.append(queryModel)

    if Filebool == 0:
        queryVector = features[queryModel]
    else:
        queryVector = extractFeatures(queryModel)
        print("query Extracted")
    count = 0
    distances = [(sum(getDistance(queryVector, features[meshPath])), meshPath) for meshPath in features]
    sortedDistances = sorted(distances, key=lambda tup: tup[0])

    for distance, path in sortedDistances[1:1 + k]:
        correctGuess = isNeighbourCorrect(queryModel, path)
        if(correctGuess):
            count += 1
        color = 'green' if correctGuess else 'red'
        print(colored(f'With a distance of {distance}. Guessed class {getClassFromPath(path)}', color))
        print(getDistance(queryVector, features[path]))
        guessList.append(["With a distance of: ", distance, "Guessed class:  ", getClassFromPath(path)])
        o3dList.append(path)
    
    meshlist = []
    meshnr = 0
    for path in o3dList:
        transmesh = viewMesh(path, meshnr)
        meshnr +=1
        meshlist.append(transmesh)  

    accuracy = count / k
    print(colored(f"Queried for mesh {queryModel}, accuracy {accuracy * 100}%", "yellow"))
    return guessList, accuracy, meshlist

def getDistance(queryVector, otherVector):
    scalarKeys = ["surfaceArea", "compactness", "rectangularity", "diameter", "eccentricity"]
    descKeys = ["d1", "d2", "d3", "d4", "a3"]

    queryScalarvector = [queryVector[key] for key in scalarKeys]
    queryDescvector = [queryVector[key] for key in descKeys]

    otherScalarvector = [otherVector[key] for key in scalarKeys]
    otherDescvector = [otherVector[key] for key in descKeys]

    #scalarweights: surfaceArea, compactness, rectangularity, diameter, eccentricity]
    scalarWeights = [2,2,1,1.2,40]
    scalarDistance = [scipy.spatial.distance.euclidean(queryScalarvector[i], otherScalarvector[i]) * scalarWeights[i] for i in range(len(queryScalarvector))]
    descWeights = [100, 200, 200, 100, 100]
    descDistances = [scipy.stats.wasserstein_distance(queryDescvector[i], otherDescvector[i]) * descWeights[i] for i in range(len(queryDescvector))]
    

    #print(scalarDistance)
    #print(descDistances)
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


def getFeatureVectors(n, features):

    returnDict = {}
    for i in range(n):
        index = i % len(features)
        filename = list(features.keys())[index] + "copy" * int(i / len(features))
        returnDict[filename] = list(features.values())[index]
    return returnDict

def mainProcess(filepath, k, Filebool):
    with open("./database/normalized_features.json", "r") as read_content:
        features = json.load(read_content)
    # "models_final\\Cup\\21.off"
    guesslist, acc, meshlist = getSortedNeighbours(filepath, features, Filebool, int(k))
    return guesslist, acc, meshlist


if __name__ == "__main__":
    mainProcess("models_final\\Airplane\\70.off", 5, 0)