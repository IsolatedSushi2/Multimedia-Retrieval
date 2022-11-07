import open3d as o3d
from pathlib import Path
import random
import numpy as np
import scipy
from NormalizationProcessor import eigenValuesFromMesh
import pandas
from termcolor import colored
import QueryProcessor
import json
import multiprocessing as mp

Q = mp.Queue()
x = 0
def extractFeatures(mesh_path):
    mesh = o3d.io.read_triangle_mesh(".\\" + str(mesh_path))
    # print(mesh_path)
    # Features are disabeled for now
    features = {}
    # The 5 scalar features
    #features["surfaceArea"] = mesh.get_surface_area()
    #features["compactness"] = getCompactness(features["surfaceArea"], getApproximatedVolume(mesh))
    features["rectangularity"] = getApproximatedVolume(mesh) / mesh.get_axis_aligned_bounding_box().volume()
    #features["diameter"] = getDiameter(mesh.vertices)
    #features["eccentricity"] = getEccentricity(mesh)

    # The 5 distribution features on N=100000
    #num_samples = 100000
    #points = np.array(mesh.sample_points_uniformly(number_of_points=num_samples).points)

    # d1Values = getD1(points)
    # d2Values = getD2(points)
    # d3Values = getD3(points)
    # d4Values = getD4(points)
    # a3Values = getA3(points)

    # histDict = {"path": str(mesh_path), "class": QueryProcessor.getClassFromPath(mesh_path), "d1": d1Values.tolist(), "d2": d2Values.tolist(), "d3": d3Values.tolist(), "d4": d4Values.tolist(), "a3": a3Values.tolist()}
    #histDict = {"path": str(mesh_path), "class": QueryProcessor.getClassFromPath(mesh_path), "a3": a3Values.tolist()}
    #histDict = {"path": str(mesh_path), "class": QueryProcessor.getClassFromPath(mesh_path)}

    # features["d1"] = binned values
    # features["d2"] = binned values
    # features["d3"] = binned values
    # features["d4"] = binned values
    # features["a3"] = binned values
    print("yes?")
    return features

# Get the distance to bary center (which was translated to 0,0,0)


def getD1(points):
    return np.linalg.norm(points, axis=1)

# Get the distance between 2 random points on mesh


def getD2(points):
    # Generate n pairs
    randomPointPairs = np.array(
        [points[np.random.choice(points.shape[0], 2, replace=False)] for _ in points])

    # Get the vectors, and return its length
    vectors = randomPointPairs[:, 1, :] - randomPointPairs[:, 0, :]
    return np.linalg.norm(vectors, axis=1)


def getD3(points):
    randomPointPairs = np.array(
        [points[np.random.choice(points.shape[0], 3, replace=False)] for _ in points])
    crossProducts = np.cross(randomPointPairs[:, 1, :] - randomPointPairs[:, 0, :],
                             randomPointPairs[:, 2, :] - randomPointPairs[:, 0, :])
    # Calculate and return the area
    return np.sqrt(0.5 * np.linalg.norm(crossProducts, axis=1))

# https://stackoverflow.com/questions/9866452/calculate-volume-of-any-tetrahedron-given-4-points/9866530


def getD4(points):
    randomPointPairs = np.array(
        [points[np.random.choice(points.shape[0], 4, replace=False)] for _ in points])
    crossProducts = np.cross(randomPointPairs[:, 1, :] - randomPointPairs[:, 3, :],
                             randomPointPairs[:, 2, :] - randomPointPairs[:, 3, :])
    # Calculate and return the volume
    return np.cbrt(np.abs(np.sum((randomPointPairs[:, 0, :] - randomPointPairs[:, 3, :]) * crossProducts, axis=1)) / 6)

# https://stackoverflow.com/questions/1211212/how-to-calculate-an-angle-from-three-points


def getA3(points):
    randomPointPairs = np.array(
        [points[np.random.choice(points.shape[0], 3, replace=False)] for _ in points])
    line1 = randomPointPairs[:, 0, :] - randomPointPairs[:, 1, :]
    line2 = randomPointPairs[:, 2, :] - randomPointPairs[:, 1, :]

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
    print("check1")
    print(mesh.triangles)
    tetraVolumes = [getTetraVolumeFromFace(face, mesh) for face in mesh.triangles]#doesn't work???
    print("CHECK 2")
    return np.sum(tetraVolumes)


def getTetraVolumeFromFace(face, mesh):
    global x
    vertices = np.array(mesh.vertices)[np.array(face)]
    x +=1
    print(x)
    return (np.abs(np.dot(vertices[0], np.cross(vertices[1], vertices[2]))) / 6)


def getConvexHullVolume(mesh):
    convexHull, _ = mesh.compute_convex_hull()
    convexHull.orient_triangles()

    if not convexHull.is_watertight():
        print(colored('Not watertight convex hull error', 'red'))
        return np.Inf
    return convexHull.get_volume()


allFeatures = []
def log_result(result):
    # This is called whenever extractFeatures returns a result.
    # allFeatures list is modified only by the main process, not the pool workers.
    allFeatures.append(result)

if __name__ == "__main__":
    pathList = list(Path('./models_final/').rglob('*.off'))
    print(colored(f"Extracting features for {len(pathList)} meshes"))
    extractFeatures("models_final\\Airplane\\64.off")
    #allFeatures = [extractFeatures(path) for path in pathList]  
    '''
    #multi-process Json-Creation of featurefactor
    for i in range(int(380/20)):
        print("start met stap i =" , i)
        pool = mp.Pool()
        allFeatures = []
        #new file every 20 meshes (inbetween saving vs crashes / other nasty interrupts.)
        copyPath = pathList[(i*20):((i+1)*20)]
        for path in copyPath:
            pool.apply_async(extractFeatures, args=(path,), callback = log_result)
        pool.close()
        pool.join()
        fileloc = "./database/Rectangularity" + str(i) + ".json"
        with open(fileloc, 'w') as f:
            json.dump(allFeatures, f)
    '''
    print(allFeatures)
#commented out the dataframe panda since this wont be used just yet
'''       
    dataFrame = pandas.DataFrame(allFeatures, index=pathList)
    dataFrame.to_csv("./database/features.csv")
'''