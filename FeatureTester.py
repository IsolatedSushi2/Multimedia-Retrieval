from glob import glob
import open3d as o3d
from scipy import stats
import numpy as np
from matplotlib import pyplot as plt


def main():
    classPaths = list(glob("./labeledDb/LabeledDB_new/*"))
    classNames = [name.split('\\')[-1] for name in classPaths]
    featureToTest = SurfaceOverVolumeRatio

    all_class_features = [GetFeatureForClass(path, featureToTest) for path in classPaths[2:3]]

    ShowAllClasses(all_class_features, classNames, featureToTest.__name__)

    


def ShowAllClasses(all_class_features, classNames, funcName):
    for i in range(len(all_class_features)):
        feature_array = all_class_features[i]

        kde = stats.gaussian_kde(feature_array)
        dist_space = np.linspace(np.min(feature_array), np.max(feature_array), 100)
        
        plt.plot(dist_space, kde(dist_space), label = classNames[i])
    
    plt.legend()
    plt.savefig(funcName + "_feature_test.png")

    plt.show()




def GetFeatureForClass(classPath, featureFunc):
    mesh_paths = glob(classPath + "/*.off")

    features = []
    for path in mesh_paths:
        mesh = o3d.io.read_triangle_mesh(path)

        featureVal = featureFunc(mesh)
        if(featureVal is not None):
            features.append(featureVal)

    feature_array = np.asarray(features)
    return feature_array


def SurfaceOverVolumeRatio(mesh):
    if not mesh.is_watertight():
        return None
    
    return mesh.get_surface_area() / mesh.get_volume()


if __name__ == "__main__":
    main()
