# GUI.py
# CSE 525 - Final Project 
# Code for running a genetic algorithm on the numberlink problem
import numpy as np
import re
import random

Population = 0
Fitnesses = 1

class Genetic():
    def __init__(self, mutRate, mutType, popSize, crossType, cutoff, gridSize, numberOfNumbers):
        self.mutRate = mutRate
        self.mutType = mutType
        self.popSize = popSize
        self.crossType = crossType
        self.cutoff = cutoff
        self.gridSize = gridSize
        self.NumberofNumbers = numberOfNumbers
        self.grid = np.zeros((gridSize, gridSize), dtype=int)

    # read in the locations of the starting numbers 
    def PopulateGrid(self, testPath, fileName):

        # READ THIS IN LATER FOR OTHER DATASETS BESIDES 7x7
        self.numberMask = 32 #2^5
        staticNumbers = [(2**i | self.numberMask) for i in range(0, self.NumberofNumbers)] #create static numbers
        self.maxConnectedValues = 31 
        print("Static Numbers: ", staticNumbers)
        ##**************************************************
        fileName = testPath+fileName

        with open(fileName, "r") as f:
            data = f.readlines()
            for line in data:
                lineList = re.split(':|,|\n', line)
                print("placing ", lineList[0], "into", int(lineList[1])-1, int(lineList[2])-1)
                self.grid[int(lineList[1])-1][int(lineList[2])-1] = staticNumbers[int(lineList[0]) - 1]

        print("Grid At Start: \n", self.grid)

    #create random intial population
    def CreateInitialGeneration(self):
        newGeneration = [[],[]]

        newGeneration[Population].append(np.zeros((self.gridSize, self.gridSize), dtype=int))

        for i in range(0, self.gridSize):
            for j in range(0, self.gridSize):
                if ~((self.grid[i][j] & (1 << self.NumberofNumbers)) == self.numberMask): #check if location is a starting num
                    newGeneration[Population][0][i][j] = random.randint(1, self.maxConnectedValues)
                else:
                    newGeneration[Population][0][i][j] = self.grid[i][j]

        return newGeneration

    def PrintGrid(self, gridToPrint):
        for i in range(0, self.gridSize):
            print(gridToPrint[i])             

    #takes number and counts the number of nubmers in that square
    def __countNumbersInSquare(self, n):
        count = 0
        while (n): 
            count += n & 1
            n >>= 1
        return count

    def __calculateSquareUniqueness(self, num):
        countOfNums = self.__countNumbersInSquare(num)
        connectednessFactors = [4, 2, 0, -2, 4] #hardcoded
        return connectednessFactors[countOfNums]
        
    def __findNumbersInSquare(self, n):
        nums = []
        curNum = self.NumberofNumbers - 1 #-1 as we start from 0 here
        while (n): 
            if(n & 1):
                nums.append(curNum)
            n >>= 1
            curNum-=1
        list.sort(nums)
        return nums


    #determine the fitness of an individual 
    def DetermineFitness(self, individual):
        #determine the fitness of an individual as a single number
        num = individual[0][0]
        #fitness = SquareUniqueness + ConnectedSquares
        squareUniqueness = self.__calculateSquareUniqueness(num)
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

        print("Intial Pop First Ind: \n", currentGeneration[Population][0])
        # for i in range(0, self.cutoff):
        #     currentGeneration = self.Reproduce(currentGeneration, self.NumberofNumbers)
        #     print(f'Generation {i}, Best Fit',  max(currentGeneration[Fitnesses]), 'Worst:', min(currentGeneration[Fitnesses]) )

        print("Counting bit in 13!", self.__countNumbersInSquare(13))
        print("Finding nums in 13!", self.__findNumbersInSquare(13))
                
        print("Finished Running!")
        return currentGeneration

    #Return the number of numbers
    def GetNumberOfNumbers(self):
        return self.NumberofNumbers

