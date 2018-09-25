#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys

sys.path.append("../src/")

from loadLib import *
from spectrometer import *
from nuclides import *
from spectrGenerator import *

nucLibrary=readNuclidLibrary('../data/NUCLIDES.TXT','../data/PHOTONS.TXT')
spectrGen=spectrGenerator(nucLibrary,spectrometer(calibration((0,1/2.92),(35,0.022))))

spectrGen.addNuclide(['Cs-137','Co-60'],[8000,10000])

spectr1 = spectrGen.getSpectr()

f = open('test.csv', 'w')
f.write('\n'.join([str(ch).replace('.', ',') for ch in spectr1]))
f.close()

print('testLine')
