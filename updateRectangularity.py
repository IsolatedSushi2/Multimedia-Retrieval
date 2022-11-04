import json
import FeatureExtractor
import open3d as o3d


exit()
with open("./database/normalized_features_old.json", "r") as read_content:
    features = json.load(read_content)

for pathName in features:
    featureValues = features[pathName]
    mesh = o3d.io.read_triangle_mesh(".\\" + str(pathName))

    features[pathName]["rectangularity"] = FeatureExtractor.getApproximatedVolume(mesh) / mesh.get_axis_aligned_bounding_box().volume()
    print("rectangularity", features[pathName]["rectangularity"])

with open("./database/normalized_features.json", "w") as fp:
    json.dump(features, fp)