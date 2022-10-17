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
        hull_ls = o3d.geometry.LineSet.create_from_triangle_mesh(convexHull)
        hull_ls.paint_uniform_color((1, 0, 0))
        o3d.visualization.draw_geometries([mesh, hull_ls])
        self_intersecting = mesh.is_self_intersecting()
        edge_manifold = mesh.is_edge_manifold(allow_boundary_edges=True)
        edge_manifold_boundary = mesh.is_edge_manifold(allow_boundary_edges=False)
        vertex_manifold = mesh.is_vertex_manifold()
        print(self_intersecting, edge_manifold, edge_manifold_boundary, vertex_manifold)
        print(colored('Not watertight convex hull error', 'red'))
        return 1
    return convexHull.get_volume()

def extractPyMeshFeatures(mesh_path, features):
    raise NotImplementedError()

if __name__ == "__main__":
    pathList = list(Path('./').rglob('*.off'))
    allFeatures = [extractFeatures(path) for path in pathList]

    dataFrame = pandas.DataFrame(allFeatures, index=pathList)
    dataFrame.to_csv("./database/features.csv")

