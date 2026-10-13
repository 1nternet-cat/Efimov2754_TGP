from fitsData import fitsData
import numpy as np
import os
import imageio.v2 as iio
import matplotlib.pyplot as plt

class joinData(fitsData):
    def __init__(self, file_arr, name_structure="Plots/temp"):
        self.data_arr = np.array([fitsData(file) for file in file_arr])
        self.name_structure = name_structure

    def plotAll(self):
        """Method to plot all the fits files to unique files names, 
        the fitsData objects will save the plots as attributes"""
        for data in self.data_arr:
            data.plotImage()

    def plotAndSave(self):
        for data, i in enumerate(self.data_arr):
            plotname = f"{self.name_structure}{i}.png"
            data.plotImage()
            data.savePlot(plotname)

    def makeGif(self, filename):
        frames = [iio.imread(f"{self.name_structure}{i}.png") for i in range(len(self.data_arr))]
        iio.mimsave(filename, frames)

def main():
    files = os.listdir("Fits_Files")
    paths = np.array([f"Fits_Files/{file}" for file in files])
    data = joinData(paths)
    data.makeGif("thegif.gif")

main()