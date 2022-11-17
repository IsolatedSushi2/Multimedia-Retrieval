import annoy
import json
import numpy as np
import open3d as o3d
import matplotlib.pylab as plt
from FeatureExtractorDemo import *
# Setup the annoy index

# Create a function to create the annoy index with euclidean (L2-distance) metric.
def createAnnoyIndex(data, dimensions=55):
    annoyIndex = annoy.AnnoyIndex(dimensions, 'euclidean')

    for i, vector in enumerate(data):
        annoyIndex.add_item(i, vector)
    annoyIndex.build(10)
    
    return annoyIndex
#create a multiview with first mesh in red and on left and the rest in pairs of 8 left->right, top->bottom like in multiview
def viewMesh(path, meshnr):
    mesh = o3d.io.read_triangle_mesh(".\\" + str(path))
    #translate and make red the first mesh (query mesh)
    if meshnr == 0:
        mesh.paint_uniform_color([1,0,0])
        mesh.translate([-5,0,0])
    else:
        #translate the rest of meshes accrodingly
        mesh.translate([(3*((meshnr-1)%8)) ,-(3*(int((meshnr-1)/8))) ,0])
     
    return mesh
#gets the class from the given mesh path.
def getClassFromPath(path):
    return str(path).split('\\')[-2]

#checks if this is a correct guess (class wise)
def isNeighbourCorrect(basePath, nnPath):
    return getClassFromPath(basePath) == getClassFromPath(nnPath)

#makes the feature list to 1 vector
def featureToVector(feature):
    scalarKeys = ["surfaceArea", "compactness", "rectangularity", "diameter", "eccentricity"]
    descKeys = ["d1", "d2", "d3", "d4", "a3"]

    scalarVector = [feature[key] for key in scalarKeys]
    descVector = [val for key in descKeys for val in feature[key]]

    return np.array(scalarVector + descVector)

# Create a function to query the annoy index
def queryAnnoyIndex(annoyIndex, vector, k=10):
    return annoyIndex.get_nns_by_vector(vector, k, include_distances=True)

#gets the filenames (mesh locations) from index numbers
def getFileNameFromIndex(index, features):
    return list(features.keys())[index]

#gets the index numbers from filenames (mesh location)
def getIndexFromFileName(filename, features):
    return list(features.keys()).index(filename)

#prints the query results (makes it so it gives the correct / same results as queryprocessor (F))
def printQueryResults(neighbours, features, k):
    guessList = []
    o3dList = []
    count = 0
    indices, distances = neighbours
    #get the filename list from all neighbours
    fileNames = [getFileNameFromIndex(index, features) for index in indices]
    for x in range(len(fileNames)):
        #create the O3D list for Open3D view
        o3dList.append(fileNames[x])
        if x != 0:
            #get the guesslist stuff for GUI terminal
            guessList.append(["With a distance of: ", distances[x], "Guessed class: ", getClassFromPath(fileNames[x])])
            #quick bool to check if it was a correct class guess
            correctGuess = isNeighbourCorrect(fileNames[0], fileNames[x])
            if(correctGuess):
                count += 1
    meshlist = []
    meshnr = 0
    #set the meshes in the O3D list in the correct location with translations etc for GUI
    for path in o3dList:
        transmesh = viewMesh(path, meshnr)
        meshnr +=1
        meshlist.append(transmesh) 
    
    #calc the accuracy
    accuracy = count / k

    return guessList, accuracy, meshlist

#main process of the program
def ANNProcess(filepath, k, Filebool):
    #open the database
    with open("./database/normalized_features.json", "r") as read_content:
        features = json.load(read_content)

    #make vectors for all meshes in DB
    data = [featureToVector(feature) for feature in features.values()]
    #create annoyIndex on Data
    annoyIndex = createAnnoyIndex(data)

    #Filebool == 0 when we use DB and ==1 when we EXTRACT features from file
    if Filebool == 0:
        neighbours = queryAnnoyIndex(annoyIndex, featureToVector(features[filepath]), k+1)
    else:
        neighbours = queryAnnoyIndex(annoyIndex, featureToVector(extractFeatures(filepath)), k+1)

    #use QueryResults to get correct values for the GUI back
    guesslist, accuracy, meshlist = printQueryResults(neighbours, features, k)
    return guesslist, accuracy, meshlist

#shows that the program is a standalone program and can work on it self.
if __name__ == "__main__":
    ANNProcess("models_final\\Airplane\\64.off", 10, 1)