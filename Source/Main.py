# GUI.py
# CSE 525 - Final Project 
# Glue code for all numberlink files

import Genetic as gen

gridSize = 5
mutRate = 0.008
mutType = "Random"
popSize = 10
crossType = "Crossy"
cutoff = 5

coolGuy = gen.Genetic(mutRate, mutType, popSize, crossType, cutoff, gridSize)

# we want to probably pass a file here and have the class read it into a grid data type
coolGuy.populateGrid([(1,2, 3,4), (4,4, 1,4), (0,2, 3,2)])

coolGuy.RunAlgorithm()
