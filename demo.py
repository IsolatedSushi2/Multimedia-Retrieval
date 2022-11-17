from fileinput import filename
import tkinter as tk
import os
from tkinter import filedialog
from tkinter import ttk
from MultiView import *
from QueryProcessorDemo import *
from ANNDemo import *
from DRDemo import *

#init global and local variables
fileLocation = "unknown"
init = True
meshlist = []
classes = None
X_embedded = None
distanceMeasure = 'F'
y = 1

#tkinter code to get and set value
def get_current_value():
    return '{: .2f}'.format(current_value.get())

#Event that changes the value of the K-label
def slider_changed(event):
    current_value_label.configure(text=('Current Value for K:', get_current_value()))

#event that gets the new distance value (F,ANN,DR+ANN)
def distValueUpdate(event):
    distmeasure.get()

#code that sets the file location and starts at correct folder (models_final/)
def addFile():
    global fileLocation
    fileLocation = filedialog.askopenfilename(initialdir="./models_final/", title="Select File",
    filetypes=(("OFF files", "*.off"),("all files", "*, *")))
    base_path = os.getcwd()
    fileLocation = os.path.relpath(fileLocation, base_path)

#function that gets called on the RUN button
def runApp():
    #global variables needed
    global init
    global meshlist
    global y
    global X_embedded
    global classes
    global paths
    acc = 0
    #error when you haven't selected a file print this
    if fileLocation == "unknown":
        print("error no file")
        mylist.insert(1, "error no file selected")
    else:
        #print some stuff in the GUI terminal
        curval = current_value.get()
        FileboolVal = Filebool.get()
        print("running on: ", fileLocation)
        print("current K = ", curval)
        mylist.insert((1+(y*100)-1), ("running On file", fileLocation, "with current K = ", curval))
        #run F, ANN , DR + ANN functions accoridng to the distmeasure setting
        if distmeasure.get() == 'F':    
            guesslist, acc, meshlist = mainProcess(fileLocation, curval, FileboolVal)
        elif distmeasure.get() == 'ANN':
            guesslist, acc, meshlist = ANNProcess(fileLocation, curval, FileboolVal)
        elif distmeasure.get() == 'DR + ANN':
            guesslist, acc, meshlist, X_embedded, classes, paths = DRDemo(fileLocation, curval)
        else:
            print("Something weird happend")
        #print all values found in the guesslist (list off guessed meshes)
        for x in range(len(guesslist)):
            mylist.insert((x+1+(y*100)), guesslist[x])
        #print acc and sugarlines to keep reuslts seperated.
        mylist.insert((x+1+(y*100)+19), ("Accuracy: ", acc))
        mylist.insert((x+1+(y*100)+20),"=====================================")
        y+=1
        
        
#runs the Open3D file or gives error when no meshes are found (meshlist is already nicely translated in the mainfunctions)
def runO3d():
    global y
    if meshlist == []:
        mylist.insert((y*100), "error no Meshes to show RUN app first")
        mylist.insert(((y*100)+1),"=====================================")
    else:
        o3d.visualization.draw_geometries(meshlist)

#runs the TSNE plot or gives error when no TSNE plot available.
def runPlot():
    global y
    if classes is None:
        mylist.insert((y*100), "error no TSNE to plot RUN DR first")
        mylist.insert(((y*100)+1),"=====================================")
    else:
        plotTSNE(X_embedded, classes, paths)

#the UI
# root window
root = tk.Tk()
root.geometry('700x700')

# slider current value of K
current_value = tk.IntVar()

#open file , runnapp , o3dview , tsneplot buttons init:
openFile = tk.Button(root, text="Open File", padx=25,
                    pady=5, fg="white", bg="black", anchor="s", command=addFile)

runAppBut = tk.Button(root, text="Run", padx=25,
                    pady=5, fg="white", bg="black", anchor="s", command=runApp)

o3dView = tk.Button(root, text="3dView", padx=25,
                    pady=5, fg="white", bg="black", anchor="s", command=runO3d)

TsnePlot = tk.Button(root, text="TsnePlot", padx=25,
                    pady=5, fg="white", bg="black", anchor="s",command=runPlot)

#Place the buttons on locations
openFile.place(x=10,y=540)
runAppBut.place(x=10, y=580)
o3dView.place(x=10, y=620)
TsnePlot.place(x=10,y=660)

# label for the slider
slider_label = tk.Label(root, text='K nearest slider:')
slider_label.place(x=10, y=25)

#  slider
slider = tk.Scale(root, from_=1, to=20, orient='horizontal', command=slider_changed, variable=current_value)
slider.place(x=125, y=10)

# current value label
current_value_label = tk.Label(root, text=('Current Value for K:', get_current_value()))
current_value_label.place(x=25,y=55)

#result bar on right.
myscroll = tk.Scrollbar(root) 
myscroll.pack(side = tk.RIGHT, fill = tk.Y) #change
mylist = tk.Listbox(root, yscrollcommand = myscroll.set, width = 70)
mylist.pack(side = tk.RIGHT, fill = tk.BOTH) #change
myscroll.config(command = mylist.yview) 
mylist.pack(side = tk.RIGHT, fill = tk.BOTH) #change
myscroll.config(command = mylist.yview) 

#distance choice box lable
distfunc_label = tk.Label(root, text='Distfunction:')
distfunc_label.place(x=10, y=90)

#distance choice box
distmeasure = tk.StringVar(root)
distmeasure.set('F')
dist_cb = ttk.Combobox(root, textvariable=distmeasure, width=15)
choices = ['F', 'ANN', 'DR + ANN']
dist_cb['values'] = choices
dist_cb['state'] = 'readonly'
dist_cb.place(x=100, y=90)
dist_cb.bind('<<ComboboxSelected>>', distValueUpdate)

#add checkbox for file or DB
Filebool = tk.IntVar()
Filebox = tk.Checkbutton(root, text='Read Vector from File (not on DR)',variable=Filebool, onvalue=1, offvalue=0)
Filebox.place(x=10, y=150)

#mainloop of GUI
root.mainloop()