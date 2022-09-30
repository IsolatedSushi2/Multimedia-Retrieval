import matplotlib.pyplot as plt   # plots: for visualizing the data (e.g. histogram)
import numpy as np
import os                         # paths: for getting the files
import csv
import pymeshlab
import math
ms = pymeshlab.MeshSet()


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

# https://pymeshlab.readthedocs.io/en/0.1.5/classes/mesh.html
# For what a mesh all contains.


def getAllPaths():
    all_paths = []
    # Only add paths that lead to .off files: we don't want the label files.
    for (dirpath, _, filenames) in os.walk(os.getcwd() + '\labeledDb\LabeledDB_new'):
        for filename in filenames:
            if filename.endswith('.off'):
                all_paths.append(os.path.join(dirpath, filename))
    # Checked and correct: it fetches ALL paths, and all paths are VALID.
    return all_paths


# Writes all the stats to the csv
def write_csv():
    all_paths = getAllPaths()
    real_paths = 0

    csvpath = os.getcwd() + '\models.csv'
    if os.path.exists(csvpath):
        os.remove(csvpath) # first "empty" it.

    for path in all_paths:
        ms.load_new_mesh(path)
        m = ms.current_mesh()

        # 1. The class of the shape = The name of the folder it is in.
        foldername = os.path.basename(os.path.dirname(path))

        # 2. Number of faces and vertices
        vertexno = m.vertex_number()
        faceno   = m.face_number() 

        # 3. Type of faces
        # After extensive testing: Upon loading any file, PyMeshLab converts all quads to triangles.
        # Thus, we don't even need this in the .csv.

        # 4. Axis-Aligned Bounding Box
        bbox = m.bounding_box()

        # 5. Path-extension to file
        # Though this is not a neccessity, it makes life so much easier.
        pathextension = path[len(os.getcwd()):]
        real_paths += 1 if os.path.exists(os.getcwd() + pathextension) else 0
 
        with open(csvpath, 'a') as file: # This is shorthand for opening and closing.
            writer = csv.writer(file)
            writer.writerow([foldername, vertexno, faceno, bbox.dim_x(), bbox.dim_y(), bbox.dim_z(), pathextension])
            # Note: putting the dim_x, dim_y and dim_z together in e.g. a list or tuple makes it a string in .csv.
    print(f"Writing succesful. Of the {len(all_paths)} paths, {real_paths} were checked and working.")


def read_csv():
    with open(os.getcwd() + '\models.csv') as file: # This is shorthand for opening and closing the file.
        reader = csv.reader(file)
        array  = list(reader)
        # everything was read as a string, and empty lines were between every entry. Parse it to the right format.
        models = [[row[0],int(row[1]),int(row[2]),float(row[3]),float(row[4]),float(row[5]),row[6]] for row in array if row != []]
    return models # would like to turn it into np.array(), but it only allows one kind of type.


# Reads from the .csv and plots whatever you like.
def make_histogram(a, xlabel, ylabel, hist_step=200, x_min=0):
    x_max = max(a)
    # FEEDBACK: we used too many bins at first. This made the whole thing look unnecessarily noisy.
    # Now we use the sqrt of the number of models for the number of bins. Looks a lot better!
    bins = int(math.sqrt(len(a)))
    average = sum(a)/len(a)

    x,y = np.histogram(a=a, bins=bins, range=(x_min, x_max))
    plt.stairs(x, y, fill=True)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    # plt.vlines(average, ymin=0, ymax=100) # TODO I WANT TO SHOW AVERAGE

    plt.show()


# read from .csv and plot the stats
def plot_csv():
    models = read_csv()
    # (a) what is the average shape in the database (in terms of vertex and face counts);
    vertices = [m[1] for m in models]
    faces    = [m[2] for m in models]
    make_histogram(vertices,'No. of vertices','Frequency')
    make_histogram(faces,   'No. of faces'   ,'Frequency')

    # (b) if there are significant outliers from this average (e.g. shapes having many, or few, vertices or cells).
    # how do I... show that?


