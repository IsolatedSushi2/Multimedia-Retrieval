import os                         # paths: for getting the files
import pymeshlab
ms = pymeshlab.MeshSet()

import math

import histograms as hist
import csv_file

# Step 2.1: Analyzing a single shape
# Start building a simple filter that checks all shapes in the database. The filter should output, for each shape
    # the class of the shape
    # the number of faces and vertices of the shape
    # the type of faces (e.g. only triangles, only quads, mixes of triangles and quads)
    # the axis-aligned 3D bounding box of the shapes
# Shape class: All shapes in the Princeton and Labeled PSB Datasets come with a class label.
# For the Labeled PSB database, use the classification which divides shapes into 19 classes (aircraft, animal, etc).

# Step 2.2: Statistics over the whole database
# Use the output of the filter, e.g. saved in an Excel sheet or CSV file, to find out
    # (a) what is the average shape in the database (in terms of vertex and face counts); and
    # (b) if there are significant outliers from this average (e.g. shapes having many, or few, vertices or cells).
# The best way to do this is to show a histogram counting how many shapes are in the database for every range of the property of interest (e.g., number of vertices, number of faces, shape class).

# https://pymeshlab.readthedocs.io/en/latest/filter_list.html
# For what a mesh all contains.

# e.g. original_folder='\labeledDb', remesh_folder='models_remesh'
def remesh(original_folder, remesh_folder):
    all_paths = hist.getAllPaths(original_folder)
    # this gets all the full paths leading to an .off file within a folder.

    vertices_before = []
    vertices_after  = []

    # empty remeshpath if existing, or create if not
    remeshpath = os.getcwd() + '\\' + remesh_folder
    if os.path.exists(remeshpath):
        print("Cannot put remeshes in existing folder. Afraid of messing everything up.")
        return
    os.mkdir(remeshpath)

    printeach = math.floor(math.sqrt(len(all_paths)))

    for i in range(len(all_paths)):
        path = all_paths[i]

        ms.clear() # to make sure we don't apply the filter to all previous meshes too
        ms.load_new_mesh(path)
        m = ms.current_mesh()

        filename   = os.path.basename(path)
        foldername = os.path.basename(os.path.dirname(path)) # the folder-name, e.g. "Airplane"
        newpath    = remeshpath + '\\' + foldername
        
        # if the folder doesn't exist yet, create it
        if not os.path.exists(newpath):
            os.mkdir(newpath)

        vertices_before.append(m.vertex_number())
        ms.apply_filter('meshing_isotropic_explicit_remeshing', iterations=3, targetlen=pymeshlab.Percentage(1.5))
        # while m.vertex_number() > 5000:
        #     ms.apply_filter('meshing_decimation_clustering', threshold=pymeshlab.Percentage(1.5))
        vertices_after.append(m.vertex_number())

        ms.save_current_mesh(newpath + '\\' + filename)

        if i % printeach == 0:
            print(f"First {i} done")

    # Now make a histogram.
    hist.make_histogram(vertices_before, 'Vertices before remeshing', 'Frequency')
    hist.make_histogram(vertices_after,  'Vertices after remeshing',  'Frequency')
    # We can always make these histograms afterwards, without having to do this all again.
    # That's why we save the models! Just read them from file and print it. Way quicker.


def printVertices(folder):
    all_paths = hist.getAllPaths(folder)
    # this gets all the full paths leading to an .off file within a folder.

    vertice_inrange = 0
    for path in all_paths:
        ms.load_new_mesh(path)
        m = ms.current_mesh()
        if m.vertex_number() <= 5000:
            vertice_inrange += 1
    print(vertice_inrange / len(all_paths))


# TEMPORARY TRY FUNCTION, TRIES OUT MULTIPLE VALUES TO SEE WHICH ONE IS BEST
def tryDecimate():

    # DECIMATING
    models = csv_file.read_csv()
    vertices_before = [row[1] for row in models]

    for i in range(1,5):
        vertices_after  = []

        for model in models:
            if model[1] > 6000: # only try decimate on > 6000 vertices
                v = 1.5 + (1.5/5)*i # 0.3, 0.6, 0.9, 1.2, 1.5
                ms.clear()
                ms.load_new_mesh(os.getcwd() + model[-1])
                m = ms.current_mesh()
                # vertices_before.append(m.vertex_number())
                ms.apply_filter('meshing_decimation_clustering', threshold=pymeshlab.Percentage(v))
                vertices_after.append(m.vertex_number())

        hist.make_histogram(vertices_before, 'Vertices before decimation', 'Frequency')
        hist.make_histogram(vertices_after,  f'Vertices after decimation, threshold = {v}', 'Frequency')
