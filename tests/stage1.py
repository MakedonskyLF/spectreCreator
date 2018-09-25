#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys

sys.path.append("../src/")

from loadLib import *
from spectrometer import *
# from nuclides import *
from spectrGenerator import *

nucLibrary = readnuclidlibrary('../data/NUCLIDES.TXT', '../data/PHOTONS.TXT')
spectrGen = SpectrGenerator(nucLibrary, Spectrometer(Calibration((0, 1 / 2.92), (35, 0.022))))

spectrGen.addnuclide(['Cs-137', 'Co-60'], [8000, 10000])

spectr1 = spectrGen.getspectr()

f = open('test.csv', 'w')
f.write('\n'.join([str(ch).replace('.', ',') for ch in spectr1]))
f.close()
