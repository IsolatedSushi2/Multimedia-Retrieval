import annoy
import json
import numpy as np
# Setup the annoy index

# Create a function to create the annoy index
def createAnnoyIndex(data, dimensions=55):
    annoyIndex = annoy.AnnoyIndex(dimensions, 'euclidean')

    for i, vector in enumerate(data):
        annoyIndex.add_item(i, vector)
    annoyIndex.build(10)

    return annoyIndex

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

def printQueryResults(neighbours, features):
    indices, distances = neighbours
    fileNames = [getFileNameFromIndex(index, features) for index in indices]
    for i in zip(fileNames, distances):
        print(i)


def main():
    with open("./database/normalized_features.json", "r") as read_content:
        features = json.load(read_content)

    data = [featureToVector(feature) for feature in features.values()]
    annoyIndex = createAnnoyIndex(data)
    neighbours = queryAnnoyIndex(annoyIndex, featureToVector(features["models_final\\Airplane\\64.off"]), k=10)

    printQueryResults(neighbours, features)
    

if __name__ == "__main__":
    main()