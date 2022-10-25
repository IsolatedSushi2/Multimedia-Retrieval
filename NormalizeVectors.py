def normalizeFeatures():
    normalizedFeatures = {}
    with open("./database/result.json", "r") as read_content:
        features = json.load(read_content)

    surfaceArea = stats.zscore(np.asarray([features[filename]["surfaceArea"] for filename in features]))
    compactness = stats.zscore(np.asarray([features[filename]["compactness"] for filename in features]))
    rectangularity = stats.zscore(np.asarray([features[filename]["rectangularity"] for filename in features]))
    diameter = stats.zscore(np.asarray([features[filename]["diameter"] for filename in features]))
    eccentricity = stats.zscore(np.asarray([features[filename]["eccentricity"] for filename in features]))

    for i, filename in enumerate(features):
        d1 = np.array(features[filename]["d1"]) / 100000
        d2 = np.array(features[filename]["d2"]) / 100000
        d3 = np.array(features[filename]["d3"]) / 100000
        d4 = np.array(features[filename]["d4"]) / 100000
        a3 = np.array(features[filename]["a3"]) / 100000

        features[filename]["d1"] = d1.tolist()
        features[filename]["d2"] = d2.tolist()
        features[filename]["d3"] = d3.tolist()
        features[filename]["d4"] = d4.tolist()
        features[filename]["a3"] = a3.tolist()

        features[filename]["surfaceArea"] = surfaceArea[i]
        features[filename]["compactness"] = compactness[i]
        features[filename]["rectangularity"] = rectangularity[i]
        features[filename]["diameter"] = diameter[i]
        features[filename]["eccentricity"] = eccentricity[i]

    with open("./database/normalized_features.json", "w") as write_content:
        features = json.dump(features, write_content)

    exit()



    #https://stackoverflow.com/questions/45834276/numpyzero-mean-data-and-standardization
    normFeatures = [stats.zscore(np.asarray(features[column])) for column in features.columns]

    normDict = dict(zip(features.columns, normFeatures))
    normalizedDF = pandas.DataFrame(normDict, index=features.index)
    normalizedDF.to_csv("./database/normalized_features.csv")
