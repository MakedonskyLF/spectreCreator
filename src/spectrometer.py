#!/usr/bin/python3
# -*- coding: utf-8 -*-

#v.0.0.1

from scipy.stats import norm

class calibration:

	def _defEnToChanell(self,En): return self.enCoeff[0]+self.enCoeff[1]*En
	
	def _defGetCumulitiveArea(self,En,peakEn):
		sigma=self.cdfKoeff[0]+self.cdfKoeff[1]*En
		return (norm.cdf(En,peakEn,sigma))
		
	def __init__(self,
				 enCoeff,
				 cdfKoeff,
				 enToCh=_defEnToChanell,
				 getArea=_defGetCumulitiveArea):
		self.enCoeff=enCoeff
		self.cdfKoeff=cdfKoeff
		self.enToCh=lambda En: enToCh(self,En)
		self.getArea=lambda En,peakEn: getArea(self,En,peakEn)
		
class spectrometer:
	def __init__ (self,calibration,channels=2**10,minEn=0,maxEn=3000):
		self.calibration=calibration
		self.channels=channels
		self.minEn=minEn
		self.maxEn=maxEn
