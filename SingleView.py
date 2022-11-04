import open3d as o3d
from pathlib import Path
import matplotlib.pyplot as plt   # plots: for visualizing the data (e.g. histogram)

if __name__ == "__main__":
    #Vase/361.off , Table/141.off , Octopus/121.off
    path = Path('./models_final/Octopus/121.off')
    mesh = o3d.io.read_triangle_mesh(".\\" + str(path))
    print(".\\" + str(path))
    print(mesh)
    o3d.visualization.draw_geometries([mesh])   