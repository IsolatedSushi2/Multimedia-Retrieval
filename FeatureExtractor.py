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
    features["compactness"] = getCompactness(features["surfaceArea"], getApproximatedVolume(mesh))
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
    pathList = list(Path('./').rglob('*.off'))
    allFeatures = [extractFeatures(path) for path in pathList]

    dataFrame = pandas.DataFrame(allFeatures, index=pathList)
    dataFrame.to_csv("./database/features.csv")