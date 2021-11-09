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
    def populateGrid(self, coordinates):
        print("grid before:\n", self.grid)
        numberToPlace = 1
        for coord in coordinates:
            self.grid[coord[0]][coord[1]] = numberToPlace
            self.grid[coord[2]][coord[3]] = numberToPlace
            numberToPlace = numberToPlace + 1
        print("grid after:\n", self.grid)

    #this is not random yet
    def FindRandomAdjacentPath(self, x, y, population):
        if y + 1 < self.gridSize - 1:
            if population[x][y+1] == 0:
                return (x, y +1)
        if x + 1 < self.gridSize- 1:
            if population[x+1][y] == 0:
                return (x+1, y)
        if x - 1 >= 0:
            if population[x-1][y] == 0:
                return (x-1, y)
        if y - 1 >= 0:
            if population[x][y-1] == 0:
                return (x, y-1)
        
        return (-1, -1)

    #create random intial population
    #***Currently, this is not random, and it also only 'fills' from the first number, ignoring the presence of the second***
    #***Much more work will need to be done here, but it does make the same shitty grid at the moment***
    def CreateInitalGeneration(self):
        newPopulation = self.grid
        newGeneration = [[],[]]

        #loop through grid to find next path
        indexes = []
        for i in range(1, self.NumberofNumbers + 1):
            foundIndex = np.where(self.grid == i)
            indexes.append(list(zip(foundIndex[0], foundIndex[1])))
        
        print(indexes)
        full = False
        currentNumber = 1
        finishedNumCount = 0
        while not full:
            if currentNumber == 0:
                currentNumber = 1

            x = indexes[currentNumber-1][0][0]
            y = indexes[currentNumber-1][0][1]
            # print("x,y", x,y)
            x, y = self.FindRandomAdjacentPath(x, y, newPopulation)
            
            #no new path can be made
            if x == -1 and y == -1:
                finishedNumCount += 1
                if finishedNumCount == self.NumberofNumbers:
                    break
                else:
                    currentNumber = (currentNumber+1)%(self.NumberofNumbers+1)
                    continue
            print("before:", indexes, "x, y", x ,y, "curnum", currentNumber)
            indexes[currentNumber-1][0] = (x,y)
            print("after:",indexes)
            newPopulation[x][y] = currentNumber

            currentNumber = (currentNumber+1)%(self.NumberofNumbers+1)

        newGeneration[Population].append(newPopulation)
        newGeneration[Population].append(newPopulation)
        newGeneration[Fitnesses].append(self.DetermineFitness(newPopulation))
        # print(newGeneration[Population])
        print("new pop: \n", newGeneration[Population][0])
        return newGeneration

    #placeholder
    def DetermineFitness(self, individual):
        return 0

    #creates a new generation from the passed one using crossover and mutation
    def Reproduce(self, currentGeneration):
        newGeneration = [[], []]
        for i in range(0, int(len(currentGeneration[Population])/2)):
            newChild1, newChild2  = self.Crossover(currentGeneration[Population])

            if (np.random.random() < self.mutRate):
                child1 = self.Mutate(child1)
            if (np.random.random() < self.mutRate):
                child2 = self.Mutate(child2)

            newGeneration[Population].append(newChild1)
            newGeneration[Fitnesses].append(self.DetermineFitness(newChild1))
            newGeneration[Population].append(newChild2)
            newGeneration[Fitnesses].append(self.DetermineFitness(newChild2))

        return newGeneration

    #placeholder
    def Crossover(self, population):
        # select parents
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

        for i in range(0, self.cutoff):
            currentGeneration = self.Reproduce(currentGeneration)
        print("Finished Running!")
        return currentGeneration

