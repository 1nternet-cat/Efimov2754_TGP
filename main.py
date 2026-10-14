from fitsData import fitsData, asteroid
import numpy as np
import os
import imageio.v2 as iio
import matplotlib.pyplot as plt
import csv

class asteroid_list():
    def __init__(self, file_arr, name_structure="Plots/temp"):
        self.asteroids = np.array([asteroid(file) for file in file_arr])
        self.name_structure = name_structure

    def plotAll(self):
        """Method to plot all the fits files to unique files names, 
        the fitsasteroid objects will save the plots as attributes"""
        for asteroid in self.asteroids:
            asteroid.plotImage()

    def loopAsteroid(self, func):
        for i, asteroid in enumerate(self.asteroids):
            pltname = f"{self.name_structure}{i}.png"
            func(asteroid, pltname)

    def plotAndSave(self):
        def plotFunc(asteroid, pltname):
            asteroid.plotImage()
            asteroid.savePlot(pltname)

        self.loopAsteroid(plotFunc)
        
    def plotAndSaveDetections(self):
        def plotFunc(asteroid, pltname):
            asteroid.plotAsteroid(pltname)

        self.loopAsteroid(plotFunc)
            
    def makeGif(self, filename):
        frames = [iio.imread(f"{self.name_structure}{i}.png") for i in range(len(self.asteroids))]
        iio.mimsave(filename, frames)

    def findAsteroidFrames(self):
        with open("Source_Detection.csv", "w") as file:
            csvwriter = csv.writer(file)
            for asteroid in self.asteroids:
                asteroid.findAsteroid()
                csvwriter.writerow(asteroid.source)

    def cropFrames(self):
        for asteroid in self.asteroids:
            asteroid.crop()


def main():
    files = os.listdir("Fits_Files")
    paths = np.array([f"Fits_Files/{file}" for file in files])

    asteroids = asteroid_list(paths, name_structure="DetectionPlots/plot")
    asteroids.cropFrames()
    asteroids.findAsteroidFrames()
    asteroids.plotAndSaveDetections()
    asteroids.makeGif("detectionGif.gif")

    


main()