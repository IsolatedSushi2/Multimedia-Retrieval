

# Does most of the plotting for 1. remeshing number-of-vertices, 2. trying out values for the remesh-parameter
# and 3. plotting the ranges of the scalar-features to see if they match our expectations


import pymeshlab
ms = pymeshlab.MeshSet()

import math
import random
import json

import histograms as hist
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm



# shows a nice gaussian plot of the 'TryValues' plot. Unused as we don't need it at all
def unused_gaussian_plot():
    # v contains the results from TryValues.
    v = [[28861, 25423, 19340, 14241, 77803, 36713, 20156, 28850, 33347, 40353, 27572, 71731, 22312, 40638, 20330, 78895, 26755, 14996, 19855, 25423, 26533, 44430, 30314, 62330, 27136, 41959, 15823, 40078, 25220, 35170, 36713, 36713, 39711, 40631, 19340, 24723, 15823, 90170, 28086, 46688, 29813, 51909, 21940, 7346, 33402, 24723, 24006, 9578, 20846, 27226, 35395, 21874, 42288, 33545, 32263, 19539, 36067, 42027, 36262, 92336],
         [7223, 6346, 4867, 3625, 19788, 8956, 4869, 7244, 8204, 9748, 7706, 18292, 5626, 11004, 5171, 19825, 9228, 4451, 5051, 6346, 6567, 11797, 7693, 15625, 7063, 10514, 4079, 10047, 6108, 8583, 8956, 8956, 9688, 10907, 4867, 5981, 4079, 22888, 8762, 11875, 7365, 13706, 5740, 1873, 8563, 5981, 5760, 2502, 6889, 8766, 8526, 5410, 10431, 8360, 7868, 4969, 8870, 10525, 8869, 23790],
         [3213, 2709, 2352, 1669, 9069, 3576, 2023, 2728, 3298, 4274, 3663, 8316, 2382, 5213, 2368, 8599, 5544, 2178, 2236, 2709, 2701, 5885, 3813, 7006, 3431, 3924, 1807, 3511, 2512, 3413, 3576, 3576, 3457, 5079, 2352, 2372, 1807, 10361, 4591, 5520, 3159, 6871, 2654, 909, 3957, 2372, 2467, 1162, 3514, 4833, 3472, 2287, 4808, 3010, 3442, 2225, 3519, 4567, 3833, 10769],
         [1801, 1540, 1456, 1003, 5108, 2037, 1128, 1672, 1887, 2387, 2258, 4740, 1366, 3114, 1371, 5046, 4314, 1359, 1304, 1540, 1546, 3760, 2514, 3896, 2170, 2398, 1091, 2536, 1407, 1957, 2037, 2037, 1958, 3015, 1456, 1331, 1091, 5823, 3191, 3094, 1741, 4774, 1560, 559, 2211, 1331, 1404, 724, 2052, 3522, 1954, 1307, 2804, 1723, 1950, 1274, 2016, 2622, 2156, 6094]]
    # Another run: [[28918, 19855, 34003, 16381, 34285, 13921, 46867, 20852, 15783, 41028, 19639, 44430, 19068, 59832, 26755, 16381, 20846, 6317, 27860, 26280, 46476, 25220, 25183, 57534, 28448, 20754, 18769, 14379, 27860, 25183, 30904, 77635, 31133, 20846, 21854, 10076, 16073, 22498, 24006, 31133, 28631, 24061, 16390, 31028, 27226, 37785, 18893, 77512, 29344, 68921, 83863, 13350, 18644, 14379, 8162, 29344, 35100, 21116, 14184, 25351], [7050, 5051, 8686, 3922, 8445, 3575, 12379, 5422, 4001, 10092, 4830, 11797, 4800, 15079, 9228, 3922, 6889, 1757, 6813, 6397, 11759, 6108, 6263, 14361, 7827, 5103, 4530, 3711, 6813, 6263, 8923, 19806, 7798, 6889, 5477, 2540, 3992, 5508, 5760, 7798, 7133, 5888, 3968, 7649, 8766, 9249, 4554, 19814, 7276, 16968, 21338, 3334, 4707, 3711, 2112, 7276, 8804, 5200, 3490, 6658], [3069, 2236, 3138, 1630, 3371, 1600, 5821, 2553, 1655, 4700, 2092, 5885, 2244, 6645, 5544, 1630, 3514, 837, 2806, 2626, 5378, 2512, 2626, 4344, 3324, 1925, 1947, 1452, 2806, 2626, 4588, 9023, 3580, 3514, 2310, 1116, 1899, 2372, 2467, 3580, 3163, 2609, 1690, 3502, 4833, 4128, 1978, 9082, 3214, 7778, 9494, 1523, 2092, 1452, 925, 3214, 3941, 2237, 1559, 3226], [1756, 1304, 1872, 917, 1916, 950, 3552, 1515, 980, 2671, 1204, 3760, 1344, 3664, 4314, 917, 2052, 533, 1562, 1484, 3101, 1407, 1534, 2644, 1962, 1104, 1098, 830, 1562, 1534, 3061, 5101, 2167, 2052, 1317, 624, 1147, 1359, 1404, 2167, 1802, 1484, 951, 1993, 3522, 2383, 1110, 5111, 1838, 4476, 5344, 843, 1188, 830, 547, 1838, 2216, 1292, 901, 2087]]
    
    bins = 14 # math.floor(math.sqrt(len(v[0]))) # == 7. 14 is nicer though.
    for i in range(len(v)):
        X = v[i]
        x,y = np.histogram(a=X,bins=bins, range=(0,10000))

        mu = np.mean(X)
        sigma = np.std(X)
        x2 = np.linspace(0, 10000, bins)
        n = norm.pdf(x2, mu, sigma)

        plt.plot(x2, n/sum(n)*sum(x), label=f"targetlen={i/2+0.5}") # so it sums to 1?
        if mu <= 10000: # to make sure the plot doesn't extend too far to the right
            plt.axvline(x=mu, color='black') # shows a vertical line around the average

        print(mu)
        # plots the default plot over the gaussian for maximum confusion yet clarity
        # plt.plot([(y[i]+y[i+1])/2 for i in range(len(y)-1)],x, label=f"targetlen={i/2+0.5}")
    plt.legend()
    plt.xlabel(f"Vertex-count after remeshing")
    plt.ylabel("Frequency")
    plt.show()



