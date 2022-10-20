import open3d as o3d
from pathlib import Path
import random
import numpy as np
import scipy
from NormalizationProcessor import eigenValuesFromMesh
import pandas
from termcolor import colored

def extractFeatures(mesh_path):
    mesh = o3d.io.read_triangle_mesh(".\\" + str(mesh_path))

    features = {}
    # The 5 scalar features
    features["surfaceArea"] = mesh.get_surface_area()
    features["compactness"] = getCompactness(features["surfaceArea"], getApproximatedVolume(mesh))
    features["rectangularity"] = getApproximatedVolume(mesh) / mesh.get_axis_aligned_bounding_box().volume()
    features["diameter"] = getDiameter(mesh.vertices)
    features["eccentricity"] = getEccentricity(mesh)

    # The 5 distribution features
    num_samples = 10
    points = np.array(mesh.sample_points_uniformly(number_of_points=num_samples).points)
    
    d1Values = getD1(points)
    d2Values = getD2(points)
    d3Values = getD3(points)
    d4Values = getD4(points)
    a3Values = getA3(points)

    # features["d1"] = binned values
    # features["d2"] = binned values
    # features["d3"] = binned values
    # features["d4"] = binned values
    # features["a3"] = binned values

    return features

#Get the distance to bary center (which was translated to 0,0,0)
def getD1(points):
    return np.linalg.norm(points, axis=1)

#Get the distance between 2 random points on mesh
def getD2(points):
    #Generate n pairs
    randomPointPairs = np.array([points[np.random.choice(points.shape[0], 2, replace=False)] for _ in points])

    #Get the vectors, and return its length
    vectors = randomPointPairs[:, 1, :] - randomPointPairs[:, 0, :]
    return np.linalg.norm(vectors, axis=1)

def getD3(points):
    randomPointPairs = np.array([points[np.random.choice(points.shape[0], 3, replace=False)] for _ in points])
    crossProducts = np.cross(randomPointPairs[:, 1, :] - randomPointPairs[:, 0, :], randomPointPairs[:, 2, :] - randomPointPairs[:, 0, :])
    #Calculate and return the area
    return 0.5 * np.linalg.norm(crossProducts, axis=1)

#https://stackoverflow.com/questions/9866452/calculate-volume-of-any-tetrahedron-given-4-points/9866530
def getD4(points):
    randomPointPairs = np.array([points[np.random.choice(points.shape[0], 4, replace=False)] for _ in points])
    crossProducts = np.cross(randomPointPairs[:, 1, :] - randomPointPairs[:, 3, :], randomPointPairs[:, 2, :] - randomPointPairs[:, 3, :])
    #Calculate and return the volume
    return np.abs(np.sum((randomPointPairs[:, 0, :] - randomPointPairs[:, 3, :]) * crossProducts, axis=1)) / 6

#https://stackoverflow.com/questions/1211212/how-to-calculate-an-angle-from-three-points
def getA3(points):
    randomPointPairs = np.array([points[np.random.choice(points.shape[0], 3, replace=False)] for _ in points])
    line1 = randomPointPairs[:, 0, :] - randomPointPairs[:, 1, :]
    line2 = randomPointPairs[:, 2, :] - randomPointPairs[:, 1, :]

    cosine_angle = np.sum(line1 * line2, axis=1) / (np.linalg.norm(line1) * np.linalg.norm(line2))
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
    tetraVolumes = [getTetraVolumeFromFace(face, mesh) for face in mesh.triangles]
    return np.sum(tetraVolumes)

def getTetraVolumeFromFace(face, mesh):
    vertices = np.array(mesh.vertices)[np.array(face)]
    return np.dot(vertices[0], np.cross(vertices[1], vertices[2])) / 6

def getConvexHullVolume(mesh):
    convexHull, _ = mesh.compute_convex_hull()
    convexHull.orient_triangles()

    if not convexHull.is_watertight():
        print(colored('Not watertight convex hull error', 'red'))
        return np.Inf
    return convexHull.get_volume()

if __name__ == "__main__":
    pathList = list(Path('./labeledDb/LabeledDB_new/').rglob('*.off'))[:2]

    print(colored(f"Extracting features for {len(pathList)} meshes"))
    allFeatures = [extractFeatures(path) for path in pathList]

    dataFrame = pandas.DataFrame(allFeatures, index=pathList)
    dataFrame.to_csv("./database/features.csv")