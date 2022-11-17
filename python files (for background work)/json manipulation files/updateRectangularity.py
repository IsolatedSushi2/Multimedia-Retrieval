import json
import FeatureExtractor
import open3d as o3d
from scipy import stats
import numpy as np

with open("./database/normalized_features.json", "r") as read_content:
    features = json.load(read_content)

for pathName in features:
    featureValues = features[pathName]
    mesh = o3d.io.read_triangle_mesh(".\\" + str(pathName))

    surfaceArea = mesh.get_surface_area()

    features[pathName]["rectangularity"] = FeatureExtractor.getApproximatedVolume(mesh) / mesh.get_axis_aligned_bounding_box().volume()
    features[pathName]["compactness"] = FeatureExtractor.getCompactness(surfaceArea, FeatureExtractor.getApproximatedVolume(mesh))
    print(pathName)
    print("rectangularity", features[pathName]["rectangularity"])
    print("compactnes", features[pathName]["compactness"])

Normcompactness = stats.zscore(np.asarray([features[filename]["compactness"] for filename in features]))
Normrectangularity = stats.zscore(np.asarray([features[filename]["rectangularity"] for filename in features]))

for i, filename in enumerate(features):
    features[filename]["compactness"] = Normcompactness[i]
    features[filename]["rectangularity"] = Normrectangularity[i]
    print(filename, Normcompactness[i], Normrectangularity[i] , "normcomp , normrect")

#print("rectangularityNorm", features["models_final\Airplane\70.off"]["rectangularity"])
#print("compactnesNorm", features["models_final\Airplane\70.off"]["compactness"])
    
with open("./database/normalized_features_NEW.json", "w") as fp:
    json.dump(features, fp)