# this tries different values for the targetlen variable of the remesh operation and plots the results
def TryValues():
    all_paths = hist.getAllPaths('\labeledDB')
    # this gets all the full paths leading to an .off file within a folder.

    which = [] # which files to try - try 60 random ones
    amount = 60
    for i in range(amount):
        i = random.randint(0,len(all_paths)-1)
        path = all_paths[i]
        which.append(path)
    bins = 14 # math.floor(math.sqrt(amount)) # 14 is nicer than 7.

    vertices = []
    for p in range(4): # 0,   1, 2,   3
        pc = p/2+0.5   # 0.5, 1, 1.5, 2
        print("p=",pc)
        vertices.append([])
        for i in range(amount):
            path = which[i]

            ms.clear() # to make sure we don't apply the filter to all previous meshes too
            ms.load_new_mesh(path)
            m = ms.current_mesh()
            ms.apply_filter('meshing_isotropic_explicit_remeshing', iterations=3, targetlen=pymeshlab.Percentage(pc))
            after = m.vertex_number()
            vertices[p].append(after)

            if i % bins == 0:
                print(f"{i} done")

    for p in range(len(vertices)):
        x,y = np.histogram(a=vertices[p], bins=bins, range=(0,10000))
        plt.plot([(y[i]+y[i+1])/2 for i in range(len(y)-1)], x, label=f"targetlen={pc}")

    print(vertices) # this is then used for the unused_gaussian_plot to prevent re-running: this takes about half an hour for me to run
    plt.xlabel(f"Vertex-count after remeshing")
    plt.ylabel("Frequency")
    plt.legend()
    plt.savefig(f"targetlen_tryout.png")
    plt.show()



# this plots the ranges of the scalar-features
def plotScalarRanges():
    with open("./database/result.json", "r") as read_content:
        features = json.load(read_content)
    
    feature_names = ['surfaceArea', 'compactness', 'rectangularity', 'diameter', 'eccentricity']
    result = [[],[],[],[],[]]
    for path in features.keys():
        mesh = features[path]
        for i in range(len(feature_names)):
            feature_value = mesh[feature_names[i]]
            result[i].append(feature_value)

    # ranges = [(0,None), (1,None), (0,1), (1,math.sqrt(2)), (1,None)]
    for i in range(len(feature_names)):
        hist.make_histogram(result[i], f"values for {feature_names[i]}", "Frequency")

    # for min-max ranges
    for i in range(len(feature_names)):
        print(f"{feature_names[i]}: {min(result[i])} -- {max(result[i])}")



