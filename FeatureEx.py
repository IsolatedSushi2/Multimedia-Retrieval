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

#number of samples (100000)
n = 100000

def getPaths():
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
    return all_paths

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

# Function to find distance in 3d points
def distance(x1, y1, z1, x2, y2, z2):
      
    d = math.sqrt(math.pow(x2 - x1, 2) +
                math.pow(y2 - y1, 2) +
                math.pow(z2 - z1, 2)* 1.0)
    return d


def extract_a3(pcd):
    #hist init
    hist_a3 = []
    #for all points get random points
    for x in range(n):
        r1 = random.randint(0, n-1)
        r2 = random.randint(0, n-1)
        r3 = random.randint(0, n-1)

        pt1 = pcd.points[r1]
        
        #make sure r1 =/= r2
        while r1 == r2:
            r2 = random.randint(0, n-1)

        pt2 = pcd.points[r2]

        #make sure r3 =/= r1 or r2
        while r3 == r2 or r3 == r1:
            r3 = random.randint(0, n-1)
        pt3 = pcd.points[r3]
        #make line segments
        ba = pt1 - pt2
        bc = pt3 - pt2  
        #get cosine angle normalized value in Radians so....... x 180 / pi to get degrees
        cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
        angle_cos = np.arccos(cosine_angle)
        #does (x * 180 / pi) to get radian -> degrees
        angle = np.degrees(angle_cos)
        #append angle value to list
        hist_a3.append(angle)
    
    #make histogram from list of angles
    make_histogram(hist_a3,'angle between 3 points in degrees','Frequency')

#distance between 1 point and bary center.
def extract_d1(pcd):
    #histogram init
    hist_d1 = []
    #for all sample points
    for x in range(n):
        pt1 = pcd.points[x]
        #append distance pt1 to 0,0,0 (barry center after normalization)
        hist_d1.append(distance(pt1[0],pt1[1],pt1[2],0,0,0))

    #print(pointlist)
    #print(hist_d1)
    make_histogram(hist_d1,'Distance of random vertices to bary center','Frequency')

#distance between 2 random points on mesh
def extract_d2(pcd):
    #histogram init
    hist_dist = []
    #pointcloud init for visualization
    #point list init
    #pointlist = []
    #pointCloud = o3d.geometry.PointCloud()
    
    for x in range(n):
        r1 = random.randint(0, n-1)
        pt1 = pcd.points[r1]
        r2 = random.randint(0, n-1)
        if r1 == r2:
            print("SKIPPED")
            continue
        else:
            pt2 = pcd.points[r2]
            hist_dist.append(distance(pt1[0],pt1[1],pt1[2],pt2[0],pt2[1],pt2[2]))
            
            #append points to list for visualization
            #pointlist.append(pt1)
            #pointlist.append(pt2)
    
    #visualization of random points
    #pointCloud.points = o3d.utility.Vector3dVector(pointlist)
    #pointCloud.paint_uniform_color([0,0,1])
    #o3d.visualization.draw_geometries([pointCloud])
    
    #print(pointlist)
    #print(hist_dist)
    make_histogram(hist_dist,'Distance of 2 random vertices','Frequency')

'''
def extract_d3():
    #square root of area of triangle given by 3 random vertices

'''



def startup():
    #get N sample points for path
    path = getPaths()[2]
    m = o3d.io.read_triangle_mesh(path)
    pcd = m.sample_points_uniformly(number_of_points=n)

    extract_a3(pcd)
    #extract_d1(pcd)
    #extract_d2(pcd)
    #extract_d3(pcd)
    #extract_d4(pcd)

if __name__ == "__main__":
    startup()