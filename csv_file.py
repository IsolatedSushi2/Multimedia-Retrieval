import histograms as hist
import os
import csv
import pymeshlab
ms = pymeshlab.MeshSet()

# Writes all the stats to the csv
def write_csv():
    all_paths = hist.getAllPaths()
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
    hist.make_histogram(vertices,'No. of vertices','Frequency')
    hist.make_histogram(faces,   'No. of faces'   ,'Frequency')