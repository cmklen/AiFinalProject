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
        #print() #TESTING, use this as breakpoint to check grid

    #Randomly guess next path from current location
    def __FindRandomAdjacentPath(self, x, y, population, finishX, finishY):
        guesses = [1,2,3,4]
        np.random.shuffle(guesses)

        if y + 1 == finishY and x == finishX or \
           y == finishY and x + 1 == finishX or \
           y == finishY and x - 1 == finishX or \
           y - 1 == finishY and x == finishX:
            return (-2, -2)

        while guesses:
            guess = guesses.pop()
            if guess == 1:
                if y + 1 < self.gridSize:
                    if population[x][y+1] == 0:
                        return (x, y +1)
            if guess == 2:
                if x + 1 < self.gridSize:
                    if population[x+1][y] == 0:
                        return (x+1, y)
            if guess == 3:
                if x - 1 >= 0:
                    if population[x-1][y] == 0:
                        return (x-1, y)
            if guess == 4:
                if y - 1 >= 0:
                    if population[x][y-1] == 0:
                        return (x, y-1)

        return (-1, -1)

    #create random intial population
    def CreateInitialGeneration(self):
        newGeneration = [[],[]]
        
        for i in range(0, self.popSize):
            currentNumber = 1
            newPopulation = list(map(list, self.grid))
            guesses = [k for k in range(1, self.NumberofNumbers + 1)]
            np.random.shuffle(guesses)
            indexes = []

            #generate list of starting number locations
            for j in range(1, self.NumberofNumbers + 1):
                foundIndex = np.where(self.grid == j)
                indexes.append(list(zip(foundIndex[0], foundIndex[1])))

            #fill the grid
            while guesses:
                #pick random starting number, and build path from it
                currentNumber = guesses.pop()
                startNumIndex = random.randint(0,1)
                finishNumIndex = int(not startNumIndex) #lmao don't look at this cursed shit
                curX, curY = indexes[currentNumber - 1][startNumIndex]
                finishX, finishY = indexes[currentNumber - 1][finishNumIndex]

                while True:
                    curX, curY = self.__FindRandomAdjacentPath(curX, curY, newPopulation, finishX, finishY)

                    #stuck, delete partial path
                    if curX == -1 and curY == -1:
                        for i in range(0, self.gridSize):
                            for j in range(0, self.gridSize):
                                if newPopulation[i][j] == currentNumber and not (i == finishX and j == finishY) and not (i == indexes[currentNumber - 1][startNumIndex][0] and j == indexes[currentNumber - 1][startNumIndex][1]):
                                    newPopulation[i][j] = 0
                        break
                    
                    #found finish, path is good
                    if curX == -2 and curY == -2:
                        break

                    newPopulation[curX][curY] = currentNumber

            newGeneration[Population].append(newPopulation)
            newGeneration[Fitnesses].append(self.DetermineFitness(newPopulation))

        return newGeneration

    def PrintGrid(self, gridToPrint):
        for i in range(0, self.gridSize):
            print(gridToPrint[i])

    #Find the valid paths between numbers and return a count of how many are valid
    def __CountValidPaths(self, individual):
        connectedNumbers = 0

        for i in range(1, self.NumberofNumbers + 1):
            isValid = True
            #cursed lol, returns a list of all coordinates (as tuples) of the given numer i
            curNumCoordList = list(zip(np.where(np.array(individual) == i)[0], np.where(np.array(individual) == i)[1]))
            for j in range(0, len(curNumCoordList) - 1):
                currentX, currentY = curNumCoordList[j]
                nextX, nextY = curNumCoordList[j + 1]
                #indexes are in order, if we jump more than 1 square then there must be a disconnect or doubleback
                if (currentX + 1 == nextX and currentY == nextY) or \
                   (currentY + 1 == nextY and currentX == nextX) or \
                   (currentX - 1 == nextX and currentY == nextY) or \
                   (currentY - 1 == nextY and currentX == nextX):
                    continue
                else:#number must not be connected
                    isValid = False
                    break

            if (isValid):
                connectedNumbers+=1

        return connectedNumbers             

    #determine the fitness of an individual 
    def DetermineFitness(self, individual):
        #Fitness will be maximized, the maximal value will be according to the following formula
        #fitMax = #ofNumsToConnect * weight + totalSquares
        #The formula to calculate fitness will be as follows:
        #fit = fitMax - #ofUnconnectedPairs * weight - #ofEmptySquares
        weightOfConnectedness = 10
        totalSquares = self.gridSize*self.gridSize
        fitMax = (self.NumberofNumbers * weightOfConnectedness) + totalSquares
        validPaths = self.__CountValidPaths(individual)
        invalidPaths = self.NumberofNumbers - validPaths

        return fitMax - (invalidPaths * weightOfConnectedness)

    #creates a new generation from the passed one using crossover and mutation
    #Create 2 children for every two children selected
    def Reproduce(self, currentGeneration, numberOfNumbers):
        newGeneration = [[] for i in range(2)]

        for i in range(0, int(len(currentGeneration[Population])/2)):
            selectedIndivs = random.choices(currentGeneration[Population], currentGeneration[Fitnesses], k = 2)

            newChild1, newChild2  = selectedIndivs #self.Crossover(selectedIndivs, numberOfNumbers)

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

        child1 = np.zeros((len(selectedIndivs[0]), len(selectedIndivs[0])))
        child2 = np.zeros((len(selectedIndivs[0]), len(selectedIndivs[0])))
        child1 = child1.tolist()
        child2 = child2.tolist()

        for i in range(0, len(selectedIndivs[0])):
            for j in range(0, len(selectedIndivs[0][0])):
                gene = random.choice(selectedIndivs)
                attempts = 0
                while(gene[i][j] == 0):
                    gene = random.choice(selectedIndivs)
                    attempts += 1
                    if attempts >= 5:
                        break
                child1[i][j] = gene[i][j]

        for i in range(0, len(selectedIndivs[0])):
            for j in range(0, len(selectedIndivs[0][0])):
                gene = random.choice(selectedIndivs)
                attempts = 0
                while(gene[i][j] == 0):
                    gene = random.choice(selectedIndivs)
                    attempts += 1
                    if attempts >= 5:
                        break
                child2[i][j] = gene[i][j]

        return (child1, child2)

    #Use a greedy algorithm to try and get a valid path
    def Mutate(self, individual, numberOfNumbers):
        numberPath = random.randint(1, numberOfNumbers)
        curNumCoordList = list(zip(np.where(np.array(self.grid) == numberPath)[0], np.where(np.array(self.grid) == numberPath)[1]))

        #reset path for selected number
        for i in range(0, self.gridSize):
            for j in range(0, self.gridSize):
                if individual[i][j] == numberPath:
                    individual[i][j] = 0

        individual[curNumCoordList[0][0]][curNumCoordList[0][1]] = numberPath
        individual[curNumCoordList[1][0]][curNumCoordList[1][1]] = numberPath

        #Create new random path for the number
        indexes = []

        #generate list of starting number locations
        for j in range(1, self.NumberofNumbers + 1):
            foundIndex = np.where(self.grid == j)
            indexes.append(list(zip(foundIndex[0], foundIndex[1])))
        #while guesses:
            #pick random starting number, and build path from it
            #currentNumber = guesses.pop()
        startNumIndex = random.randint(0,1)
        finishNumIndex = int(not startNumIndex)
        curX, curY = indexes[numberPath - 1][startNumIndex]
        finishX, finishY = indexes[numberPath - 1][finishNumIndex]

        while True:
            curX, curY = self.__FindRandomAdjacentPath(curX, curY, individual, finishX, finishY)

            #stuck, delete partial path
            if curX == -1 and curY == -1:
                for i in range(0, self.gridSize):
                    for j in range(0, self.gridSize):
                        if individual[i][j] == numberPath and not (i == finishX and j == finishY) and not (i == indexes[numberPath - 1][startNumIndex][0] and j == indexes[numberPath - 1][startNumIndex][1]):
                            individual[i][j] = 0
                break
            
            #found finish, path is good
            if curX == -2 and curY == -2:
                break

            individual[curX][curY] = numberPath

        return individual

    #Run the algorithm
    def RunAlgorithm(self):
        currentGeneration = self.CreateInitialGeneration()

        for i in range(0, self.cutoff):
            currentGeneration = self.Reproduce(currentGeneration, self.NumberofNumbers)
            print(f'Generation {i}, Best Fit',  max(currentGeneration[Fitnesses]), 'Worst:', min(currentGeneration[Fitnesses]) )
                
        print("Finished Running!")
        return currentGeneration

    #Return the number of numbers
    def GetNumberOfNumbers(self):
        return self.NumberofNumbers

