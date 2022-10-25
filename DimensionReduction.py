import json
import numpy as np
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
from QueryProcessor import getClassFromPath
import seaborn as sns
with open("./database/normalized_features.json", "r") as read_content:
        features = json.load(read_content)

data = []
classes = [getClassFromPath(path) for path in features]
# print(classes)
for filename in features:
    row = features[filename]
    values = list(row.values())
    flat_list = values[:5] + [item for sublist in values[5:] for item in sublist]
    data.append(flat_list)

data = np.array(data)

X_embedded = TSNE(n_components=2, learning_rate='auto',
                  init='random', perplexity=3).fit_transform(data)
palette = sns.color_palette(None, len(set(classes)))
colorMapper = dict(zip(set(classes), palette))
print(colorMapper)
print(palette)
x = X_embedded[:, 0]
y = X_embedded[:, 1]
plt.scatter(x, y, c =[colorMapper[currClass] for currClass in classes],s=100)
plt.show()