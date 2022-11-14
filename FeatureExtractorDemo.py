import open3d as o3d
import numpy as np
import scipy
from NormalizationProcessor import eigenValuesFromMesh
from termcolor import colored
import math
from scipy import stats
import json


x = 0
def extractFeatures(mesh_path):
    mesh = o3d.io.read_triangle_mesh(".\\" + str(mesh_path))
    nrbins = 10


    #normalize the scalar functions with respect to what's in the database
    with open("./database/Scallers.json", "r") as read_content:
        features = json.load(read_content)

    featlen = len(features)
    # The 5 scalar features
    #features["path"] = str(mesh_path)
    surfaceArea = mesh.get_surface_area()
    compactness = getCompactness(surfaceArea, getApproximatedVolume(mesh))
    rectangularity = getApproximatedVolume(mesh) / mesh.get_axis_aligned_bounding_box().volume()
    diameter = getDiameter(mesh.vertices)
    eccentricity = getEccentricity(mesh)

    #print(rectangularity)
    #print(compactness)  

    features["querryVect"] = {"surfaceArea":surfaceArea, "compactness":compactness, "rectangularity":rectangularity, "diameter":diameter, "eccentricity":eccentricity}

    NormsurfaceArea = stats.zscore(np.asarray([features[filename]["surfaceArea"] for filename in features]))[featlen]
    Normcompactnessdic = stats.zscore(np.asarray([features[filename]["compactness"] for filename in features]))
    Normrectangularity = stats.zscore(np.asarray([features[filename]["rectangularity"] for filename in features]))[featlen]
    Normdiameter = stats.zscore(np.asarray([features[filename]["diameter"] for filename in features]))[featlen]
    Normeccentricity = stats.zscore(np.asarray([features[filename]["eccentricity"] for filename in features]))[featlen]


    Normcompactness = Normcompactnessdic[featlen]
    compactness = np.asarray([features[filename]["compactness"] for filename in features])
    #print(compactness)
    #print(Normcompactnessdic)

    #print(Normrectangularity)   
    #print(Normcompactness)



    # The 5 distribution features on N=10000 (only 10K so that extraction is reasonably fast....... (not really though))
    num_samples = 10000
    points = np.array(mesh.sample_points_uniformly(number_of_points=num_samples).points)

    # Generate n pairs
    randomPointPairs = np.array([points[np.random.choice(points.shape[0], 2, replace=False)] for _ in points])

    randomPointTrips = np.array([points[np.random.choice(points.shape[0], 3, replace=False)] for _ in points])

    randomPointQuads = np.array([points[np.random.choice(points.shape[0], 4, replace=False)] for _ in points])

    #print(randomPointPairs)

    d1Values = getD1(points)
    d2Values = getD2(randomPointPairs)
    d3Values = getD3(randomPointTrips)
    d4Values = getD4(randomPointQuads)
    a3Values = getA3(randomPointTrips)


    #normalize histogram values
    dbins = binvalues(0, 1, nrbins)
    d2bin = binvalues(0, np.sqrt(3), nrbins)
    a3bin = binvalues(0, math.pi, nrbins)

    #create bin nr instead of value.
    d1binlist = np.digitize(d1Values, dbins) -1
    d2binlist = np.digitize(d2Values, d2bin) -1
    d3binlist = np.digitize(d3Values, dbins) -1
    d4binlist = np.digitize(d4Values, dbins) -1
    a3binlist = np.digitize(a3Values, a3bin) -1

    countvaluesa3 = []
    countvaluesd1 = []
    countvaluesd2 = []
    countvaluesd3 = []
    countvaluesd4 = []

    for bin in range(nrbins):
        countvaluesa3.append(np.count_nonzero(a3binlist == bin))
        countvaluesd1.append(np.count_nonzero(d1binlist == bin))
        countvaluesd2.append(np.count_nonzero(d2binlist == bin))
        countvaluesd3.append(np.count_nonzero(d3binlist == bin))
        countvaluesd4.append(np.count_nonzero(d4binlist == bin))

    #print(countvaluesd1)
    # histDict = {"path": str(mesh_path), "class": QueryProcessor.getClassFromPath(mesh_path), "d1": d1Values.tolist(), "d2": d2Values.tolist(), "d3": d3Values.tolist(), "d4": d4Values.tolist(), "a3": a3Values.tolist()}
    #histDict = {"path": str(mesh_path), "class": QueryProcessor.getClassFromPath(mesh_path), "a3": a3Values.tolist()}
    #histDict = {"path": str(mesh_path), "class": QueryProcessor.getClassFromPath(mesh_path)}

    d1ValuesNorm = (np.array(countvaluesd1) / num_samples).tolist()
    d2ValuesNorm = (np.array(countvaluesd2) / num_samples).tolist()
    d3ValuesNorm = (np.array(countvaluesd3) / num_samples).tolist()
    d4ValuesNorm = (np.array(countvaluesd4) / num_samples).tolist()
    a3ValuesNorm = (np.array(countvaluesa3) / num_samples).tolist()


    querryfeature = {"surfaceArea":NormsurfaceArea, "compactness":Normcompactness, "rectangularity":Normrectangularity, "diameter":Normdiameter, "eccentricity":Normeccentricity,
                      "d1":d1ValuesNorm,"d2":d2ValuesNorm,"d3":d3ValuesNorm,"d4":d4ValuesNorm,"a3":a3ValuesNorm}

    #print(querryfeature)
    return querryfeature

