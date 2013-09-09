#!/usr/bin/env python
'''
@author Jeremy Barr
@date 5/8/2013
@brief Using SciPy to detect and count the blobs within the image 'dna.jpeg' and using MatPlotLib to display (plot) the labeled image.

'''

import scipy
from scipy import ndimage as ni
import matplotlib.pyplot as plt

# read image into numpy array
dna = scipy.misc.imread('dna.jpeg') # grey-scale iamge

# smooth the image (to remove small objects); set the threshold
dnaf = ni.gaussian_filter(dna, 16)
T = 25 # set threshold by hand to avoid installing 'mohatos' or
       # 'scipy.stsci.image' dependencies that have threshold() functions

# find connected components
labeled, nr_objects = ni.label(dnaf > T)  # 'dna[:,:,0] > T' for red-dot case
print "number of objects is %d " % nr_objects

# save and show labeled image
#scipy.misc.imsave('labeled_dna.png',labeled)
#scipy.misc.imshow(labeled) # black and white image
print 'Saving image...'
plt.imsave('labeled_dna.png',labeled)
print 'displaying image...'
plt.imshow(labeled)

plt.show()

print 'windows closed\nEND of program'
