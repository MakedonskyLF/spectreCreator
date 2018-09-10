#!/usr/bin/python3
# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

class Source:

	def getDecayCoef(daysPass:timedelta,halfTime:timedelta) -> float:
		return 2**(-daysPass/halfTime)
	
	def __init__(self,nucName,Activity,Date):
		self.Nuclide=nuclideDict[nucName]
		self.activity=Activity
		self.date=Date
		
	def getActivity(toDate=datetime.now()):
		return self.activity*getDecayCoef(toDate-self.date,self.Nuclide[0])
