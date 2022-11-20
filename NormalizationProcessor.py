import open3d as o3d
import copy
import numpy as np
from pathlib import Path
import random
import math
import matplotlib.pyplot as plt   # plots: for visualizing the data (e.g. histogram)
import os
import sys
#from HistCompare import make_histogram, make_histogram_comparison

#global variables
beforehist = []
afterhist = []
dircheck = False


def processAllMeshes():
    #base path change based on step.
    #pathList = list(Path('./labeledDb/labeledDB_new').rglob('*.off'))
    
    #for remesh -> center
    #pathList = list(Path('./models_remesh').rglob('*.off'))
    #Path_out = 'models_center'
    
    #for center -> allign
    pathList= list(Path('./models_center').rglob('*.off'))   
    Path_out = 'models_alligned'
    
    #for allig -> flip
    #pathList= list(Path('./models_alligned').rglob('*.off'))   
    #Path_out = 'models_flipped'

    #for flip -> scalled (finalized)
    #pathList= list(Path('./models_flipped').rglob('*.off'))   
    #Path_out = 'models_scaled_final'
    
    if dircheck:
        check_dir_exists(Path_out)


    filenr = 0
    for path in pathList:
        processMesh(path, Path_out)
        #filenr +=1
        #print(filenr, "out off", len(pathList))

    #histograms for before after centrilization
    #make_histogram_comparison(beforehist,'Distance of barycenter to origin (before translation)','Frequency', 0, afterhist, 'Distance of barycenter to origin(after translation)','Frequency')

def safe_mesh(mesh, foldername, path):
    newpath = os.getcwd() + '\\' + foldername + '\\' + os.path.basename(path)
    print(newpath)
    o3d.io.write_triangle_mesh(newpath, mesh)

def check_dir_exists(foldername):
    remeshpath = os.getcwd() + '\\' + foldername
    if os.path.exists(remeshpath):
        print("Cannot put remeshes in existing folder. Afraid of messing everything up.")
        sys.exit("ERROR")
    else:
        os.mkdir(remeshpath)

def processMesh(path, foldername):
    mesh = o3d.io.read_triangle_mesh(".\\" + str(path))
    #translated_mesh = o3d.io.read_triangle_mesh(".\\" + foldername + '\\' + os.path.basename(path))
    
    #translation
    #translated_mesh = processTranslation(mesh)
    #safe_mesh(translated_mesh, foldername, path)

    #allignment
    aligned_mesh = processRotation(mesh)
    #safe_mesh(aligned_mesh, foldername, path)

    #flipping
    #flipped_mesh = processFlipping(mesh)
    #safe_mesh(flipped_mesh, foldername, path)

    #scale
    #scaled_mesh = processScale(mesh)
    #safe_mesh(scaled_mesh, foldername, path)

    #axis_lines (for visualization)
    #axis_lines = processAxis()

    #visualization
    #o3d.visualization.draw_geometries([mesh.translate([2,2,0]), axis_lines, translated_mesh.paint_uniform_color([1,0,0])])
    #o3d.visualization.draw_geometries([mesh, scaled_mesh.translate([2, 0 ,0 ])])

    #histograms
    #make disthist before
    #beforehist.append(makeDistHist(mesh))
    #make disthist after
    #afterhist.append(makeDistHist(translated_mesh))

# Function to find distance in 3d points
def distance(x1, y1, z1, x2, y2, z2):
      
    d = math.sqrt(math.pow(x2 - x1, 2) +
                math.pow(y2 - y1, 2) +
                math.pow(z2 - z1, 2)* 1.0)
    return d

#makes the axis lines at (0,0,0) of coordinate system
def processAxis():
    scale = 10
    xVector = np.array([1,0,0]) * scale
    yVector = np.array([0,1,0]) * scale
    zVector = np.array([0,0,1]) * scale
    points = np.array([xVector, yVector, zVector, -xVector, -yVector, -zVector])
    lines = [[0, 3], [1, 4], [2, 5]]
    #x = red , y = green , z = blue
    colors = [[1, 0 ,0], [0, 1 ,0], [0, 0 ,1]]
    line_set = o3d.geometry.LineSet(points=o3d.utility.Vector3dVector(points), lines=o3d.utility.Vector2iVector(lines))
    line_set.colors = o3d.utility.Vector3dVector(colors)
    return line_set

def makeDistHist(mesh):
    center = calculateBaryCenter(mesh)
    dist = distance(center[0],center[1],center[2],0,0,0)
    print(dist)
    return dist

def processRotation(mesh):
    mesh_clone = copy.deepcopy(mesh)
    eigenvalues, eigenvectors = eigenValuesFromMesh(mesh_clone)
    


    #print(eigenvalues, eigenvectors)
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
    o3d.visualization.draw_geometries([mesh_clone, mesh.translate([5 ,0 ,0]).paint_uniform_color([1,0,0]),getEigenVectorLines(_val, _vec), processAxis()])

    return mesh_clone
    
def processFlipping(mesh):
    mesh_clone = copy.deepcopy(mesh)

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
    print("DIT IS De xVector:", xVector)
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

