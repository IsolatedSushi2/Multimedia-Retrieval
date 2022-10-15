import pymeshlab
import matplotlib.pyplot as plt   # plots: for visualizing the data (e.g. histogram)
import numpy as np
import os                         # paths: for getting the files
ms = pymeshlab.MeshSet()


base_path = os.getcwd() + '\labeledDb\LabeledDB_new'

all_paths = []
# Only add paths that lead to .off files: we don't want the labels.
for (dirpath, dirnames, filenames) in os.walk(base_path):
    for filename in filenames:
        if filename.endswith('.off'):
            all_paths.append(os.path.join(dirpath, filename))

print(f"Found {len(all_paths)} .off files.")
# Check whether all paths actually function, as a simple test.
actual_paths = 0
for path in all_paths:
    actual_paths += 1 if os.path.exists(path) else 0
print(f"Actual paths: {actual_paths} / {len(all_paths)}.")


# https://pymeshlab.readthedocs.io/en/0.1.5/classes/mesh.html
# For what a mesh all contains.

def make_histogram(a, xlabel, ylabel, hist_step=200, x_min=0):
    x_max = max(a)
    x,y = np.histogram(a=a, bins=int((x_max-x_min)/hist_step), range=(x_min, x_max))
    plt.stairs(x, y, fill=True)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()

def plot_stats():
    hist_vertex = []
    hist_face   = []
    hist_edge   = []

    for path in all_paths:
        ms.load_new_mesh(path)
        m = ms.current_mesh()

        hist_vertex.append(m.vertex_number())
        hist_face.append(m.face_number())    
        hist_edge.append(m.edge_number()) 

    make_histogram(hist_vertex,'No. of vertices','Frequency')
    # make_histogram(hist_face,'No. of faces','Frequency')  # UNCOMMENT TO PRINT TOO
    # make_histogram(hist_face,'No. of edges','Frequency')  # UNCOMMENT TO PRINT TOO


#plot_stats()





ms.load_new_mesh(base_path + r'/Airplane/61.off')
# ms.generate_convex_hull()
ms.apply_filter('convex_hull')
ms.save_current_mesh('convex_hull.ply')


# https://pymeshlab.readthedocs.io/en/0.1.9/tutorials/load_mesh.html

# load a new mesh in the MeshSet, and sets it as current mesh
# the path of the mesh can be absolute or relative
ms.load_new_mesh(base_path + r'/Airplane/62.off')
print(ms.number_meshes())  # now ms contains 1 mesh

# load a new mesh, and sets it as current mesh
ms.load_new_mesh(base_path + r'/Airplane/63.off')
print(ms.number_meshes())  # now ms contains 2 meshes

# set the first mesh (id 0) as current mesh
ms.set_current_mesh(0)
# print the number of vertices of the current mesh
print(ms.current_mesh().vertex_number())

# set the second mesh (id 1) as current mesh
ms.set_current_mesh(1)
# print the number of vertices of the current mesh
print(ms.current_mesh().vertex_number())