# this plots the number of vertices of the models before and after remeshing
def plotVertices(plotSeparate = False):
    all_before_paths = hist.getAllPaths(r'\labeledDB')
    all_after_paths  = hist.getAllPaths(r'\models_final')

    # vertices_before = []
    # vertices_after  = []
    # for path in all_before_paths:
    #     ms.load_new_mesh(path)
    #     m = ms.current_mesh()
    #     vertices_before.append(m.vertex_number())
    # for path in all_after_paths:
    #     ms.load_new_mesh(path)
    #     m = ms.current_mesh()
    #     vertices_after.append(m.vertex_number())
    # print(vertices_before)
    # print(vertices_after)
    vertices_before = [5400, 5619, 5519, 6797, 6448, 7739, 7651, 5583, 6701, 5631, 5849, 5228, 5109, 5044, 8679, 5923, 6587, 7470, 6689, 7351, 8064, 6370, 8299, 6376, 6850, 8388, 7038, 7470, 8210, 7654, 7877, 8640, 5867, 8216, 7236, 7355, 8504, 8167, 6154, 6881, 25273, 24473, 24484, 25494, 25193, 25108, 25491, 20000, 25211, 25431, 24615, 21774, 15000, 16501, 16780, 15832, 15315, 15000, 17117, 17453, 1663, 1663, 1663, 3182, 3614, 3587, 2623, 2568, 2568, 8759, 5192, 10400, 1512, 2910, 14994, 14992, 14872, 14127, 14956, 2200, 3478, 7849, 3158, 4501, 6475, 4219, 5519, 11790, 3714, 4280, 3158, 6351, 6164, 3638, 5054, 5970, 2135, 8946, 9015, 2497, 9252, 25125, 15516, 25467, 27824, 26798, 27439, 23976, 5197, 8263, 25230, 26985, 10852, 26437, 25768, 23395, 27726, 25145, 26558, 27118, 8499, 15724, 9652, 8653, 9261, 14052, 11421, 10500, 10301, 8456, 8050, 13628, 10748, 5794, 10043, 13463, 14372, 9153, 12326, 10121, 15198, 15002, 15037, 15246, 15087, 15209, 15137, 15070, 15127, 15006, 15227, 14751, 7349, 9602, 15136, 9076, 6270, 15064, 15161, 15165, 7121, 5255, 6656, 5061, 6076, 5216, 5216, 5592, 5245, 7573, 6264, 5440, 10186, 7498, 5250, 4845, 4439, 5096, 5121, 6833, 6938, 8078, 13331, 4712, 10436, 2087, 14680, 8411, 9490, 9239, 4315, 8618, 9757, 9009, 11312, 5538, 7268, 1480, 3911, 3703, 7016, 4164, 3414, 6288, 5399, 2394, 2028, 5176, 3110, 7420, 2858, 1554, 2496, 7407, 2850, 8771, 7413, 1857, 2895, 2375, 7242, 10283, 11413, 4685, 2489, 6607, 7628, 8603, 14084, 7500, 13766, 6991, 7314, 8471, 8524, 7112, 7553, 9564, 8647, 1515, 4706, 9508, 10999, 5614, 13703, 5691, 5631, 15223, 15910, 15385, 15477, 10050, 15700, 5641, 5676, 15154, 10098, 8441, 11015, 2639, 14995, 14991, 14991, 14812, 14999, 14995, 14937, 14994, 14999, 15000, 15000, 14997, 14942, 14997, 14995, 15505, 11533, 19403, 15000, 14997, 5944, 7251, 15493, 3101, 1343, 6325, 11906, 6164, 6144, 7747, 11051, 7812, 10466, 10932, 15201, 14126, 9124, 9594, 8017, 9200, 4487, 4491, 3906, 4407, 4478, 4794, 5202, 6104, 5110, 5508, 4284, 4298, 3963, 3804, 4463, 4478, 5201, 6198, 3942, 4457, 13926, 9802, 9270, 15082, 13206, 13714, 13705, 13375, 13588, 13579, 12696, 10543, 13581, 13929, 14384, 10100, 13883, 14587, 13930, 10082, 13826, 10096, 10879, 14509, 10233, 11090, 12647, 10752, 12561, 12500, 14905, 10141, 13867, 12831, 9480, 12500, 12543, 12175, 13324, 9548, 14859, 14476, 13434, 13548, 13514, 10637, 3900, 11202, 13606, 13920, 14599, 6684, 10556, 14872, 11762, 12568, 15169, 6684, 6923, 9356]
    vertices_after  = [1986, 1580, 1533, 2079, 1595, 2352, 2242, 1706, 1902, 1964, 1651, 1561, 1484, 1623, 2180, 1898, 1609, 1752, 1859, 2012, 2499, 2293, 2493, 2272, 2245, 2798, 2693, 2270, 2035, 2604, 2515, 2616, 2282, 2194, 1931, 2473, 2309, 2853, 2300, 2029, 4575, 5465, 3973, 4813, 4751, 5591, 5952, 4589, 3561, 5482, 5310, 4404, 4569, 3633, 3981, 4617, 5123, 4307, 4553, 3247, 3324, 3526, 3598, 4724, 4805, 4783, 5106, 3079, 2916, 2227, 3506, 3502, 2271, 2711, 2095, 2091, 2604, 3900, 3909, 3116, 1219, 2368, 1522, 1837, 2261, 1811, 2032, 2661, 1542, 1628, 1522, 2424, 1942, 1594, 1854, 1638, 2394, 3969, 2359, 3644, 4828, 6308, 5395, 4899, 5818, 4519, 4491, 5180, 6868, 5150, 5922, 5068, 5739, 5162, 5216, 5882, 4994, 4973, 5035, 5310, 3316, 3424, 2997, 2870, 3129, 3600, 3285, 3152, 3349, 2912, 2722, 3468, 3413, 2626, 3194, 3586, 3801, 2905, 3210, 3197, 7870, 9067, 6645, 8690, 10768, 9475, 9448, 7862, 8741, 4535, 7539, 9489, 8065, 8599, 7315, 7006, 9159, 11075, 10761, 10355, 2623, 2275, 2512, 2225, 2380, 2371, 2371, 2353, 2387, 2700, 2468, 2446, 3140, 2821, 2239, 2076, 1998, 2149, 2281, 2705, 3856, 2897, 4597, 3053, 3310, 3727, 3238, 3860, 3799, 2302, 4170, 3580, 3345, 3415, 3867, 3319, 3326, 3124, 3081, 3078, 1782, 1405, 1250, 1791, 1688, 921, 908, 1444, 1156, 1856, 1126, 843, 919, 1788, 1154, 2116, 1746, 834, 1130, 897, 2727, 3689, 3832, 3940, 3453, 3199, 2844, 2822, 3221, 2848, 3872, 2936, 3371, 3301, 3336, 2604, 3163, 2662, 3996, 2654, 2551, 2603, 2398, 1836, 3208, 2399, 3902, 4440, 4413, 5132, 3395, 2603, 4847, 3035, 3024, 3754, 4523, 2905, 2266, 2040, 9097, 9068, 9023, 7921, 7001, 7706, 7151, 8971, 9077, 9065, 9063, 8316, 9084, 9146, 9035, 6197, 6259, 7774, 9082, 9183, 1741, 1864, 3162, 1478, 2173, 1453, 2652, 1651, 1702, 1853, 2660, 3749, 2444, 2592, 3405, 3082, 2083, 2646, 1749, 1974, 1541, 1527, 1697, 1449, 1700, 1629, 1660, 1709, 1730, 1612, 1545, 1336, 1634, 1627, 1573, 1565, 1738, 1939, 1409, 1560, 5559, 3923, 3368, 4326, 4063, 4994, 4782, 4965, 4508, 3460, 5998, 3924, 5730, 4278, 4807, 3132, 4696, 3543, 5558, 3511, 4212, 3413, 3577, 4249, 3736, 3472, 3695, 3718, 3540, 3735, 3784, 3519, 4726, 3029, 3303, 3970, 3822, 3848, 3808, 3369, 4787, 5007, 3203, 4395, 5372, 4350, 3890, 5224, 5336, 4314, 4655, 3842, 4130, 4235, 3368, 4905, 4369, 3955, 3904, 5520]
    # these values are obtained from the code above. This is to prevent recalculation every time, as it takes a while

    x_max = max(vertices_before + vertices_after)

    # FEEDBACK: we used too many bins at first. This made the whole thing look unnecessarily noisy.
    # Now we use the sqrt of the number of models for the number of bins. Looks a lot better!
    bins = int(math.sqrt(len(vertices_before)))
    average1 = sum(vertices_before) / len(vertices_before)
    average2 = sum(vertices_after)  / len(vertices_after)

    # whether to plot the before- and after- in different plots or the same
    if(plotSeparate):
        x,y = np.histogram(a=vertices_before, bins=bins, range=(0, x_max))
        plt.stairs(x, y, fill=True, alpha=1)
        plt.xlabel("Vertices before remeshing")
        plt.ylabel("Frequency")
        plt.ylim(top=150)
        plt.axvline(x=average1, color='blue') # shows a vertical line around the average
        plt.show()

        x,y = np.histogram(a=vertices_after, bins=bins, range=(0, x_max))
        plt.stairs(x, y, fill=True, alpha=1)
        plt.xlabel("Vertices after remeshing")
        plt.ylabel("Frequency")
        plt.ylim(top=150)
        plt.axvline(x=average2, color='blue') # shows a vertical line around the average
        plt.show()
    else:
        x,y = np.histogram(a=vertices_before, bins=bins, range=(0, x_max))
        plt.stairs(x, y, fill=True, alpha=0.7)
        x,y = np.histogram(a=vertices_after, bins=bins, range=(0, x_max))
        plt.stairs(x, y, fill=True, alpha=0.7)
        
        plt.legend(["Before remeshing", "After remeshing"])
        plt.xlabel("Vertex-count")
        plt.ylabel("Frequency")
        plt.axvline(x=average1, color='blue') # shows a vertical line around the average
        plt.axvline(x=average2, color='red') # shows a vertical line around the average
        plt.show()
