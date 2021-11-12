# GUI.py
# CSE 525 - Final Project 
# Provides a visual representaion of solutions to the numbelink problem
import matplotlib.pyplot as plt
from matplotlib import colors

def DisplayGame(Array, numbersNeeded):
    Name = str(len(Array[0])) + "x" + str(len(Array[0]))
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

    cax = fig.add_axes([0.12, 0.1, 0.78, 0.8])
    cax.get_xaxis().set_visible(False)
    cax.get_yaxis().set_visible(False)
    cax.patch.set_alpha(0)
    cax.set_frame_on(False)
    plt.colorbar(orientation='vertical')
    plt.savefig(FileName)
    plt.show()
