# GUI.py
# CSE 525 - Final Project 
# Glue code for all numberlink files

import Genetic as gen
import os
import GUI as gui

coolGuy = gen.Genetic(mutRate=.008, mutType="Random", popSize=150, crossType="Crossy", cutoff=200, gridSize=7)

#Get directory that the test files are in
TestPath = "TestData/"

coolGuy.PopulateGrid(TestPath, "7x7.txt")


finalGen = coolGuy.RunAlgorithm()
gui.DisplayGame(finalGen[0][0], coolGuy.grid, coolGuy.GetNumberOfNumbers())
