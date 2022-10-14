import open3d as o3d
import copy
import numpy as np
from pathlib import Path
import random


def processAllMeshes():
    pathList = list(Path('./labeledDb/labeledDB_new').rglob('*.off'))
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


    o3d.visualization.draw_geometries([mesh, scaled_mesh.translate([2, 0 ,0 ])])


def processRotation(mesh):
    mesh_clone = copy.deepcopy(mesh)
    eigenvalues, eigenvectors = eigenValuesFromMesh(mesh_clone)
    


    print(eigenvalues, eigenvectors)
    # rotMatrix = np.array(eigenvectors)

    # print("Rotation Matrix", rotMatrix)
    # mesh_clone.rotate(rotMatrix, center=(0, 0, 0))

    # for i in range(len(mesh_clone.vertices)):
    #     mesh_clone.vertices[i] = np.dot(rotMatrix, mesh_clone.vertices[i]).T

    # # Get the necessary indices
    # majorIndex = np.argmax(eigenvalues)
    # mediumIndex = (majorIndex + 1) % 3

    # Get the necessary vectors
    majorEigenVector = eigenvectors[0]
    mediumEigenVector = eigenvectors[1]
    perpendicularEigenVector = np.cross(majorEigenVector, mediumEigenVector)

    print("vectors", majorEigenVector, mediumEigenVector, perpendicularEigenVector)
    print("values", eigenvalues[0], eigenvalues[1], eigenvalues[2])
    # Perform linear transformation
    for i in range(len(mesh_clone.vertices)):
        currVertex = mesh_clone.vertices[i]

        newVertex = [0, 0, 0]
        # In the rotation step, the mesh should already be translated to barycenter at the origin
        newVertex[0] = np.dot(currVertex, majorEigenVector)
        newVertex[1] = np.dot(currVertex, mediumEigenVector)
        newVertex[2] = np.dot(currVertex, perpendicularEigenVector)

        mesh_clone.vertices[i] = newVertex

    _val, _vec = eigenValuesFromMesh(mesh_clone)
    #o3d.visualization.draw_geometries([mesh_clone, mesh.translate([5 ,0 ,0]) ,getEigenVectorLines(eigenvalues, eigenvectors).translate([5, 0 ,0]) ,getEigenVectorLines(_val, _vec)])


    xScale, yScale, zScale = getFlippingSign(mesh_clone)

    print("flipping in xyz:", xScale, yScale, zScale)

    for i in range(len(mesh_clone.vertices)):
        mesh_clone.vertices[i][0] *= xScale
        mesh_clone.vertices[i][1] *= yScale
        mesh_clone.vertices[i][2] *= zScale


    return mesh_clone


def getFlippingSign(mesh):
    totals = [0, 0, 0]
    vertices = mesh.vertices
    for triangle in mesh.triangles:
        triangleCenter = (
            vertices[triangle[0]] + vertices[triangle[1]] + vertices[triangle[2]]) / 3

        for i in range(3):
            currVal = triangleCenter[i]
            totals[i] += np.sign(currVal) * currVal * currVal

    return np.sign(totals)


def getEigenVectorLines(eigenvalues, eigenvectors):
    scale = 10

    #points = np.array([origin, eigenvectors[0] * eigenvalues[0], eigenvectors[1] * eigenvalues[1], eigenvectors[2] * eigenvalues[2]])

    xVector = scale * eigenvectors[0] * eigenvalues[0]
    yVector = scale * eigenvectors[1] * eigenvalues[1]
    zVector = scale * eigenvectors[2] * eigenvalues[2]

    points = np.array([xVector, yVector, zVector, -
                      xVector, -yVector, -zVector])
    lines = [[0, 3], [1, 4], [2, 5]]
    colors = [[1, 0 ,0], [0, 1 ,0], [0, 0 ,1]]
    line_set = o3d.geometry.LineSet(points=o3d.utility.Vector3dVector(
        points), lines=o3d.utility.Vector2iVector(lines))
    line_set.colors = o3d.utility.Vector3dVector(colors)

    return line_set


def eigenValuesFromMesh(mesh):
    vertices = np.asarray(mesh.vertices).T
    cov_matrix = np.cov(vertices)
    eigenvalues, eigenvectors = np.linalg.eig(cov_matrix)

    eigenComponents = list(zip(eigenvalues, eigenvectors.T))
    eigenComponents.sort(key=lambda x: x[0], reverse=True)

    eigenvalues, eigenvectors = zip(*eigenComponents)
    eigenvectors = np.asarray(eigenvectors)

    return eigenvalues, eigenvectors


def processTranslation(mesh):

    mesh_clone = copy.deepcopy(mesh)
    center = calculateBaryCenter(mesh_clone)
    mesh_clone.translate(-center)

    return mesh_clone


#According to https://stackoverflow.com/a/67078389/14264858
def calculateBaryCenter(mesh):
    totalVolume = 0
    totalVolumeWeightedCenters = np.array([0,0,0], dtype= np.float64)

    for triangle in mesh.triangles:
        currVertices = np.asarray(mesh.vertices)[np.asarray(triangle)]

        currCenter = (currVertices[0] + currVertices[1] + currVertices[2]) / 4
        currVolume = np.dot(currVertices[0], np.cross(currVertices[1], currVertices[2])) / 6

        totalVolume += currVolume
        totalVolumeWeightedCenters += currCenter * currVolume

    return totalVolumeWeightedCenters / totalVolume

def processScale(mesh):
    mesh_clone = copy.deepcopy(mesh)

    bounding_box = mesh_clone.get_axis_aligned_bounding_box()
    max_size = bounding_box.get_max_extent()
    scale = 1 / max_size

    mesh_clone.scale(scale, center=[0, 0, 0])
    return mesh_clone


def normalizeScale():
    return


if __name__ == "__main__":
    processAllMeshes()