def remesh():
    models = read_csv()

    vertices_before = [row[1] for row in models]
    vertices_after  = []

    for i in range(len(models)):
        path = os.getcwd() + models[i][-1]
        remeshpath = os.getcwd() + '\\2-3_remesh\\' + os.path.basename(models[i][-1])

        ms.clear() # to make sure we don't apply the filter to all other meshes too
        ms.load_new_mesh(path)
        m = ms.current_mesh()

        ms.apply_filter('meshing_isotropic_explicit_remeshing')
        vertices_after.append(m.vertex_number())
        ms.save_current_mesh(remeshpath)

        printeach = 40
        if i % printeach == 0:
            print(f"First {i} done")

    # Now make a histogram.
    make_histogram(vertices_before, 'Vertices before remeshing', 'Frequency')
    make_histogram(vertices_after,  'Vertices after remeshing',  'Frequency')
    # We can always make these histograms afterwards, without having to do this all again.
    # That's why we save the models! Just read them from file and print it. Way quicker.

    # DECIMATING

    # for i in range(0,20):
    #     v = i/10
    #     ms.clear()
    #     ms.load_new_mesh(all_paths[0])
    #     m = ms.current_mesh()
    #     before = m.vertex_number()
    #     ms.apply_filter('meshing_decimation_clustering', threshold=pymeshlab.Percentage(v))
    #     after = m.vertex_number()
    #     print(f"VERTEX FOR {v} THRESHOLD: {before} -> {after}")

















#                   COMMENT SECTION, DELETE AFTERWARDS


# IN REMESHING
    # worst = [-1,math.inf]
    # for i in range(len(all_paths)):
    #     if models[i][1] < worst[1]:
    #         worst = [i,models[i][1]]
    # print(f"Lowest vertices: model {worst[0]} with {worst[1]} vertices")



# https://wellsr.com/python/how-to-open-files-with-python-os/
# "It physically launches your file or application on your screen
# using the default program associated with it"
# Perhaps I can use that...?



#       FILTER REMESHING
# generate_iso_parametrization_remeshing
# meshing_isotropic_explicit_remeshing
#   might do a bit of supersampling/decimation on its own.

#       DECIMATION
# meshing_decimation_clustering
# meshing_decimation_quadric_edge_collapse



# 3. Type of faces
# print(f"FACES: {len(m.face_matrix())} vs {faceno}")
# print(f"VERTI: {len(m.vertex_matrix())} vs {vertexno}")
# THEY CORRESPOND.

# Every input in the face AND vertex matrix has 3 attributes.
# Every input in the vertix matrix represents a vertex. Of the face matrix represents a face.
# I would IMAGINE that every triplet in the vertex matrix represents the xyz-coordinates.
# And every in the face represents... indices into the vertex one? WOULD MAKE SENSE!
# How do I test it though?
# print((m.face_matrix() < np.array([vertexno])).all()) # First check: are they all lower?
# print(f"MAX: {m.face_matrix().max()} / {vertexno}") # second check: do they use the max_range? If so, no doubt. Indices.
# YES. It is always one lower (0-based), so IT IS TRUE!

    # .ply
# Importing (at least a .ply) automatically makes it triangular, even if it was not.
    # I tested this using a man-made "TriQuad.ply" file that contained 1 quad and 2 triangles.
    # Upon reading it, suddenly it duplicated all shared vertices (??) and contained 4 faces.
# Upon testing it with a cube: EXPECTED: 6 faces, 8 vertices. REAL: 6*2 faces, 8*3 vertices.
    # Matches EXACTLY my expectations. Every qaud split in half, every vertice repeated for every of the 3 neighboring faces

    # .obj
# DOESN'T duplicate the vertices anymore.

    # .off
# Even though it PBVIOUSLY supports Quad meshes (in fact, I WROTE THEM), loading them in still triangulates them.
# Thus, it is not the file format that does it, it is the Loading that does it!
# This is confirmed in the https://pymeshlab.readthedocs.io/en/0.1.5/classes/mesh.html#meshlab.Mesh.__init__
    # as it states "face_matrix: numpy.ndarray[numpy.int32[m, 3]] = array([], shape=(0, 3), dtype=int32)"
    # That's one mystery solved...