# Get the distance to bary center (which was translated to 0,0,0)

def binvalues(min,max, nrbins):
    binlist = np.arange(min, (max+((max-min)/nrbins)), ((max-min)/nrbins))
    return binlist

def getD1(points):
    return np.linalg.norm(points, axis=1)

# Get the distance between 2 random points on mesh


def getD2(points):
    # Get the vectors, and return its length
    vectors = points[:, 1, :] - points[:, 0, :]
    return np.linalg.norm(vectors, axis=1)


def getD3(points):
    crossProducts = np.cross(points[:, 1, :] - points[:, 0, :],
                             points[:, 2, :] - points[:, 0, :])
    # Calculate and return the area
    return np.sqrt(0.5 * np.linalg.norm(crossProducts, axis=1))

# https://stackoverflow.com/questions/9866452/calculate-volume-of-any-tetrahedron-given-4-points/9866530


def getD4(points):
    crossProducts = np.cross(points[:, 1, :] - points[:, 3, :],
                             points[:, 2, :] - points[:, 3, :])
    # Calculate and return the volume
    return np.cbrt(np.abs(np.sum((points[:, 0, :] - points[:, 3, :]) * crossProducts, axis=1)) / 6)

# https://stackoverflow.com/questions/1211212/how-to-calculate-an-angle-from-three-points


def getA3(points):
    line1 = points[:, 0, :] - points[:, 1, :]
    line2 = points[:, 2, :] - points[:, 1, :]

    cosine_angle = np.sum(line1 * line2, axis=1) / (np.linalg.norm(line1, axis=1) * np.linalg.norm(line2, axis=1))
    return np.arccos(cosine_angle)


def getEccentricity(mesh):
    eigenvalues, eigenvectors = eigenValuesFromMesh(mesh)
    return eigenvalues[0] / eigenvalues[2]


def getDiameter(vertices):
    distanceMatrix = scipy.spatial.distance.cdist(vertices, vertices)
    return np.max(distanceMatrix)


def getCompactness(surface, volume):
    return (surface ** 3) / (36 * np.pi * volume ** 2)


def getApproximatedVolume(mesh):
    tetraVolumes = [getTetraVolumeFromFace(face, mesh) for face in np.asarray(mesh.triangles)]#doesn't work???
    return np.sum(tetraVolumes)


def getTetraVolumeFromFace(face, mesh):
    vertices = np.array(mesh.vertices)[np.array(face)]
    return (np.abs(np.dot(vertices[0], np.cross(vertices[1], vertices[2]))) / 6)


def getConvexHullVolume(mesh):
    convexHull, _ = mesh.compute_convex_hull()
    convexHull.orient_triangles()

    if not convexHull.is_watertight():
        print(colored('Not watertight convex hull error', 'red'))
        return np.Inf
    return convexHull.get_volume()


if __name__ == "__main__":
    extractFeatures("models_final\\Airplane\\70.off")
