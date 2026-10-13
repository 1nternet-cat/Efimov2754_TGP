# Import data and calibrate using flat field and bias frames!!

import numpy as np
from astropy.io import fits
import matplotlib.pyplot as plt
import matplotlib.patches as patch
from astropy.visualization import astropy_mpl_style
from astropy.visualization import SimpleNorm
from photutils.aperture import CircularAperture
plt.style.use(astropy_mpl_style)

from photutils.detection import DAOStarFinder as daost

class fitsData():
    def __init__(self, file):
        self.hdul = fits.open(file)
        self.image = self.hdul[0].data

    def getImage(self):
        return fits.getdata(self.hdul, ext=0)

    def getinfo(self):
        return self.hdul.info()

    def crop(self):
        """Method will shave 10% off every edge of the image"""
        cut = round(self.image.shape[0] / 10)
        self.image = self.image[cut:len(self.image) - cut, cut:len(self.image) - cut]
    
    def plotImage(self):
        # Using the simple norm style to create plots visible
        self.fig, self.ax = plt.subplots()
        norm = SimpleNorm("sqrt", percent=95, clip=True)
        axim = norm.imshow(self.image, ax=self.ax)
        self.fig.colorbar(axim)

    def savePlot(self, file):
        self.fig.savefig(file)
        plt.close()

class asteroid(fitsData):
    def __init__(self, file):
        fitsData.__init__(self, file)

    def findAsteroid(self):
        """Look for point-like sources in the centre of the image"""
        # find centre and take the 5% region of the image around that
        c = int(self.image.shape[0] / 2)
        percent = int(self.image.shape[0] / 20)
        centre_r = self.image[c - percent: c + percent, c - percent: c + percent]

        mask = np.full(self.image.shape, True)
        mask[c - percent: c + percent, c - percent: c + percent] = False

        daofind = daost(500, fwhm=2.5)
        self.sources = daofind(self.image, mask=mask, )
        print(self.sources)

    def plotAsteroid(self, file):
        positions = np.transpose((self.sources['x_centroid'], self.sources['y_centroid']))
        apertures = CircularAperture(positions, r=10.0)
        self.plotImage()
        p1 = apertures.plot(ax = self.ax)
        self.savePlot(file)

    