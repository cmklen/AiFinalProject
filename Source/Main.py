# GUI.py
# CSE 525 - Final Project 
# Glue code for all numberlink files

import Genetic as gen
import GUI as gui
import numpy as np

#Get directory that the test files are in
TestPath = "TestData/"

numberlinkTests= []
testDataSizes = [7]#, 9, 11, 13, 15]
numberOfRuns = 20 #5

for i in range(0, numberOfRuns):
    numberlinkTests.append((gen.Genetic(mutRate=.015, mutType="Random", popSize=200, crossType="Crossy", cutoff=100, gridSize=7, numberOfNumbers=5), 7))
    numberlinkTests[i][0].PopulateGrid(TestPath, str(7) + "x" + str(7) + ".txt")

# wocSolutions = []
wisemen = []
for i in range(0, numberOfRuns):
    result = numberlinkTests[i][0].RunAlgorithm()
    bestOfRun = result[0]
    gui.PlotGenerations(result[1], str(i) + "_test")
    wisemen.append(bestOfRun)

finalSolution = numberlinkTests[i][0].WisdomOfCrowds(wisemen,  numberlinkTests[i][0].grid,  numberlinkTests[i][0].gridSize, 5)
gui.DisplayGame(finalSolution, numberlinkTests[i][0].grid, 5, str(i), True)

