Overleaf:
radretifyo@vusra.com
Password


The .csv has format
1) shapeclass, as string;
2) vertex no., as int;
3) face no., as int;
4) boundingbox_x, as float;
5) boundingbox_y, as float;
6) boundingbox_z, as float;
7) path-extension, as string.
Note that "Is_triangle_or_quad" is not needed, as pymeshlab converts all to triangles implicitly anyway.
For the path-extension, simply stand in the git repository and use os.getcwd() + path-extension to get the path to the model. os.getcwd() fetches the current path.