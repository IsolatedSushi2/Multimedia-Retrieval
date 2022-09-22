import pymeshlab
ms = pymeshlab.MeshSet()


base_path = r'C:\Users\Nickname5862\Desktop\UUmap\Multimedia Retrieval (MR)\labeledDb\LabeledDB_new\Airplane'
ms.load_new_mesh(base_path + r'\61.off')
# ms.generate_convex_hull()
ms.apply_filter('convex_hull')
ms.save_current_mesh('convex_hull.ply')




# https://pymeshlab.readthedocs.io/en/0.1.9/tutorials/load_mesh.html

# load a new mesh in the MeshSet, and sets it as current mesh
# the path of the mesh can be absolute or relative
ms.load_new_mesh(base_path + r'\62.off')
print(ms.number_meshes())  # now ms contains 1 mesh

# load a new mesh, and sets it as current mesh
ms.load_new_mesh(base_path + r'\63.off')
print(ms.number_meshes())  # now ms contains 2 meshes

# set the first mesh (id 0) as current mesh
ms.set_current_mesh(0)
# print the number of vertices of the current mesh
print(ms.current_mesh().vertex_number())

# set the second mesh (id 1) as current mesh
ms.set_current_mesh(1)
# print the number of vertices of the current mesh
print(ms.current_mesh().vertex_number())