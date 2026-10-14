# Import data and calibrate using flat field and bias frames!!

import numpy as np
from astropy.io import fits
import matplotlib.pyplot as plt
from astropy.visualization import astropy_mpl_style
from astropy.visualization import SimpleNorm, simple_norm
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
        #closes figure so memory dosent fill up when dealing with multiple plots
        plt.close() 

class asteroid(fitsData):
    def __init__(self, file):
        fitsData.__init__(self, file)

    def findAsteroid(self):
        """Look for point-like sources in the centre of the image"""
        # find centre and take the 2.5% region of the image around that
        c = int(self.image.shape[0] / 2)
        percent = int(self.image.shape[0] / 40)
        centre_r = self.image[c - percent: c + percent, c - percent: c + percent]

        # mask everything but the middle
        mask = np.full(self.image.shape, True)
        mask[c - percent: c + percent, c - percent: c + percent] = False

        # using DAOStarFinder object to search
        daofind = daost(350, fwhm=2.5)
        sources = daofind(self.image, mask=mask)

        # if multiple sources are found, only record the highest count one
        if len(sources) > 1:
            pos = np.where(sources["peak"] == np.max(sources["peak"]))[0]
            print(f"Position from multiple at: {pos}")
            self.source = sources[pos]

        else:
            self.source = sources

        print(self.source)

    def plotAsteroid(self, file):
        try:
            positions = np.transpose((self.source['x_centroid'], self.source['y_centroid']))
            fig, ax = plt.subplots()
            apertures = CircularAperture(positions, r=50.0)
            norm = simple_norm(self.image, 'sqrt', percent=99)
            axim = ax.imshow(self.image, norm=norm, origin='lower')
            apertures.plot(ax=ax, color='red')
            plt.savefig(file)
            plt.close()

        except:
            print("empty frame...")

    