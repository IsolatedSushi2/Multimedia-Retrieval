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
    features["surfaceArea"] = mesh.get_surface_area()
    features["compactness"] = getCompactness(features["surfaceArea"], getConvexHullVolume(mesh))
    features["BBoxVolume"] = mesh.get_axis_aligned_bounding_box().volume()
    features["diameter"] = getDiameter(mesh.vertices)
    features["eccentricity"] = getEccentricity(mesh)

    return features

def getEccentricity(mesh):
    eigenvalues, eigenvectors = eigenValuesFromMesh(mesh)
    return eigenvalues[0] / eigenvalues[2]

def getDiameter(vertices):
    distanceMatrix = scipy.spatial.distance.cdist(vertices, vertices)
    return np.max(distanceMatrix)

def getCompactness(surface, volume):
    return (surface ** 3) / (36 * np.pi * volume ** 2)

def getConvexHullVolume(mesh):
    convexHull, _ = mesh.compute_convex_hull()
    convexHull.orient_triangles()

    if not convexHull.is_watertight():
        print(colored('Not watertight convex hull error', 'red'))
        return np.Inf
    return convexHull.get_volume()

def extractPyMeshFeatures(mesh_path, features):
    raise NotImplementedError()

if __name__ == "__main__":
    pathList = list(Path('./').rglob('*.off'))
    allFeatures = [extractFeatures(path) for path in pathList]

    dataFrame = pandas.DataFrame(allFeatures, index=pathList)
    dataFrame.to_csv("./database/features.csv")

