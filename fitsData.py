# Import data and calibrate using flat field and bias frames!!

import numpy as np
from astropy.io import fits
import matplotlib.pyplot as plt
from astropy.visualization import astropy_mpl_style
from astropy.visualization import SimpleNorm
plt.style.use(astropy_mpl_style)

class fitsData():
    def __init__(self, file):
        self.hdul = fits.open(file)
        self.image = self.hdul[0].data

    def getImage(self):
        return fits.getdata(self.hdul, ext=0)

    def getinfo(self):
        return self.hdul.info()
    
    def plotImage(self, file):
        # Using the simple norm style to create plots visible
        fig, ax = plt.subplots()

        norm = SimpleNorm("sqrt", percent=95, clip=True)
        axim = norm.imshow(self.image, ax=ax)
        fig.colorbar(axim)
        fig.savefig(file)