import annoy
import json
import numpy as np
import open3d as o3d
import matplotlib.pylab as plt
from FeatureExtractorDemo import *
# Setup the annoy index

# Create a function to create the annoy index
def createAnnoyIndex(data, dimensions=55):
    annoyIndex = annoy.AnnoyIndex(dimensions, 'euclidean')

    for i, vector in enumerate(data):
        annoyIndex.add_item(i, vector)
    annoyIndex.build(10)
    
    return annoyIndex

def viewMesh(path, meshnr):
    mesh = o3d.io.read_triangle_mesh(".\\" + str(path))
    if meshnr == 0:
        mesh.paint_uniform_color([1,0,0])
        mesh.translate([-5,0,0])
    else:
        mesh.translate([(3*((meshnr-1)%8)) ,-(3*(int((meshnr-1)/8))) ,0])
     
    return mesh

def getClassFromPath(path):
    return str(path).split('\\')[-2]

def isNeighbourCorrect(basePath, nnPath):
    return getClassFromPath(basePath) == getClassFromPath(nnPath)

def featureToVector(feature):
    scalarKeys = ["surfaceArea", "compactness", "rectangularity", "diameter", "eccentricity"]
    descKeys = ["d1", "d2", "d3", "d4", "a3"]

    scalarVector = [feature[key] for key in scalarKeys]
    descVector = [val for key in descKeys for val in feature[key]]

    return np.array(scalarVector + descVector)

# Create a function to query the annoy index
def queryAnnoyIndex(annoyIndex, vector, k=10):
    return annoyIndex.get_nns_by_vector(vector, k, include_distances=True)

def getFileNameFromIndex(index, features):
    return list(features.keys())[index]

def getIndexFromFileName(filename, features):
    return list(features.keys()).index(filename)

def printQueryResults(neighbours, features, k):
    guessList = []
    o3dList = []
    count = 0
    indices, distances = neighbours
    fileNames = [getFileNameFromIndex(index, features) for index in indices]
    for x in range(len(fileNames)):
        o3dList.append(fileNames[x])
        if x != 0:
            guessList.append(["With a distance of: ", distances[x], "Guessed class: ", getClassFromPath(fileNames[x])])
            correctGuess = isNeighbourCorrect(fileNames[0], fileNames[x])
            if(correctGuess):
                count += 1
    meshlist = []
    meshnr = 0
    for path in o3dList:
        transmesh = viewMesh(path, meshnr)
        meshnr +=1
        meshlist.append(transmesh) 
    
    accuracy = count / k

    return guessList, accuracy, meshlist

def ANNProcess(filepath, k, Filebool):
    with open("./database/normalized_features.json", "r") as read_content:
        features = json.load(read_content)

    data = [featureToVector(feature) for feature in features.values()]
    annoyIndex = createAnnoyIndex(data)

    if Filebool == 0:
        neighbours = queryAnnoyIndex(annoyIndex, featureToVector(features[filepath]), k+1)
    else:
        neighbours = queryAnnoyIndex(annoyIndex, featureToVector(extractFeatures(filepath)), k+1)

    guesslist, accuracy, meshlist = printQueryResults(neighbours, features, k)
    return guesslist, accuracy, meshlist

if __name__ == "__main__":
    ANNProcess("models_final\\Airplane\\64.off", 10, 1)