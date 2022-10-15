import os                         # paths: for getting the files
import pymeshlab
ms = pymeshlab.MeshSet()

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


def remesh(remesh_folder = 'models_remesh'):
    models = csv_file.read_csv()

    vertices_before = [row[1] for row in models]
    vertices_after  = []

    # empty remeshpath if existing, or create if not
    remeshpath = os.getcwd() + '\\' + remesh_folder
    if os.path.exists(remeshpath):
        print("Cannot put remeshes in existing folder. Afraid of messing everything up.")
        return
    os.mkdir(remeshpath)

    for i in range(len(models)):
        model = models[i]

        path = os.getcwd() + model[-1]
        remeshpath = os.getcwd() + '\\' + remesh_folder + '\\' + os.path.basename(model[-1])

        ms.clear() # to make sure we don't apply the filter to all other meshes too
        ms.load_new_mesh(path)
        m = ms.current_mesh()

        # if model[1] > 6000:
        #     ms.apply_filter('meshing_decimation_clustering', threshold=pymeshlab.Percentage(1.5))
        ms.apply_filter('meshing_isotropic_explicit_remeshing', iterations=3, targetlen=pymeshlab.Percentage(1.5))
        # ms.apply_filter('generate_resampled_uniform_mesh', cellsize=pymeshlab.Percentage(p), mergeclosevert=True)
        vertices_after.append(m.vertex_number())
        ms.save_current_mesh(remeshpath)

        printeach = 10
        if i % printeach == 0:
            print(f"First {i} done")

    # Now make a histogram.
    hist.make_histogram(vertices_before, 'Vertices before remeshing', 'Frequency')
    hist.make_histogram(vertices_after,  'Vertices after remeshing',  'Frequency')
    # We can always make these histograms afterwards, without having to do this all again.
    # That's why we save the models! Just read them from file and print it. Way quicker.


# generate_resampled_uniform mesh: cellsize = 1, no change whatsoever.
# generate_resampled_uniform mesh: cellsize = 2, no change whatsoever.



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
