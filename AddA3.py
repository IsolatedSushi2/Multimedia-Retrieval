import json
from attr import NOTHING
import matplotlib.pyplot as plt
import numpy as np
import math
from pathlib import Path


def addA3Files():
    path1 = './database/a3histValues.json'
    path2 = './database/disthistValues.json'

    
    with open(path1, 'r') as f:
        data1 = json.load(f)
    
    with open(path2, 'r') as g:
        data2 = json.load(g)

    pathvaluesa3 = np.array([x["path"] for x in data1])
    a3values = np.array([x["a3"] for x in data1])
    classes = [x["class"] for x in data1]

    pathvaluesdist = np.array([x["path"] for x in data2])
    d1values = np.array([x["d1"] for x in data2])
    d2values = np.array([x["d2"] for x in data2])
    d3values = np.array([x["d3"] for x in data2])
    d4values = np.array([x["d4"] for x in data2])

    binnedOutPut=[]
    for path1 in range(len(pathvaluesa3)):
        #print(pathvaluesa3[path1])
        for path2 in range(len(pathvaluesdist)):
            if pathvaluesa3[path1] == pathvaluesdist[path2]:
                binnedOutPut.append({"path": pathvaluesa3[path1], "class": classes[path1], "d1": d1values[path2].tolist(), "d2": d2values[path2].tolist(), "d3": d3values[path2].tolist(), "d4": d4values[path2].tolist(), "a3": a3values[path1].tolist()})
    with open("./database/combinedValues.json", 'w') as output_file:
        json.dump(binnedOutPut, output_file)            

if __name__ == "__main__":
    addA3Files()