# GUI.py
# CSE 525 - Final Project 
# Implements wisdom of crowds on a collection of numberlink solutions

import numpy as np

def BuildAggregateSolution(wisemen, gridSize, numberOfNumbers):
    agregateSolution = []

    #create 3d array
    for i in range(0, gridSize):
        agregateSolution.append([])
        for j in range(0, gridSize):
            agregateSolution[i].append([])
            for k in range(0, numberOfNumbers):
                agregateSolution[i][j].append(0)

    for wiseman in wisemen:
        for i in range(0, gridSize):
            for j in range(0, gridSize):
                agregateSolution[i][j][wiseman[i][j] - 1] += 1

    return agregateSolution

def TranslateAggregateSolutionIntoFinalGraph(agregateSolution, grid, gridSize, numberOfNumbers):
    finalGrid = np.zeros((gridSize, gridSize), dtype=int)


    # print(agregateSolution)
    # print(agregateSolution[0][0]) 
    # print(max(agregateSolution[0][0])) 
    # print(agregateSolution[0][0].index(max(agregateSolution[0][0]))) 
    for i in range(0, gridSize):
        for j in range(0, gridSize):
            if grid[i][j] != 0:
                finalGrid[i][j] = grid[i][j]
            else:
                if max(agregateSolution[i][j]):
                    finalGrid[i][j] = agregateSolution[i][j].index(max(agregateSolution[i][j]))

    return finalGrid

def WisdomOfCrowds(wisemen, grid, gridSize, numberOfNumbers):
    agregateSolution = BuildAggregateSolution(wisemen, gridSize, numberOfNumbers)
    return TranslateAggregateSolutionIntoFinalGraph(agregateSolution, grid, gridSize, numberOfNumbers)


    