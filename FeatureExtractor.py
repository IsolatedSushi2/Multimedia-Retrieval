import open3d as o3d
from pathlib import Path
import random


def extractFeatures(mesh_path):
    features = {}
    extractOpen3dFeatures(mesh_path, features)
    #extractPyMeshFeatures(mesh_path, features)
    print(features)


def extractOpen3dFeatures(mesh_path, features):
    mesh = o3d.io.read_triangle_mesh(".\\" + str(mesh_path))


    features["orientable"] = mesh.is_orientable()
    features["watertight"] = mesh.is_watertight()

    assert features["orientable"]
    assert features["watertight"]

    features["area"] = mesh.get_surface_area()
    features["volume"] = mesh.get_volume()

def extractPyMeshFeatures(mesh_path, features):
    raise NotImplementedError()


if __name__ == "__main__":
    pathList = list(Path('./').rglob('*.off'))
    random_path = random.choice(pathList)
    extractFeatures(random_path)
