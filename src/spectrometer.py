#!/usr/bin/python3
# -*- coding: utf-8 -*-
# v.0.0.1

from scipy.stats import norm


class Calibration:

    def getch(self, en):
        return self._enCoeff[0] + self._enCoeff[1] * en

    def geten(self, eh):
        return (eh - self._enCoeff[0]) / self._enCoeff[1]

    def getarea(self, en, peaken):
        sigma = self._cdfKoeff[0] + self._cdfKoeff[1] * en
        return norm.cdf(en, peaken, sigma)

    def __init__(self,
                 encoeff,
                 cdfcoeff,
                 entoch=None,
                 chtoen=None,
                 getarea=None):
        self._enCoeff = encoeff
        self._cdfKoeff = cdfcoeff
        if entoch: self.getch = lambda en: entoch(self, en)
        if chtoen: self.geten = lambda ch: entoch(self, ch)
        if getarea: self.getarea = lambda en, peaken: getarea(self, en, peaken)


class Spectrometer:
    def __init__(self, calibration, channels=2 ** 10, minen=0, maxen=3000):
        self.calibration = calibration
        self.channels = channels
        self.minEn = minen
        self.maxEn = maxen
