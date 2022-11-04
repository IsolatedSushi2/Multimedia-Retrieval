from fileinput import filename
import tkinter as tk
import os
from tkinter import filedialog
from MultiView import *
from QueryProcessorDemo import *


fileLocation = "unknown"
init = True
meshlist = []
def get_current_value():
    return '{: .2f}'.format(current_value.get())


def slider_changed(event):
    current_value_label.configure(text=('Current Value for K:', get_current_value()))

def addFile():
    global fileLocation
    fileLocation = filedialog.askopenfilename(initialdir="./models_final/", title="Select File",
    filetypes=(("OFF files", "*.off"),("all files", "*, *")))
    base_path = os.getcwd()
    fileLocation = os.path.relpath(fileLocation, base_path)


def runO3dApp():
    global init
    global meshlist
    y = 1
    if fileLocation == "unknown":
        print("error no file")
        mylist.insert(1, "error no file selected")
    else:
        curval = current_value.get()
        print("running on: ", fileLocation)
        print("current K = ", curval)
        guesslist, acc, meshlist = mainProcess(fileLocation, curval)
        meshlist = meshlist
        for x in range(len(guesslist)):
            mylist.insert((x+1+(y*100)), guesslist[x])
        mylist.insert((x+1+(y*100)+19), ("Accuracy: ", acc))
        mylist.insert((x+1+(y*100)+20),"=====================================")
        y+=1
        o3d.visualization.draw_geometries(meshlist)
    


    
# root window
root = tk.Tk()
root.geometry('700x700')

# slider current value
current_value = tk.IntVar()

openFile = tk.Button(root, text="Open File", padx=25,
                    pady=5, fg="white", bg="black", anchor="s", command=addFile)

runApp = tk.Button(root, text="Run", padx=25,
                    pady=5, fg="white", bg="black", anchor="s", command=runO3dApp)
openFile.place(x=10,y=600)
runApp.place(x=10, y=650)

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

#choose box
choices = ['F', 'ANN', 'DR + ANN']
distmeasure = tk.StringVar(root)
distmeasure.set('F')

#w = tk.Combobox(root, textvariable=choices)
#w.place(x=25, y=90)

root.mainloop()