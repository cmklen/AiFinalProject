# GUI.py
# CSE 525 - Final Project 
# Code for running a genetic algorithm on the numberlink problem
import numpy as np
import re
import math
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
        # print("Static Numbers: ", staticNumbers)
        ##**************************************************
        fileName = testPath+fileName

        with open(fileName, "r") as f:
            data = f.readlines()
            for line in data:
                lineList = re.split(':|,|\n', line)
                # print("placing ", lineList[0], "into", int(lineList[1])-1, int(lineList[2])-1)
                self.grid[int(lineList[1])-1][int(lineList[2])-1] = staticNumbers[int(lineList[0]) - 1]

        # print("Grid At Start: \n", self.grid)

    #create random intial population
    def CreateInitialGeneration(self):
        newGeneration = [[],[]]

        for n in range(0, self.popSize):
            newGeneration[Population].append(np.zeros((self.gridSize, self.gridSize), dtype=int))

            for i in range(0, self.gridSize):
                for j in range(0, self.gridSize):
                    if ~((self.grid[i][j] & (1 << self.NumberofNumbers)) == self.numberMask): #check if location is a starting num
                        newGeneration[Population][n][i][j] = random.randint(1, self.maxConnectedValues)
                    else:
                        newGeneration[Population][n][i][j] = self.grid[i][j]

            newGeneration[Fitnesses].append(self.DetermineFitness(newGeneration[Population][n]))

        return newGeneration           

    #takes number and counts the number of nubmers in that square
    def __countNumbersInSquare(self, n):
        count = 0
        
        #protec
        if n == 63:
            return 1

        while (n): 
            count += n & 1
            n >>= 1

        
        return count

    def __calculateSquareUniqueness(self, num):
        countOfNums = self.__countNumbersInSquare(num)
        #weight assosciated with number of numbers
        connectednessFactors = [10, 2, 0, -4, -25] #hardcoded
        return connectednessFactors[countOfNums - 1]

    #3need to fix, this isn't working for numbers < some amonut (2^4 ???)
    def __findNumberIndexesInSquare(self, n):
        nums = []
        for i in range(0, self.NumberofNumbers):
            if (1 << i) &  n:
                nums.append(i)
        list.sort(nums)
        return nums

    #checks if a static number matchs the given other number
    def __checkIfStaticNumberMatch(self, numStatic, num):   
        return (numStatic & ((1 << num) | (1 << self.NumberofNumbers) == numStatic))

    #scores the numbers of adjacent sqaures with the same number as a given sqaure (for each number in it)
    def __scoreConnectedSquares(self, individual, x, y):

        listOfNums = self.__findNumberIndexesInSquare(individual[x][y])

        connectedCountWeight = [0, 4, 3, 2, 1] #a line has a square on either side
        totalScore = 0

        for num in listOfNums:
            connectedCount = 0
            #right
            if y + 1 < self.gridSize:
                if self.__checkIfStaticNumberMatch(individual[x][y+1], num):
                    totalScore += 9
                elif individual[x][y+1] & (1 << num):
                    connectedCount += 1
            #left
            if y - 1 >= 0:
                if self.__checkIfStaticNumberMatch(individual[x][y-1], num):
                    totalScore += 9
                elif individual[x][y-1] & (1 << num):
                    connectedCount += 1
            #down
            if x + 1 < self.gridSize:
                if self.__checkIfStaticNumberMatch(individual[x+1][y], num):
                    totalScore += 9
                elif individual[x+1][y] & (1 << num):
                    connectedCount += 1
            #up
            if x - 1 >= 0:
                if self.__checkIfStaticNumberMatch(individual[x-1][y], num):
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
                if self.grid[i][j] == 0: #don't use starting grid in calculation
                    squareUniqueness = self.__calculateSquareUniqueness(individual[i][j])
                    connectedSquares = self.__scoreConnectedSquares(individual, i, j)
                    totalFitness += (squareUniqueness +  connectedSquares)
        return totalFitness

    #creates a new generation from the passed one using crossover and mutation
    #Create 2 children for every two children selected
    def Reproduce(self, currentGeneration):
        newGeneration = list([[] for i in range(2)])

        for i in range(0, int(len(currentGeneration[Population])/2)):
            selectedIndivs = random.choices(currentGeneration[Population], weights=currentGeneration[Fitnesses], k = 2)

            newChild1, newChild2  = self.Crossover(selectedIndivs[0], selectedIndivs[1])

            if (np.random.random() < self.mutRate):
                newChild1 = self.Mutate(newChild1)
            if (np.random.random() < self.mutRate):
                newChild2 = self.Mutate(newChild2)

            newGeneration[Population].append(newChild1)
            newGeneration[Fitnesses].append(self.DetermineFitness(newChild1))
            newGeneration[Population].append(newChild2)
            newGeneration[Fitnesses].append(self.DetermineFitness(newChild2))
            
        return newGeneration

    #Create 2 new children from the 2 selected parents
    def Crossover(self, parent1, parent2):
        child1 = [row[:] for row in parent1]
        child2 = [row[:] for row in parent2]

        for i in range(0, self.gridSize):
            for j in range(0, self.gridSize):
                if self.__countNumbersInSquare(child1[i][j]) >= 3:
                    child1[i][j] = parent1[i][j] | parent2[i][j]
                if self.__countNumbersInSquare(child2[i][j]) >= 3:
                    child2[i][j] = parent1[i][j] | parent2[i][j]

        return (child1, child2)

    #Use a greedy algorithm to try and get a valid path
    def Mutate(self, individual):
        i = 0 
        j = 0
        aStaticNum = True
        while(aStaticNum):
            i = random.randint(0, self.gridSize - 1)
            j = random.randint(0, self.gridSize - 1)
            #make sure we don't replace a starting num
            if self.grid[i][j] == 0:
                individual[i][j] ^= (1 << math.floor(random.randint(0, self.NumberofNumbers)))
                aStaticNum = False

        return individual

    def ConvertGridToPrintableSoultion(self, grid):
        
        for i in range(0, self.gridSize):
            for j in range(0, self.gridSize):
                if grid[i][j] == 4:
                    grid[i][j] = 3
                if grid[i][j] == 8:
                    grid[i][j] = 4
                if grid[i][j] == 16:
                    grid[i][j] = 5
        for i in range(0, self.gridSize):
            for j in range(0, self.gridSize):
                if self.grid[i][j] == 33:
                    self.grid[i][j] = 1
                    grid[i][j] = 1
                if self.grid[i][j] == 34:
                    self.grid[i][j] = 2
                    grid[i][j] = 2
                if self.grid[i][j] == 36:
                    self.grid[i][j] = 3 
                    grid[i][j] = 3
                if self.grid[i][j] == 40:
                    self.grid[i][j] = 4
                    grid[i][j] = 4
                if self.grid[i][j] == 48:
                    self.grid[i][j] = 5
                    grid[i][j] = 5


    #Run the algorithm
    def RunAlgorithm(self):
        currentGeneration = self.CreateInitialGeneration()

        runBestFit = 0
        runBestInd = np.zeros((self.gridSize, self.gridSize), dtype=int)
        # 562 max for fitness
        for i in range(0, self.cutoff):
            maxForGen = max(currentGeneration[Fitnesses])
            avgForGen = sum(currentGeneration[Fitnesses])/len(currentGeneration[Fitnesses])
            if maxForGen >= runBestFit: 
                runBestFit = maxForGen
                runBestInd = currentGeneration[Population][currentGeneration[Fitnesses].index(maxForGen)]
            currentGeneration = self.Reproduce(currentGeneration)
            print("Gen ", i, "| Fitness (best/avg):", maxForGen, "/", avgForGen)

        print("best Fit from run:", runBestFit)
        print("bestInd\n", np.array(runBestInd))
        self.ConvertGridToPrintableSoultion(runBestInd)
        return runBestInd
    
        # solutionGrid = [[2,2,2,4,4,4,4],
        #                 [2,3,2,2,2,5,4],
        #                 [2,3,3,3,1,5,4],
        #                 [2,5,5,5,1,5,4],
        #                 [2,5,1,1,1,5,4],
        #                 [2,5,1,5,5,5,4],
        #                 [2,5,5,5,4,4,4]]
        # for i in range(0, 7):
        #     for j in range(0, 7):
        #         solutionGrid[i][j] = 2**(solutionGrid[i][j]-1)

        # solutionGrid[2][4] = 32 | (1 << 0)
        # solutionGrid[5][2] = 32 | (1 << 0)
        # solutionGrid[6][0] = 32 | (1 << 1)
        # solutionGrid[1][4] = 32 | (1 << 1)
        # solutionGrid[1][1] = 32 | (1 << 2)
        # solutionGrid[2][3] = 32 | (1 << 2)
        # solutionGrid[0][3] = 32 | (1 << 3)
        # solutionGrid[6][4] = 32 | (1 << 3)
        # solutionGrid[3][3] = 32 | (1 << 4)
        # solutionGrid[1][5] = 32 | (1 << 4)

        # # print(np.array(solutionGrid)) 
        # print("fit of sol:", self.DetermineFitness(solutionGrid))

        # self.ConvertGridToPrintableSoultion(solutionGrid)
        # print(np.array(solutionGrid))

        # return solutionGrid

    #Return the number of numbers
    def GetNumberOfNumbers(self):
        return self.NumberofNumbers

class WisdomOfCrowds():
    def __findNumberIndexesInSquare(self, n):
        nums = []
        for i in range(0, self.NumberofNumbers):
            if (1 << i) &  n:
                nums.append(i)
        list.sort(nums)
        return nums

    def buildAggregateSolution(self, wisemen, gridSize, numberOfNumbers):

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
                    numberIndexes = self.__findNumberIndexesInSquare(wiseman[i][j])
                    for k in range(0, len(numberIndexes)):
                        agregateSolution[i][j][numberIndexes[k]] += 1

        print(agregateSolution)