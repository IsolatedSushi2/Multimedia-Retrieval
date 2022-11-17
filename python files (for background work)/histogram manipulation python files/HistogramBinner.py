import json
import matplotlib.pyplot as plt
import numpy as np
import math
from pathlib import Path




def binfeatures():
    #a3 path (since a3 was broke in 1st computation this is solo a3)
    path = './database/combinedValues.json'
    nrbins = 10
    binnedOutPut = []
    with open(path, 'r') as f:
        data = json.load(f)
    
    pathvalues = np.array([x["path"] for x in data])
    d1values = np.array([x["d1"] for x in data])
    d2values = np.array([x["d2"] for x in data])
    d3values = np.array([x["d3"] for x in data])
    d4values = np.array([x["d4"] for x in data])
    a3values = np.array([x["a3"] for x in data])
    classes = [x["class"] for x in data]
    print(classes)
    dbins = binvalues(0, 1, nrbins)
    d2bin = binvalues(0, np.sqrt(3), nrbins)
    a3bin = binvalues(0, math.pi, nrbins)

    #create bin nr instead of value.
    d1binlist = np.digitize(d1values, dbins) -1
    d2binlist = np.digitize(d2values, d2bin) -1
    d3binlist = np.digitize(d3values, dbins) -1
    d4binlist = np.digitize(d4values, dbins) -1
    a3binlist = np.digitize(a3values, a3bin) -1

    #print(a3binlist)
    for x in range(len(a3values)):
        countValuesa3 = []
        countvaluesd1 = []
        countvaluesd2 = []
        countvaluesd3 = []
        countvaluesd4 = []
        for bin in range(nrbins):
            countValuesa3.append(np.count_nonzero(a3binlist[x] == bin))
            countvaluesd1.append(np.count_nonzero(d1binlist[x] == bin))
            countvaluesd2.append(np.count_nonzero(d2binlist[x] == bin))
            countvaluesd3.append(np.count_nonzero(d3binlist[x] == bin))
            countvaluesd4.append(np.count_nonzero(d4binlist[x] == bin))
        binnedOutPut.append({"path": pathvalues[x], "class": classes[x], "d1": countvaluesd1, "d2": countvaluesd2, "d3": countvaluesd3, "d4": countvaluesd4, "a3": countValuesa3})
    return binnedOutPut

def binvalues(min,max, nrbins):
    binlist = np.arange(min, (max+((max-min)/nrbins)), ((max-min)/nrbins))
    return binlist

def jsonPrint(binlist):
    with open("./database/binnedHistValues.json", 'w') as output_file:
        json.dump(binlist, output_file)

if __name__ == "__main__":
    binlist = binfeatures()
    jsonPrint(binlist)
    
