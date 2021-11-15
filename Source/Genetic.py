# GUI.py
# CSE 525 - Final Project 
# Code for running a genetic algorithm on the numberlink problem
import numpy as np
import re
import random
from itertools import product, starmap
import copy

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
            return (-1, -1)

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

                    if curX == -1 and curY == -1:
                        break

                    newPopulation[curX][curY] = currentNumber

            newGeneration[Population].append(newPopulation)
            newGeneration[Fitnesses].append(self.DetermineFitness(newPopulation))

        return newGeneration

    def __PrintGrid(self, gridToPrint):
        for i in range(0, self.gridSize):
            print(gridToPrint[i])

    #Find the valid paths between numbers and return a count of how many are valid
    def __CountValidPaths(self, individual):
        connectedNumbers = 0

        for i in range(1, self.NumberofNumbers + 1):
            isValid = True
            #cursed lol, returns a list of all coordinates 9as tuples) of the given numer i
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

    def CountStrayPath(self,array):
        strayCount = 0

        for i in range(self.gridSize):
            for j in range(self.gridSize):
                currentNum = array[i][j]
                adjacentSpace = 0

                #examine space above currentNum
                try:
                    if array[i][j-1] == currentNum: adjacentSpace +=1
                except: 
                    pass

                #examine space to the left of currentNum
                try:
                    if array[i-1][j] == currentNum: adjacentSpace +=1
                except: 
                    pass

                #examine space to the right of currentNum
                try:
                    if array[i+1][j] == currentNum: adjacentSpace +=1
                except: 
                    pass

                #examine space below currentNum
                try:
                    if array[i][j+1] == currentNum: adjacentSpace +=1
                except: 
                    pass

                if adjacentSpace == 0:
                    strayCount += 1

        return strayCount                   


    #placeholder
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
        emptySquares = totalSquares - np.count_nonzero(individual)
        straySquares = self.CountStrayPath(individual)

        return fitMax - (invalidPaths * weightOfConnectedness) - emptySquares - straySquares

    #creates a new generation from the passed one using crossover and mutation
    #be careful here, this will not return a deep copy at the moment
    #Create 2 children for every two children selected
    def Reproduce(self, currentGeneration, numberOfNumbers):
        newGeneration = [[], []]

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
        parent1 = selectedIndivs[0]
        parent2 = selectedIndivs[1]

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
        #Find spaces where the nodes to connect are
        curNumCoordList = list(zip(np.where(np.array(self.grid) == numberPath)[0], np.where(np.array(self.grid) == numberPath)[1]))

        gridCopy = copy.deepcopy(self.grid)

        for i in range(0,len(individual)):
            for j in range(0,len(individual)):
                if individual[i][j] == numberPath:
                    gridCopy[i][j] = numberPath

        gridCopy, check = self.createPath(numberPath, curNumCoordList, gridCopy)

        if check:
            #Copy path into individual
            for i in range(0,len(individual)):
                for j in range(0,len(individual)):
                    """ if individual[i][j] == numberPath:
                        individual[i][j] = 0 """
                    if gridCopy[i][j] == numberPath:
                        individual[i][j] = numberPath

        return individual


    def checkDirection(self, direction, curPosition, gridCopy, numberPath, visitedCoords):
        #if direction is right
        if direction == 0:
            if(curPosition[1] + 1 < len(gridCopy)) and (gridCopy[curPosition[0]][curPosition[1]+1] == 0 or gridCopy[curPosition[0]][curPosition[1]+1] == numberPath):
                gridCopy[curPosition[0]][curPosition[1]+1] = numberPath
                curPosition = (curPosition[0], curPosition[1]+1)
                if curPosition not in visitedCoords:
                    visitedCoords.append(curPosition)
                    return True, visitedCoords
        #if direction is up
        if direction == 1:
            if(curPosition[0] - 1 >= 0) and (gridCopy[curPosition[0]-1][curPosition[1]] == 0 or gridCopy[curPosition[0]-1][curPosition[1]] == numberPath):
                gridCopy[curPosition[0]-1][curPosition[1]] = numberPath
                curPosition = (curPosition[0]-1, curPosition[1])
                if curPosition not in visitedCoords:
                    visitedCoords.append(curPosition)
                    return True, visitedCoords
        #if direction is left
        if direction == 2:
            if(curPosition[1] - 1 >= 0) and (gridCopy[curPosition[0]][curPosition[1]-1] == 0 or gridCopy[curPosition[0]][curPosition[1]-1] == numberPath):
                gridCopy[curPosition[0]][curPosition[1]-1] = numberPath
                curPosition = (curPosition[0], curPosition[1]-1)
                if curPosition not in visitedCoords:
                    visitedCoords.append(curPosition)
                    return True, visitedCoords
        #if direction is down
        if direction == 3:
            if(curPosition[0] + 1 < len(gridCopy)) and (gridCopy[curPosition[0]+1][curPosition[1]] == 0 or gridCopy[curPosition[0]+1][curPosition[1]] == numberPath):
                gridCopy[curPosition[0]+1][curPosition[1]] = numberPath
                curPosition = (curPosition[0]+1, curPosition[1])
                if curPosition not in visitedCoords:
                    visitedCoords.append(curPosition)
                    return True, visitedCoords

        return False, visitedCoords

    def createPath(self, numberPath, curNumCordList, gridCopy):
        startPosition = curNumCordList[0]
        gridArray = np.array(gridCopy)
        indices = np.where(gridArray==numberPath)
        """ while(True):

        startPosition = (random.choice(indices[0], random)) """
        endPosition = curNumCordList[1]
        curPosition = startPosition
        attempts = 0
        check = False

        #0 = right, 1 = up, 2 = left, 4 = down
        directions = [0,1,2,3]
        visitedCoords = [startPosition]
        while(True):
            random.shuffle(directions)
            choice = random.randint(1,4)
            if attempts > 5:
                break

            #Check if the next move could move to the end state
            #Check right
            if(curPosition[1] + 1 < len(gridCopy)) and (curPosition[0] == endPosition[0] and curPosition[1]+1 == endPosition[1]):
                check = True
                break
            #Check up
            if(curPosition[0] - 1 >= 0) and (curPosition[0]-1 == endPosition[0] and curPosition[1] == endPosition[1]):
                check = True
                break
            #Check left
            if(curPosition[0] - 1 >= 0) and (curPosition[0]== endPosition[0] and curPosition[1]-1 == endPosition[1]):
                check = True
                break
            #Check down
            if(curPosition[0] + 1 < len(gridCopy)) and (curPosition[0]+1 == endPosition[0] and curPosition[1] == endPosition[1]):
                check = True
                break
            #Check current position
            if(curPosition[0] == endPosition[0]) and (curPosition[1] == endPosition[1]):
                check = True
                break
            
            loopCheck = False
            for i in directions:
                validDir, visitedCoords = self.checkDirection(i, curPosition, gridCopy, numberPath, visitedCoords)
                if validDir:
                    if i == 0:
                        gridCopy[curPosition[0]][curPosition[1]+1] = numberPath
                        curPosition = (curPosition[0], curPosition[1]+1)
                        attempts = 0
                        loopCheck = True
                        break
                    elif i == 1:
                        gridCopy[curPosition[0]-1][curPosition[1]] = numberPath
                        curPosition = (curPosition[0]-1, curPosition[1])
                        attempts = 0
                        loopCheck = True
                        break
                    elif i == 2:
                        gridCopy[curPosition[0]][curPosition[1]-1] = numberPath
                        curPosition = (curPosition[0], curPosition[1]-1)
                        attempts = 0
                        loopCheck = True
                        break
                    else:
                        gridCopy[curPosition[0]+1][curPosition[1]] = numberPath
                        curPosition = (curPosition[0]+1, curPosition[1])
                        attempts = 0
                        loopCheck = True
                        break

                if not loopCheck:
                    break
            attempts += 1
            
            #print()
        return gridCopy, check

    #placeholder
    def RunAlgorithm(self):
        currentGeneration = self.CreateInitialGeneration()

        print("Final Gen:")
        for i in range(0, self.popSize):
            self.__PrintGrid(currentGeneration[Population][i])
            print("Fitness:", currentGeneration[Fitnesses][i])
            print("**************************************")

        #be careful here, this will not return a deep copy at the moment
        for i in range(0, self.cutoff):
            currentGeneration = self.Reproduce(currentGeneration, self.NumberofNumbers)

            #Print out progress every so many generations
            if(i % 50) == 0:
                print(f'Generation {i}')

        print("Finished Running!")
        return currentGeneration

    #Return the number of numbers
    def GetNumberOfNumbers(self):
        return self.NumberofNumbers

