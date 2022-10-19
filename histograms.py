import matplotlib.pyplot as plt   # plots: for visualizing the data (e.g. histogram)
import numpy as np
import os                         # paths: for getting the files
import math

# Step 2.2: Statistics over the whole database
# Use the output of the filter, e.g. saved in an Excel sheet or CSV file, to find out
    # (a) what is the average shape in the database (in terms of vertex and face counts); and
    # (b) if there are significant outliers from this average (e.g. shapes having many, or few, vertices or cells).
# The best way to do this is to show a histogram counting how many shapes are in the database for every range of the property of interest (e.g., number of vertices, number of faces, shape class).



# Name        : getAllPaths
# Args:
# | folder    : the name of the folder [string]
# Result      : returns all .off file-paths in the folder
def getAllPaths(folder = '\labeledDb\LabeledDB_new'):
    all_paths = []
    # Only add paths that lead to .off files: we don't want any other files (e.g. the label files).
    for (dirpath, _, filenames) in os.walk(os.getcwd() + folder):
        for filename in filenames:
            if filename.endswith('.off'):
                all_paths.append(os.path.join(dirpath, filename))
    return all_paths


# Name        : make_histogram
# Args:
# | a         : the values to plot in a list: [1,2,2,2,1,3]
# | xlabel    : the name of the label on the x-axis
# | ylabel    : the name of the label on the y-axis
# Result      : returns all .off file-paths in the folder
def make_histogram(a, xlabel="", ylabel="", x_min=None, x_max=None):
    x_min = min(a) if x_min == None else x_min
    x_max = max(a) if x_max == None else x_max
    # FEEDBACK: we used too many bins at first. This made the whole thing look unnecessarily noisy.
    # Now we use the sqrt of the number of models for the number of bins. Looks a lot better!
    bins = int(math.sqrt(len(a)))
    average = sum(a)/len(a)

    x,y = np.histogram(a=a, bins=bins, range=(x_min, x_max))
    plt.stairs(x, y, fill=True)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.axvline(x=average, color='black') # shows a vertical line around the average
    plt.show()