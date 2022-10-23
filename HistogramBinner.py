import json
import matplotlib.pyplot as plt
import numpy as np
import math

path = "./database/histValues18.json"

with open(path, 'r') as f:
  data = json.load(f)


d1values = np.array([x["d1"] for x in data])
d2values = np.array([x["d2"] for x in data])
d3values = np.array([x["d3"] for x in data])
d4values = np.array([x["d4"] for x in data])
a3values = np.array([x["a3"] for x in data])
classes = [x["class"] for x in data]

print(classes)
print(np.max(d3values))
#Perform so tests in order to check if the calculations were correct
d1RangeCheck = (d1values >= 0) & (d1values <= 1)
d2RangeCheck = (d2values >= 0) & (d2values <= np.sqrt(3))
d3RangeCheck = (d3values >= 0) & (d3values <= (0.5*np.sqrt(2))) #the area spanning 2 corners and 1 corner in other edge diagonally
d4RangeCheck = (d4values >= 0) & (d4values <= 1)

print(d1RangeCheck.all())
print(d2RangeCheck.all())
# assert d3RangeCheck.all()
print(d4RangeCheck.all())

class_name = classes[1]
for x in range(len(d1values)):
  plt.hist(d1values[x], range=(0, 1), bins=int(math.sqrt(len(d1values[x]))), histtype='step')
  plt.xlabel(f"Values of d1values for class {class_name}") # TODO should e.g. be "D1"
  plt.ylabel("Frequency")
  plt.savefig(f"d1_{class_name}.png") # e.g. D1_Airplane.png
#plt.show()  

for x in range(len(d2values)):
  plt.hist(d2values[x], range=(0, np.sqrt(3)), bins=int(math.sqrt(len(d2values[x]))), histtype='step')
  plt.xlabel(f"Values of d2values for class {class_name}") # TODO should e.g. be "D1"
  plt.ylabel("Frequency")
  plt.savefig(f"d2_{class_name}.png") # e.g. D2_Airplane.png
#plt.show() 

for x in range(len(d3values)):
  plt.hist(d3values[x], range=(0, 1), bins=int(math.sqrt(len(d3values[x]))), histtype='step')
  plt.xlabel(f"Values of d3values for class {class_name}") # TODO should e.g. be "D1"
  plt.ylabel("Frequency")
  plt.savefig(f"d3_{class_name}.png") # e.g. D3_Airplane.png
#plt.show()  

for x in range(len(d4values)):
  plt.hist(d4values[x], range=(0, 1), bins=int(math.sqrt(len(d4values[x]))), histtype='step')
  plt.xlabel(f"Values of d4values for class {class_name}") # TODO should e.g. be "D1"
  plt.ylabel("Frequency")
  plt.savefig(f"d4_{class_name}.png") # e.g. D4_Airplane.png
#plt.show()  

for x in range(len(a3values)):
  plt.hist(a3values[x], range=(0, 2), bins=int(math.sqrt(len(a3values[x]))), histtype='step')
  plt.xlabel(f"Values of a3values for class {class_name}") # TODO should e.g. be "D1"
  plt.ylabel("Frequency")
  plt.savefig(f"a3_{class_name}.png") # e.g. a3_Airplane.png
#plt.show() 
