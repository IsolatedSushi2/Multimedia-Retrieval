import json
import matplotlib.pyplot as plt
import numpy as np
import math
from pathlib import Path


def mergeFiles():
    pathList = list(Path('./database/').rglob('*.json'))
    merge_JsonFiles(pathList)

def merge_JsonFiles(files):
    result = list()
    for file in files:
        with open(file, 'r') as infile:
            result.extend(json.load(infile))

    with open("./database/histValues.json", 'w') as output_file:
        json.dump(result, output_file)


if __name__ == "__main__":
    mergeFiles()