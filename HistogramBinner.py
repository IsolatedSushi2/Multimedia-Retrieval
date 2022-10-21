import json
import matplotlib.pyplot as plt
import numpy as np

path = "./database/histValues.json"

with open(path, 'r') as f:
  data = json.load(f)


d1values = np.array([x["d1"] for x in data])
d2values = np.array([x["d2"] for x in data])
d3values = np.array([x["d3"] for x in data])
d4values = np.array([x["d4"] for x in data])
classes = [x["class"] for x in data]

print(classes)

#Perform so tests in order to check if the calculations were correct
d1RangeCheck = (d1values >= 0) & (d1values <= np.sqrt(3) / 2)
d2RangeCheck = (d2values >= 0) & (d1values <= np.sqrt(3))
#d3RangeCheck = (d3values >= 0) & (d1values <= np.sqrt(3) / 2) the area spanning 2 corners and 1 corner in other edge diagonally
d4RangeCheck = (d4values >= 0) & (d1values <= 1)

print(d1RangeCheck.all())
print(d2RangeCheck.all())
# assert d3RangeCheck.all()
print(d4RangeCheck.all())


plt.hist(d1values[0], range=(0, np.sqrt(3) / 2))
plt.show()
