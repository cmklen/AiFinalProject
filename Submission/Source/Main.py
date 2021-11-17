# GUI.py
# CSE 525 - Final Project 
# Glue code for all numberlink files

import Genetic as gen
import GUI as gui
import WOC as woc

#Get directory that the test files are in
TestPath = "TestData/"

numberlinkTests= []
testDataSizes = [7]#, 9, 11, 13, 15]
numberOfDatasets = 1 #5

for i in range(0, numberOfDatasets):
    numberlinkTests.append((gen.Genetic(mutRate=.010, mutType="Random", popSize=200, crossType="Crossy", cutoff=500, gridSize=testDataSizes[i], numberOfNumbers=5), testDataSizes[i]))
    numberlinkTests[i][0].PopulateGrid(TestPath, str(testDataSizes[i]) + "x" + str(testDataSizes[i]) + ".txt")

# wocSolutions = []
for i in range(0, numberOfDatasets):
    wisemen = []
    resultingGeneration = numberlinkTests[i][0].RunAlgorithm()
    # bestIndexToPop = resultingGeneration[1].index(max(resultingGeneration[1]))
    # bestInd = resultingGeneration[0].pop(bestIndexToPop)
    # gui.DisplayGame(bestInd, numberlinkTests[i][0].grid, numberlinkTests[i][0].GetNumberOfNumbers(), str(i))
    # for j in range(0, 10):
    #     bestIndexToPop = resultingGeneration[1].index(max(resultingGeneration[1]))
    #     bestInd = resultingGeneration[0].pop(bestIndexToPop)
    #     wisemen.append(bestInd)
    
    # print("Solution for ", str(testDataSizes[i]) + "x" + str(testDataSizes[i]) + ".txt")
    # wocSolution = woc.WisdomOfCrowds(wisemen, numberlinkTests[i][0].grid, numberlinkTests[i][0].gridSize, numberlinkTests[i][0].GetNumberOfNumbers())
    # wocSolutions.append(wocSolution)
    # gui.DisplayGame(wocSolution, numberlinkTests[i][0].grid, numberlinkTests[i][0].GetNumberOfNumbers(), "woc")
