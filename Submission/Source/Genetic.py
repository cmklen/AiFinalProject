# GUI.py
# CSE 525 - Final Project 
# Code for running a genetic algorithm on the numberlink problem
import numpy as np
import re
import random

Population = 0
Fitnesses = 1

class Genetic():
    def __init__(self, mutRate, mutType, popSize, crossType, cutoff, gridSize):
        self.mutRate = mutRate
        self.mutType = mutType
        self.popSize = popSize
        self.crossType = crossType
        self.cutoff = cutoff
        self.gridSize = gridSize
        self.grid = np.zeros((gridSize, gridSize), dtype=int)

    # read in the locations of the starting numbers 
    def PopulateGrid(self, testPath, fileName):
        fileName = testPath+fileName
        numberToPlace = 1
        count = 1
        with open(fileName, "r") as f:
            data = f.readlines()
            for line in data:
                lineList = re.split(':|,|\n', line)
                self.grid[int(lineList[1])-1][int(lineList[2])-1] = numberToPlace
                if (count % 2) == 0:
                    numberToPlace += 1
                count += 1

        self.NumberofNumbers = numberToPlace - 1
        print("Grid At Start: \n", self.grid)

    #create random intial population
    def CreateInitialGeneration(self):
        newGeneration = [[],[]]

        return newGeneration

    def PrintGrid(self, gridToPrint):
        for i in range(0, self.gridSize):
            print(gridToPrint[i])             

    #determine the fitness of an individual 
    def DetermineFitness(self, individual):

        return 0

    #creates a new generation from the passed one using crossover and mutation
    #Create 2 children for every two children selected
    def Reproduce(self, currentGeneration, numberOfNumbers):
        newGeneration = [[] for i in range(2)]

        for i in range(0, int(len(currentGeneration[Population])/2)):
            selectedIndivs = random.choices(currentGeneration[Population], currentGeneration[Fitnesses], k = 2)

            newChild1, newChild2  = self.Crossover(selectedIndivs, numberOfNumbers)

            if (np.random.random() < self.mutRate):
                newChild1 = self.Mutate(newChild1, numberOfNumbers)
            if (np.random.random() < self.mutRate):
                newChild2 = self.Mutate(newChild2, numberOfNumbers)

            newGeneration[Population].append(newChild1)
            newGeneration[Fitnesses].append(self.DetermineFitness(newChild1))
            newGeneration[Population].append(newChild2)
            newGeneration[Fitnesses].append(self.DetermineFitness(newChild2))

        return newGeneration

    #Create 2 new children from the 2 selected parents
    def Crossover(self, selectedIndivs, numberOfNumbers):

        return (1, 2)

    #Use a greedy algorithm to try and get a valid path
    def Mutate(self, individual, numberOfNumbers):

        return individual

    #Run the algorithm
    def RunAlgorithm(self):
        currentGeneration = self.CreateInitialGeneration()

        # print("Intial Pop: ", currentGeneration[Population][0])
        # for i in range(0, self.cutoff):
        #     currentGeneration = self.Reproduce(currentGeneration, self.NumberofNumbers)
        #     print(f'Generation {i}, Best Fit',  max(currentGeneration[Fitnesses]), 'Worst:', min(currentGeneration[Fitnesses]) )
                
        print("Finished Running!")
        return currentGeneration

    #Return the number of numbers
    def GetNumberOfNumbers(self):
        return self.NumberofNumbers

