from ssl import PROTOCOL_TLSv1_1
import pymeshlab
import matplotlib.pyplot as plt   # plots: for visualizing the data (e.g. histogram)
import numpy as np
import os                         # paths: for getting the files
from glob import glob
import open3d as o3d
from scipy import stats
import random
import math



def make_histogram(a, xlabel, ylabel, x_min=0):
    x_max = max(a)
    print(x_max)
    x,y = np.histogram(a=a, bins=int(math.sqrt(len(a))), range=(x_min, x_max))
    plt.stairs(x, y, fill=True)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()

def make_histogram_comparison(y1, xlabel, ylabel, x_min, y2, x2label, y2label):
    x_max = max(y1)
    print(x_max)
    x,y = np.histogram(a=y1, bins=int(math.sqrt(len(y1))), range=(x_min, x_max))
    plt.stairs(x, y, fill=True)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()

    x,y = np.histogram(a=y2, bins=int(math.sqrt(len(y1))), range=(x_min, x_max))
    plt.stairs(x, y, fill=True)
    plt.xlabel(x2label)
    plt.ylabel(y2label)
    plt.show()