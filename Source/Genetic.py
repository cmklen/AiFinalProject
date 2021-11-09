# GUI.py
# CSE 525 - Final Project 
# Code for running a genetic algorithm on the numberlink problem
import numpy as np

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
        self.NumberofNumbers = 3
        self.grid = np.zeros((gridSize, gridSize), dtype=int)

    # read in the locations of the starting numbers 
    def PopulateGrid(self, coordinates):
        numberToPlace = 1
        for coord in coordinates:
            self.grid[coord[0]][coord[1]] = numberToPlace
            self.grid[coord[2]][coord[3]] = numberToPlace
            numberToPlace = numberToPlace + 1

    #Randomly guess next path from current location
    def __FindRandomAdjacentPath(self, x, y, population):
        guesses = [1,2,3,4]
        np.random.shuffle(guesses)

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
    def CreateInitalGeneration(self):
        newGeneration = [[],[]]
        
        for i in range(0, self.popSize):
            currentNumber = 1
            newPopulation = list(map(list, self.grid))
            partialFinishedNums = []
            finishedNums = []
            indexes = []

            #generate list of starting number locations
            for i in range(1, self.NumberofNumbers + 1):
                foundIndex = np.where(self.grid == i)
                indexes.append(list(zip(foundIndex[0], foundIndex[1])))

            #fill the grid
            while True:
                if currentNumber == 0:
                    currentNumber = 1
                if currentNumber not in partialFinishedNums:
                    x = indexes[currentNumber-1][0][0]
                    y = indexes[currentNumber-1][0][1]
                else: #grab the second number start location
                    x = indexes[currentNumber-1][1][0]
                    y = indexes[currentNumber-1][1][1]

                x, y = self.__FindRandomAdjacentPath(x, y, newPopulation)
                
                #no new path can be made
                if x == -1 and y == -1:
                    if currentNumber not in partialFinishedNums:
                        partialFinishedNums.append(currentNumber)
                        currentNumber = (currentNumber+1)%(self.NumberofNumbers+1)
                    elif currentNumber in partialFinishedNums:
                        if currentNumber not in finishedNums:
                            finishedNums.append(currentNumber)
                            # print("num:", currentNumber)
                            # print(newPopulation)
                        if len(finishedNums) == self.NumberofNumbers:
                            break
                    currentNumber = (currentNumber+1)%(self.NumberofNumbers+1)
                    continue

                if currentNumber not in partialFinishedNums:
                    indexes[currentNumber-1][0] = (x,y)
                elif currentNumber in partialFinishedNums:
                    indexes[currentNumber-1][1] = (x,y)

                newPopulation[x][y] = currentNumber

                currentNumber = (currentNumber+1)%(self.NumberofNumbers+1)

            newGeneration[Population].append(newPopulation)
            newGeneration[Population].append(newPopulation)
            newGeneration[Fitnesses].append(self.DetermineFitness(newPopulation))

        return newGeneration

    def __PrintGrid(self, gridToPrint):
        for i in range(0, self.gridSize):
            print(gridToPrint[i])

    #placeholder
    def DetermineFitness(self, individual):
        return 0

    #creates a new generation from the passed one using crossover and mutation
    #be careful here, this will not return a deep copy at the moment
    def Reproduce(self, currentGeneration):
        newGeneration = [[], []]
        for i in range(0, int(len(currentGeneration[Population])/2)):
            newChild1, newChild2  = self.Crossover(currentGeneration[Population])

            if (np.random.random() < self.mutRate):
                newChild1 = self.Mutate(newChild1)
            if (np.random.random() < self.mutRate):
                newChild2 = self.Mutate(newChild2)

            newGeneration[Population].append(newChild1)
            newGeneration[Fitnesses].append(self.DetermineFitness(newChild1))
            newGeneration[Population].append(newChild2)
            newGeneration[Fitnesses].append(self.DetermineFitness(newChild2))

        return newGeneration

    #placeholder
    def Crossover(self, population):
        parent1 = population[0]
        parent2 = population[1]

        child1 = parent1 
        child2 = parent2
        return (child1, child2)

    #placeholder
    def Mutate(self, individual):
        return individual

    #placeholder
    def RunAlgorithm(self):
        currentGeneration = self.CreateInitalGeneration()

        print("Final Gen:")
        for i in range(0, self.popSize):
            self.__PrintGrid(currentGeneration[Population][i])
            print("**************************************")

        #be careful here, this will not return a deep copy at the moment
        # for i in range(0, self.cutoff):
        #     currentGeneration = self.Reproduce(currentGeneration)

        print("Finished Running!")
        return currentGeneration

