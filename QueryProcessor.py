import pandas
import numpy as np
from scipy import stats
from sklearn.neighbors import NearestNeighbors
from termcolor import colored

def normalizeFeatures():
    features = pandas.read_csv('./database/features.csv', index_col=[0])

    #https://stackoverflow.com/questions/45834276/numpyzero-mean-data-and-standardization
    normFeatures = [stats.zscore(np.asarray(features[column])) for column in features.columns]

    normDict = dict(zip(features.columns, normFeatures))
    normalizedDF = pandas.DataFrame(normDict, index=features.index)
    normalizedDF.to_csv("./database/normalized_features.csv")

def getNearestNeighours(featureVectors):
    #Use the brute algorithm in order to access more metrics (doubt the extra computation time will be problematic)
    nbrs = NearestNeighbors(n_neighbors=10, algorithm='brute', metric="cosine").fit(featureVectors.values)

    return nbrs
    
def getKNN(nbrs, featureVector):
    distances, indices = nbrs.kneighbors([featureVector.values])

    return distances[0], indices[0]

def queryVector(featureVectors, nbrs):
    index = 75
    distances, indices = getKNN(nbrs, featureVectors.iloc[index])
    results = featureVectors.iloc[indices]

    basePath = featureVectors.iloc[index].name
    guessScores = [isNeighbourCorrect(basePath, i) for i in results.index]

    print(colored(f'KNN for {basePath}, using the {nbrs.metric} distance', 'yellow'))
    for i in zip(results.index, distances, guessScores):
        color = 'green' if i[2] else 'red'
        print(colored(f'With a distance of {i[1]}. Guessed class {getClassFromPath(i[0])}', color))
    print(colored(f'{sum(guessScores)} guessses correct out of {len(guessScores)}', 'yellow', attrs=['underline']))

def getClassFromPath(path):
    return path.split('\\')[-2]

def isNeighbourCorrect(basePath, nnPath):
    return getClassFromPath(basePath) == getClassFromPath(nnPath)

def main():
    normalizeFeatures()

    featureVectors = pandas.read_csv('./database/normalized_features.csv', index_col=[0])
    nbrs = getNearestNeighours(featureVectors)
    queryVector(featureVectors, nbrs)

if __name__ == "__main__":
    main()