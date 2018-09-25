#!/usr/bin/python3
# -*- coding: utf-8 -*-

#v.0.0.1

from scipy.stats import norm

class calibration:

	def enToCh(self,En): return self._enCoeff[0]+self._enCoeff[1]*En
	def chToEn(self,Ch): return (Ch-self._enCoeff[0])/self._enCoeff[1]
	
	def _defGetCumulitiveArea(self,En,peakEn):
		sigma=self._cdfKoeff[0]+self._cdfKoeff[1]*En
		return (norm.cdf(En,peakEn,sigma))
		
	def __init__(self,
				 enCoeff,
				 cdfKoeff,
				 enToCh=None,
				 chToEn=None,
				 getArea=_defGetCumulitiveArea):
		self._enCoeff=enCoeff
		self._cdfKoeff=cdfKoeff
		if not(enToCh): self.enToCh=lambda En: enToCh(self,En)
		if not(chToEn): self.enToCh=lambda En: enToCh(self,En)
		self.getArea=lambda En,peakEn: getArea(self,En,peakEn)
		
class spectrometer:
	def __init__ (self,calibration,channels=2**10,minEn=0,maxEn=3000):
		self.calibration=calibration
		self.channels=channels
		self.minEn=minEn
		self.maxEn=maxEn
