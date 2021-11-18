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
        self.maxConnectedValues = self.numberMask - 1 
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
        #weight assosciated with number of numbers
        connectednessFactors = [10, 2, 0, -2, -10] #hardcoded
        return connectednessFactors[countOfNums - 1]

    #3need to fix, this isn't working for numbers < some amonut (2^4 ???)
    def __findNumberIndexesInSquare(self, n):
        nums = []
        for i in range(0, self.NumberofNumbers):
            if (1 << i) &  n:
                nums.append(i)
        list.sort(nums)
        return nums

    #scores the numbers of adjacent sqaures with the same number as a given sqaure (for each number in it)
    def __scoreConnectedSquares(self, individual, x, y):

        listOfNums = self.__findNumberIndexesInSquare(individual[x][y])

        connectedCountWeight = [0, 3, 4, 2, 1] #a line has a sqaure on either side
        totalScore = 0

        for num in listOfNums:
            connectedCount = 0
            #Right
            if y + 1 < self.gridSize:
                if individual[x][y+1] & ((1 << num) | (1 << self.NumberofNumbers)  == individual[x][y+1]):
                    totalScore += 9
                elif individual[x][y+1] & (1 << num):
                    connectedCount += 1
            #left
            if y - 1 >= 0:
                if individual[x][y-1] & ((1 << num) | (1 << self.NumberofNumbers) == individual[x][y-1]):
                    totalScore += 9
                elif individual[x][y-1] & (1 << num):
                    connectedCount += 1
            #down
            if x + 1 < self.gridSize:
                if individual[x+1][y] & ((1 << num) | (1 << self.NumberofNumbers) == individual[x+1][y]):
                    totalScore += 9
                elif individual[x+1][y] & (1 << num):
                    connectedCount += 1
            #up
            if x - 1 >= 0:
                if individual[x-1][y] & ((1 << num) | (1 << self.NumberofNumbers) == individual[x-1][y]):
                    totalScore += 9
                elif individual[x-1][y] & (1 << num):
                    connectedCount += 1
            
            totalScore+=connectedCountWeight[connectedCount] 

        return totalScore

    #determine the fitness of an individual 
    def DetermineFitness(self, individual):
        totalFitness = 0
        # num = individual[0][0]
        # fitness/square = SquareUniqueness + ConnectedSquares
        # total  fit = sum of squares
        for i in range(0, self.gridSize):
            for j in range(0, self.gridSize):
                squareUniqueness = self.__calculateSquareUniqueness(individual[i][j])
                connectedSquares = self.__scoreConnectedSquares(individual, i, j)
                totalFitness += (squareUniqueness +  connectedSquares)
        return totalFitness

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

        # print("Counting bit in 13!", self.__countNumbersInSquare(13))
        # print("Finding nums in 1!", self.__findNumberIndexesInSquare(1))

        # testGrid = np.zeros((3,3), dtype=int)

        # j= 1 
        # k = 1
        # testGrid[j][k] = 1
        # testGrid[j-1][k] = 0
        # testGrid[j+1][k] = 0
        # testGrid[j][k-1] = 1
        # testGrid[j][k+1] = 1

        # # print("Connectedness score for (1,1)", self.__scoreConnectedSquares(testGrid, j, k))
        # self.gridSize = 3        
        # print("Test Grid\n", testGrid)
        solutionGrid = [[2,2,2,4,4,4,4],
                        [2,3,2,2,2,5,4],
                        [2,3,3,3,1,5,4],
                        [2,5,5,5,1,5,4],
                        [2,5,1,1,1,5,4],
                        [2,5,1,5,5,5,4],
                        [2,5,5,5,4,4,4]]
        for i in range(0, 7):
            for j in range(0, 7):
                solutionGrid[i][j] = 2**(solutionGrid[i][j]-1)

        solutionGrid[2][4] = 32 | (1 << 0)
        solutionGrid[5][2] = 32 | (1 << 0)
        solutionGrid[6][0] = 32 | (1 << 1)
        solutionGrid[1][4] = 32 | (1 << 1)
        solutionGrid[1][1] = 32 | (1 << 2)
        solutionGrid[2][3] = 32 | (1 << 2)
        solutionGrid[0][3] = 32 | (1 << 3)
        solutionGrid[6][4] = 32 | (1 << 3)
        solutionGrid[3][3] = 32 | (1 << 4)
        solutionGrid[1][5] = 32 | (1 << 4)

        print(np.array(solutionGrid)) 
        print("Fitness solution: ", self.DetermineFitness(solutionGrid))
        print("Fitness pop: ", self.DetermineFitness(currentGeneration[Population][0]))
        print("Finished Running!")
        return currentGeneration

    #Return the number of numbers
    def GetNumberOfNumbers(self):
        return self.NumberofNumbers

