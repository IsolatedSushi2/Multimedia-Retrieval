import open3d as o3d
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt   # plots: for visualizing the data (e.g. histogram)


#make seperate folder for multiview
pathList= list(Path('./models_multiview').rglob('*.off'))


def multiview(pathList):
    meshlist = []
    meshnr = 0
    for path in pathList:
        transmesh = viewMesh(path, meshnr)
        meshnr +=1
        meshlist.append(transmesh)
        #print(".\\" + str(path))
    o3d.visualization.draw_geometries(meshlist)    

def viewMesh(path, meshnr):
    mesh = o3d.io.read_triangle_mesh(".\\" + str(path))
    mesh.translate([(3*(meshnr%8)) ,(3*(int(meshnr/8))) ,0])
    return mesh

if __name__ == "__main__":
    multiview(pathList)