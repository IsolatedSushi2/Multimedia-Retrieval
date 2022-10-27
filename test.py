import json 
import pandas
from FeatureExtractor import extractFeatures

# Opening JSON file
with open('./BinnedHistValues/binnedHistValues.json',) as f:
    # returns JSON object as 
    # a dictionary
    binnedDatadata = json.load(f)

featureVectors = pandas.read_csv('./database/features.csv', index_col=[0])

featureDict = {}

for row in binnedDatadata:
    featureDict[row["path"]] = {"d1": row["d1"], "d2": row["d2"], "d3": row["d3"], "d4": row["d4"], "a3": row["a3"]}
    featureDict[row["path"]] = {**extractFeatures(row["path"]), **featureDict[row["path"]]}
    print(row["path"])

with open('result.json', 'w') as fp:
    json.dump(featureDict, fp)