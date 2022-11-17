import json
from attr import NOTHING
import numpy as np
import scipy
from sklearn.neighbors import NearestNeighbors
from termcolor import colored
import open3d as o3d
from FeatureExtractorDemo import *

#create a multiview with first mesh in red and on left and the rest in pairs of 8 left->right, top->bottom like in multiview
def viewMesh(path, meshnr):
    mesh = o3d.io.read_triangle_mesh(".\\" + str(path))
    #translate and make red the first mesh (query mesh)
    if meshnr == 0:
        mesh.paint_uniform_color([1,0,0])
        mesh.translate([-5,0,0])
    else:
        #translate the rest of meshesh accordingly
        mesh.translate([(3*((meshnr-1)%8)) ,-(3*(int((meshnr-1)/8))) ,0])
     
    return mesh


# our F function that gives the lowest k distances back of the queryvector.
def getSortedNeighbours(queryModel, features, Filebool, k=10):
    guessList = []
    o3dList = []
    o3dList.append(queryModel)

    #filebool = 0 use Database else create a new queryvector.
    if Filebool == 0:
        queryVector = features[queryModel]
    else:
        queryVector = extractFeatures(queryModel)
        print("query Extracted")
    #value used for precision
    count = 0
    #all distances per mesh (summed so we have the total mesh distance)
    distances = [(sum(getDistance(queryVector, features[meshPath])), meshPath) for meshPath in features]
    #sort these distances
    sortedDistances = sorted(distances, key=lambda tup: tup[0])

    #for distance , mesh check how many correct and print if correct or incorrect in Terminal, and add to guesslist and Open3d list
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
    #fix your O3dlist so that its translated correctly
    for path in o3dList:
        transmesh = viewMesh(path, meshnr)
        meshnr +=1
        meshlist.append(transmesh)  

    #calc the accuracy
    accuracy = count / k
    print(colored(f"Queried for mesh {queryModel}, accuracy {accuracy * 100}%", "yellow"))
    return guessList, accuracy, meshlist

#calcs the distances from query and rest vector (1 to 1) and uses euclidean for scalar, EMD for binned hist.
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
    #bin weights d1,d2,d3,d4,a3
    descWeights = [100, 200, 200, 100, 100]
    descDistances = [scipy.stats.wasserstein_distance(queryDescvector[i], otherDescvector[i]) * descWeights[i] for i in range(len(queryDescvector))]
    
    return scalarDistance + descDistances

#gives class from path
def getClassFromPath(path):
    return str(path).split('\\')[-2]

#check if class = class
def isNeighbourCorrect(basePath, nnPath):
    return getClassFromPath(basePath) == getClassFromPath(nnPath)

#main process to start
def mainProcess(filepath, k, Filebool):
    #open the database
    with open("./database/normalized_features.json", "r") as read_content:
        features = json.load(read_content)
    #get results from sortedNeighbours 
    guesslist, acc, meshlist = getSortedNeighbours(filepath, features, Filebool, int(k))
    return guesslist, acc, meshlist

#shows that its standalone
if __name__ == "__main__":
    mainProcess("models_final\\Airplane\\70.off", 5, 0)