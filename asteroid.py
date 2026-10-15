from fitsData import fitsData

import matplotlib.pyplot as plt
import numpy as np
from photutils.aperture import CircularAperture
from photutils.detection import DAOStarFinder as daost
from photutils.profiles import RadialProfile # for radial profile

from astropy.visualization import simple_norm
from astropy.visualization import astropy_mpl_style
plt.style.use(astropy_mpl_style)


class asteroid(fitsData):
    def __init__(self, file):
        fitsData.__init__(self, file)

    def findAsteroid(self):
        """Look for point-like sources in the centre of the image"""
        # find centre and take the 2.5% region of the image around that
        c = int(self.image.shape[0] / 2)
        percent = int(self.image.shape[0] / 40)

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

    def plotAsteroid(self, filename):
        """Plot source detections with youtube thumbnail graphics"""
        positions = np.transpose((self.source['x_centroid'], self.source['y_centroid']))
        fig, ax = plt.subplots()

        # i dont really understand this kinda matplotlib stuff, this is from astropy tutorial docs 
        apertures = CircularAperture(positions, r=50.0)
        norm = simple_norm(self.image, 'sqrt', percent=99)
        axim = ax.imshow(self.image, norm=norm, origin='lower')
        apertures.plot(ax=ax, color='red')
        plt.savefig(filename)
        plt.close() # close for saving memory

    def centreImage(self):
        pos_x, pos_y = int(np.round(self.source["x_centroid"][0])), int(np.round(self.source["y_centroid"][0]))
        print(pos_x, pos_y)
        self.centred_img = self.image[pos_y-100:pos_y+100, pos_x-100:pos_x+100]
        return [pos_x, pos_y], self.centred_img

    def radialPlot(self, max_r):
        # stack asteroid images w/ asteroid centred and average them?

        # use the source position as the central part when chopping every image up

        pos, c_image = self.centreImage()
        radii = np.arange(max_r)
        rp = RadialProfile(self.image, pos, radii)
        rp.plot(label="Instantanious asteroid radial profile")
        plt.show()

        return rp.radii, rp.profile, rp.profile_error