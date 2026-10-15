# Import data and calibrate using flat field and bias frames!!

import numpy as np
from astropy.io import fits
import matplotlib.pyplot as plt
from astropy.visualization import astropy_mpl_style
from astropy.visualization import SimpleNorm
plt.style.use(astropy_mpl_style)


class fitsData():
    def __init__(self, file):
        with fits.open(file) as hdu:
            self.image = hdu[0].data
            self.header = hdu[0].header

    def crop(self):
        """Method will shave 10% off every edge of the image"""
        cut = round(self.image.shape[0] / 10)
        self.image = self.image[cut:len(self.image) - cut, cut:len(self.image) - cut]
    
    def plotImage(self, image):
        # Using the simple norm style to create plots visible
        self.fig, self.ax = plt.subplots()
        norm = SimpleNorm("sqrt", percent=95, clip=True)
        axim = norm.imshow(image, ax=self.ax)
        self.fig.colorbar(axim)

    def savePlot(self, file):
        self.fig.savefig(file)
        plt.close() # close for saving memory yuh

    def backgroundCorrect(self):
        pass

    def biasDarkCorrect(self):
        pass

