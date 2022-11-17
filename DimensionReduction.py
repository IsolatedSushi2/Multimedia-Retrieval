import json
import numpy as np
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import matplotlib
from QueryProcessor import getClassFromPath
import seaborn as sns
import ANN
import colorcet as cc
from collections import defaultdict

def createTSNEObject(data, n_components=2):
    X_embedded = TSNE(n_components=n_components, method="exact", learning_rate='auto',
                  init='random', perplexity=40).fit_transform(data)

    return X_embedded


            

def plotTSNE(X_embedded, classes, paths):
    
    #Create the colors
    palette = sns.color_palette(cc.glasbey, n_colors=len(set(classes)))
    colorMapper = dict(zip(set(classes), palette))

    #Extract the data
    x = X_embedded[:, 0]
    y = X_embedded[:, 1]

    #Create the annotations as done in https://stackoverflow.com/questions/7908636/how-to-add-hovering-annotations-to-a-plot
    names = list(set(classes))
    norm = matplotlib.colors.Normalize(0, len(set(classes)))
    fig, ax = plt.subplots()

    # Use colors of color map jet and assign to each class a color.
    colors = [colorMapper[name] for name in classes]

    scatter = ax.scatter(x=x, y=y, c=colors,
                         alpha=0.6, edgecolors='none')

    # Create tooltip with its properties for annotation.
    annot = ax.annotate("", xy=(0, 0), xytext=(20, 20),
                        textcoords="offset points",
                        bbox=dict(boxstyle="round", fc="w"),
                        arrowprops=dict(arrowstyle="->"))
    annot.set_visible(False)

    ax.set_title('TSNE Dimension Reduction')
    ax.set_xlabel('Dimension 1')
    ax.set_ylabel('Dimension 2')

    # Connects function to event manager
    fig.canvas. mpl_connect("motion_notify_event", lambda event: hover(
        fig, scatter, annot, ax, event, norm, colorMapper, colors, classes, paths))
    plt.show()

    print("Done")
    

#https://stackoverflow.com/questions/7908636/how-to-add-hovering-annotations-to-a-plot
def update_annot(scatter, annot, ind, norm, cmap, colors, classes, paths):
    index = ind["ind"][0]
    path = paths[index]
    pos = scatter.get_offsets()[index]
    annot.xy = pos

    text = f"mesh: {paths[index]}, class: {classes[index]}"
    annot.set_text(text)
    annot.get_bbox_patch().set_facecolor(colors[index])
    annot.get_bbox_patch().set_alpha(0.8)


#https://stackoverflow.com/questions/7908636/how-to-add-hovering-annotations-to-a-plot
def hover(fig, scatter, annot, ax, event, norm, cmap,
          colors, classes, paths):
    """
    Implements a hover event that call the update annot function.
    Continuously checks whether the mouse is on hovered on a point.
    """
    vis = annot.get_visible()
    if event.inaxes == ax:
        cont, ind = scatter.contains(event)
        if cont:
            update_annot(scatter, annot, ind, norm,
                         cmap, colors, classes, paths)
            annot.set_visible(True)
            fig.canvas.draw_idle()
        else:
            if vis:
                annot.set_visible(False)
                fig.canvas.draw_idle()


#Create the main function
def main():
    with open("./database/normalized_features.json", "r") as read_content:
        features = json.load(read_content)

    # Get all the data
    allData = [ANN.featureToVector(features[filename]) for filename in features]
    data = np.array(allData)
    classes = [getClassFromPath(path) for path in features]
    paths = [path for path in features]

    # # Perform an ANN with the dimension reduction
    # dimensions = 10
    # X_embedded_10n = createTSNEObject(data, dimensions)
    # annIndex = ANN.createAnnoyIndex(X_embedded_10n, dimensions)
    # index = ANN.getIndexFromFileName("models_final\\Airplane\\64.off", features)
    # neighbours = ANN.queryAnnoyIndex(annIndex, X_embedded_10n[index])
    # ANN.printQueryResults(neighbours, features)



    #Plot the 2d TSNE dimension reduction
    x_embedded_2n = createTSNEObject(data, 2)
    plotTSNE(x_embedded_2n, classes, paths)



if __name__ == "__main__":
    main()