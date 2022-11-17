import open3d as o3d
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt   # plots: for visualizing the data (e.g. histogram)


#seperate folder called multiview and checks all files in there (only if you wanna multiview different meshes for testing purpose)
pathList= list(Path('./models_multiview').rglob('*.off'))

#multiview gets a pathlist (list of meshes) and views all of them in a singular window
def multiview(pathList):
    meshlist = []
    meshnr = 0
    #for all meshes in the pathlist create a transmesh (translated mesh) add to meshlist to create 1 view
    for path in pathList:
        transmesh = viewMesh(path, meshnr)
        meshnr +=1
        meshlist.append(transmesh)
        #print(".\\" + str(path))
    o3d.visualization.draw_geometries(meshlist)    

#create the meshlist from left to right top to bottom in pairs of 8.
def viewMesh(path, meshnr):
    mesh = o3d.io.read_triangle_mesh(".\\" + str(path))
    mesh.translate([(3*(meshnr%8)) ,(3*(int(meshnr/8))) ,0])
    return mesh

#sign that this function is a standalone application.
if __name__ == "__main__":
    multiview(pathList)