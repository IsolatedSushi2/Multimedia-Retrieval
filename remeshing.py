

# This file applies Remeshing for each model.


import os
import pymeshlab
import math
ms = pymeshlab.MeshSet()

import histograms as hist


# https://pymeshlab.readthedocs.io/en/latest/filter_list.html
# For what a mesh all contains.


# This does the remeshing. Given all meshes in 'original_folder', remesh them using pre-set parameters
# and save all meshes in 'remesh_folder'.
def remesh(original_folder, remesh_folder):
    all_paths = hist.getAllPaths(original_folder)
    # this gets all the full paths leading to an .off file within a folder.

    vertices_before = []
    vertices_after  = []

    # empty remeshpath if existing, or create if not
    remeshpath = os.getcwd() + '\\' + remesh_folder
    if os.path.exists(remeshpath):
        print("Cannot put remeshes in existing folder. Afraid of accidental overwriting.")
        return
    os.mkdir(remeshpath)

    printeach = math.floor(math.sqrt(len(all_paths))) # solely used for progress-report.

    for i in range(len(all_paths)):
        path = all_paths[i]

        ms.clear() # to make sure we don't apply the filter to all previous meshes again
        ms.load_new_mesh(path)
        m = ms.current_mesh()

        filename   = os.path.basename(path)                  # the file-name, e.g. "001.off"
        foldername = os.path.basename(os.path.dirname(path)) # the folder-name, e.g. "Airplane"
        newpath    = remeshpath + '\\' + foldername
        
        # if the folder doesn't exist yet, create it
        if not os.path.exists(newpath): # this is to put each model back in its original class-folder
            os.mkdir(newpath)

        vertices_before.append(m.vertex_number())
        ms.apply_filter('meshing_isotropic_explicit_remeshing', iterations=3, targetlen=pymeshlab.Percentage(1.5))
        vertices_after.append(m.vertex_number())

        ms.save_current_mesh(newpath + '\\' + filename)

        if i % printeach == 0:
            print(f"First {i} done")

    # Note: these histograms were solely used to quickly check the immediate results.
    # for the advanced histograms used in the report, see 'histogramPlotting.py' 'plotVertices' function.
    hist.make_histogram(vertices_before, 'Vertices before remeshing', 'Frequency')
    hist.make_histogram(vertices_after,  'Vertices after remeshing',  'Frequency')



if __name__ == "__main__":
    remesh(r'\labeledDB', r'\models_remesh')



# temporary function to print how many of the models have their vertices within a certain range
def printVertices(folder):
    all_paths = hist.getAllPaths(folder)
    # this gets all the full paths leading to an .off file within a folder.

    vertice_inrange = 0
    for path in all_paths:
        ms.load_new_mesh(path)
        m = ms.current_mesh()
        if m.vertex_number() <= 5000 and m.vertex_number() >= 1000:
            vertice_inrange += 1
    print(vertice_inrange / len(all_paths))

# >>> printVertices('\labeledDB')
# 0.16842105263157894
# >>> printVertices('\models_remesh')
# 0.8