import open3d as o3d
import copy
import numpy as np
from pathlib import Path
import random

def processAllMeshes():
    pathList = list(Path('./').rglob('*.off'))

    while True:
        random_path = random.choice(pathList)
        processMesh(random_path)


def processMesh(path):
    mesh = o3d.io.read_triangle_mesh(".\\" + str(path))

    aligned_mesh = processRotation(mesh)
    return
    scaled_mesh = processScale(mesh)
    translated_mesh = processTranslation(scaled_mesh)

def processRotation(mesh):
    mesh_clone = copy.deepcopy(mesh)
    eigenvalues, eigenvectors = eigenValuesFromMesh(mesh_clone)

    lineset = getEigenVectorLines(mesh_clone.get_center(), eigenvalues, eigenvectors)
    o3d.visualization.draw_geometries([lineset, mesh_clone])


def getEigenVectorLines(origin, eigenvalues, eigenvectors):
    scale = 10
    eigenvalues = eigenvalues * scale

    #points = np.array([origin, eigenvectors[0] * eigenvalues[0], eigenvectors[1] * eigenvalues[1], eigenvectors[2] * eigenvalues[2]])
    points = np.array([eigenvectors[0] * eigenvalues[0], eigenvectors[1] * eigenvalues[1], eigenvectors[2] * eigenvalues[2], -eigenvectors[0] * eigenvalues[0], -eigenvectors[1] * eigenvalues[1], -eigenvectors[2] * eigenvalues[2]])
    lines = [[0, 3], [1, 4], [2, 5]]
    colors = [[1, 0, 0] for i in range(len(lines))]
    line_set = o3d.geometry.LineSet()
    line_set.points = o3d.utility.Vector3dVector(points)
    line_set.lines = o3d.utility.Vector2iVector(lines)
    line_set.colors = o3d.utility.Vector3dVector(colors)
    
    return line_set


def eigenValuesFromMesh(mesh):
    print(dir(mesh.vertices))
    
    vertices = np.asarray(mesh.vertices).T

    pcd = mesh.sample_points_poisson_disk(1000)
    print(np.asarray(pcd.points).shape)
    mean, cov_matrix = pcd.compute_mean_and_covariance()
    # cov_matrix = np.cov(vertices)
    cov_matrix = np.cov(np.asarray(pcd.points).T)
    eigenvalues, eigenvectors = np.linalg.eig(cov_matrix)
    print(eigenvalues, eigenvectors)

    return eigenvalues, eigenvectors

def processTranslation(mesh):
    mesh_clone = copy.deepcopy(mesh)

    center = mesh_clone.get_center()
    print(center)
    mesh_clone.translate(-center)
    print(mesh_clone.get_center())

    return mesh_clone


def processScale(mesh):
    mesh_clone = copy.deepcopy(mesh)

    bounding_box = mesh_clone.get_axis_aligned_bounding_box()
    max_size = bounding_box.get_max_extent()
    scale = 1 / max_size

    mesh_clone.scale(scale, center=mesh_clone.get_center())
    return mesh_clone


def normalizeScale():
    return


if __name__ == "__main__":
    processAllMeshes()
