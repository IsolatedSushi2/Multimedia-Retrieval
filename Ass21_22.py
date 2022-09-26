import matplotlib.pyplot as plt   # plots: for visualizing the data (e.g. histogram)
import numpy as np
import os                         # paths: for getting the files
import csv
import pymeshlab
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


base_path = os.getcwd() + '\labeledDb\LabeledDB_new'

all_paths = []
# Only add paths that lead to .off files: we don't want the labels.
for (dirpath, dirnames, filenames) in os.walk(base_path):
    for filename in filenames:
        if filename.endswith('.off'):
            all_paths.append(os.path.join(dirpath, filename))
# Checked and correct: it fetches ALL paths, and all paths are VALID.


# class Model:
#     def __init__(self, shapeclass, vertexno, faceno, boundingbox):
#         self.shapeclass  = shapeclass
#         self.vertexno    = vertexno
#         self.faceno      = faceno
#         self.boundingbox = boundingbox

# https://pymeshlab.readthedocs.io/en/0.1.5/classes/mesh.html
# For what a mesh all contains.

def find_stats():
    for path in all_paths:
        ms.load_new_mesh(path)
        m = ms.current_mesh()

        # 1. The class of the shape = The name of the folder it is in.
        foldername = os.path.basename(os.path.dirname(path))

        # 2. Number of Faces and Vertices
        vertexno = m.vertex_number()
        faceno   = m.face_number() 

        # 3. Type of faces
        # After extensive testing: Upon loading any file, PyMeshLab converts all quads to triangles.
        # Thus, we don't even need this in the .csv.

        # 4. Axis-Aligned Bounding Box
        bbox = m.bounding_box() # I assume it is axis-aligned.

        with open(os.getcwd() + '\models.csv', 'a') as file: # This is the same as Opening and Closing.
            writer = csv.writer(file)
            writer.writerow([foldername, vertexno, faceno, bbox.dim_x(), bbox.dim_y(), bbox.dim_z()])
            # Note: putting the dim_x, dim_y and dim_z together in e.g. a list or tuple makes it a string in .csv.

find_stats()


# TODO:
# 1. Put in a .csv
# 2. plot the vertex and face counts. I have already done that before!

# But also... deliver the exercise for the other course!



#                   COMMENT SECTION

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