__author__ = 'rickwg'
from matplotlib import pyplot as plt
from matplotlib.legend_handler import HandlerLine2D
import numpy as np

from Tica_Amuse import TicaAmuse
from common_data_importer import CommonBinaryFileDataImporter
from time import time

mixingImporter  = CommonBinaryFileDataImporter('../testdata/mixedSignalsBinary.npy')
origImporter    = CommonBinaryFileDataImporter('../testdata/origSignalsBinary.npy')
mixingData      = mixingImporter.get_data(len(mixingImporter._file)+1)
origData        = origImporter.get_data(len(origImporter._file)+1)

start = time()

amuse = TicaAmuse(mixingData, i_addEps = 1e-16)
ic = amuse.performAmuse(i_timeLag = 1, i_thresholdICs = 1)

elapsed = time() - start
print(elapsed)

x = np.arange(0.0, np.pi, np.pi/ic.shape[0])

plt.subplot(2, 1, 1)
line1, = plt.plot(x, origData[:, 0], label = '$\sin(10x)$')
line2, = plt.plot(x, origData[:, 1], label = '$\cos(50x)$')
plt.title('Original Signals')
plt.ylim(-1.5, 1.5)
plt.legend(handler_map={line1: HandlerLine2D(numpoints=4)})

plt.subplot(2, 1, 2)
plt.plot(x, mixingData[:, 0])
plt.plot(x, mixingData[:, 1])
plt.title('Mixed Signals')
plt.ylim(-1.5, 1.5)

plt.show()


plt.subplot(2, 1, 1)
plt.plot(x, ic[:, 0])
plt.title('Separated Signals')
plt.subplot(2, 1, 2)
plt.plot(x, ic[:, 1])
plt.show()