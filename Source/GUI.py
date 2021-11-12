# GUI.py
# CSE 525 - Final Project 
# Provides a visual representaion of solutions to the numbelink problem
import matplotlib.pyplot as plt
from matplotlib import colors
import matplotlib.patheffects as PathEffects

def DisplayGame(Array,StartArray, numbersNeeded):
    gridSize = len(Array[0])
    Name = str(gridSize) + "x" + str(gridSize)
    FileName = Name + "Graph.png"

    fig = plt.figure(figsize=(8, 4))

    ax = fig.add_subplot(111)
    ax.set_title(Name)
    #Determine which color scheme to use and how many colors to select
    cmap = plt.cm.get_cmap("plasma", (numbersNeeded))
    #Set color to white under the threshold (anything under 1)
    cmap.set_under('w')
    plt.imshow(Array, cmap=cmap, vmin=.9)
    ax.set_aspect('equal')

    ax = plt.gca()
    ax.axes.xaxis.set_ticklabels([])
    ax.axes.yaxis.set_ticklabels([])
    ax.axes.xaxis.set_ticks([])
    ax.axes.yaxis.set_ticks([])
    plt.colorbar(orientation='vertical')

    for i in range(gridSize):
        for j in range(gridSize):
            if StartArray[j,i] == 0: continue
            text = ax.text(i,j,StartArray[j,i],ha="center",va="center",color="w",size="12")
            text.set_path_effects([PathEffects.withStroke(linewidth=2, foreground='black')])
    plt.savefig(FileName)
    plt.show()
