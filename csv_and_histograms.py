# HISTOGRAMS

import matplotlib.pyplot as plt   # plots: for visualizing the data (e.g. histogram)
import numpy as np
import os                         # paths: for getting the files
import csv
import pymeshlab
import math
ms = pymeshlab.MeshSet()


# Step 2.2: Statistics over the whole database
# Use the output of the filter, e.g. saved in an Excel sheet or CSV file, to find out
    # (a) what is the average shape in the database (in terms of vertex and face counts); and
    # (b) if there are significant outliers from this average (e.g. shapes having many, or few, vertices or cells).
# The best way to do this is to show a histogram counting how many shapes are in the database for every range of the property of interest (e.g., number of vertices, number of faces, shape class).

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


# read from .csv and plot the stats
def plot_csv():
    models = read_csv()
    # (a) what is the average shape in the database (in terms of vertex and face counts);
    vertices = [m[1] for m in models]
    faces    = [m[2] for m in models]
    make_histogram(vertices,'No. of vertices','Frequency')
    make_histogram(faces,   'No. of faces'   ,'Frequency')


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

    # (b) if there are significant outliers from this average (e.g. shapes having many, or few, vertices or cells).
    # how do I... show that?