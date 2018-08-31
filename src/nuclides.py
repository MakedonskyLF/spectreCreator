#!/usr/bin/python3
# -*- coding: utf-8 -*-

class Source:

	# TODO make use of dateTime module
	def getDecayCoef(daysPass,halfTime): return 2**(-daysPass/halfTime)
	
	def __init__(self,nucName,Activity,Date):
		self.Nuclide=nuclideDict[nucName]
		self.activity=Activity
		self.date=Date
		
	def getActivity(toDate=self.date):
		return self.activity*getDecayCoef(toDate-self.date,self.Nuclide[halfTime])
		

