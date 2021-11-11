# GUI.py
# CSE 525 - Final Project 
# Glue code for all numberlink files

import Genetic as gen
import os

coolGuy = gen.Genetic(mutRate=.008, mutType="Random", popSize=10, crossType="Crossy", cutoff=5, gridSize=7)

#Get directory that the test files are in
curDir = os.getcwd()
TestPath = curDir+"\\Source"+"\\TestData\\"

coolGuy.PopulateGrid(TestPath, "7x7.txt")

coolGuy.RunAlgorithm()
