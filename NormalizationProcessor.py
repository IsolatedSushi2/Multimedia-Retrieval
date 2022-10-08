import open3d as o3d
import copy
import numpy as np
from pathlib import Path
import random

def processAllMeshes():
    pathList = list(Path('./labeledDb/labeledDB_new').rglob('*.off'))
    print(pathList)
    # while True:
    #     random_path = random.choice(pathList)
    #     processMesh(random_path)

    for path in pathList:
        processMesh(path)


def processMesh(path):
    mesh = o3d.io.read_triangle_mesh(".\\" + str(path))

    translated_mesh = processTranslation(mesh)
    aligned_mesh = processRotation(translated_mesh)
    scaled_mesh = processScale(aligned_mesh)

def processRotation(mesh):
    mesh_clone = copy.deepcopy(mesh)
    eigenvalues, eigenvectors = eigenValuesFromMesh(mesh_clone)

    # Get the necessary indices
    majorIndex = np.argmax(eigenvalues)
    mediumIndex = (majorIndex + 1) % 3

    #Get the necessary vectors
    majorEigenVector = eigenvectors[majorIndex]
    mediumEigenVector = eigenvectors[mediumIndex]
    perpendicularEigenVector = np.cross(majorEigenVector, mediumEigenVector)

    # Perform linear transformation
    for i in range(len(mesh_clone.vertices)):
        currVertex = mesh_clone.vertices[i]

        newVertex = [0, 0, 0]
        # In the rotation step, the mesh should already be translated to barycenter at the origin
        newVertex[0] = np.dot(currVertex, majorEigenVector)
        newVertex[1] = np.dot(currVertex, mediumEigenVector)
        newVertex[2] = np.dot(currVertex, perpendicularEigenVector)

        mesh_clone.vertices[i] = newVertex


    xScale, yScale, zScale = getFlippingSign(mesh_clone)

    print("flipping in xyz:", xScale, yScale, zScale)
    for i in range(len(mesh_clone.vertices)):
        mesh_clone.vertices[i][0] *= xScale
        mesh_clone.vertices[i][1] *= yScale
        mesh_clone.vertices[i][2] *= zScale

    o3d.visualization.draw_geometries([mesh_clone])
    return mesh_clone

def getFlippingSign(mesh):
    totals = [0, 0, 0]
    vertices = mesh.vertices
    for triangle in mesh.triangles:
        triangleCenter = (vertices[triangle[0]] + vertices[triangle[1]] + vertices[triangle[2]]) / 3
        
        for i in range(3):
            currVal = triangleCenter[i]
            totals[i] += np.sign(currVal) * currVal * currVal

    return np.sign(totals)

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
