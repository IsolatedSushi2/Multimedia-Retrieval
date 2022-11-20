This MRsystem can be run by simply running the Demo.py file. This file will represent the user with a small GUI. Please use the Meshes in the Models_final file (the standard map) for retrieval. When using a model that is not in this map please use Read Vector from File, this is cause the given filepath of meshes is being used in retrieval in the database. 

The ANN, and the DR + ANN are computed slowly. This is because we do not safe the Annoy or the TSNE object. Meaning we need to recompute this. Ofcourse this could be preprocessed and safed, we simply do not do this.

There are also non Demo files and other files not used in the demo, These files where mostly used for tinkering, testing, checking, making minor adjustments or simply because we needed to plot stuff for the report.

Dependencies needed for running the program: (pip installable)
annoy,			pymeshlab
matplotlib,		sklearn
numpy,			json
open3d,			os
pandas,			colorcet
seaborn,		scipy



This program is made for an assignment for Multimedia Retrieval, a master course given by prof. dr. Alexandru C. Telea at Utrecht University.

Program made by students:
Nick Schuitemaker 	stnr: 6259855
Ben Veldhuijzen 	stnr: 5981778
Simen van Herpt 	stnr: 5955106