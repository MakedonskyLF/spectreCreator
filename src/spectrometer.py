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
