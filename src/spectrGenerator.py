#!/usr/bin/python3
# -*- coding: utf-8 -*-

#v.0.0.1

class spectrGenerator:
	def __init__(self,nucDictionary,spectrometer):
		self._lines=dict()
		self._dictionary=nucDictionary
		self._spectrometer=spectrometer
		
	"""
	 Adding nuclide for generation.
	
	 nuclide - name or list of names to add
	
	 Output - dictionary:{energy:{activity:...,source:[NucName1,...]}}
	"""
	def addNuclide(self,nuclide:str,activity:float,source:str=None):
		if not(source): source=nuclide
		if isinstance(nuclide,(list,tuple)):
			for nuc in zip(nuclide,activity,source): self.addNuclide(*nuc)
			return
		if not(isinstance(source,list)): source=[source]
		nuclide=self._dictionary[nuclide]
		for child in nuclide['childs']:
			self.addNuclide(child[0],
							child[1]*activity,
							source.copy()+[child[0]])
		for enLine in nuclide['gammaLines']:
			self._lines[enLine[1]]=dict(activity=activity*enLine[0],source=source) # for same energy will be used only last instance
			
	def addLine(self,energy,activity):
		self._lines[energy]=dict(activity=activity,source=None)

	def getSpectr(self,spectrometer=None):
		if not(spectrometer): spectrometer=self._spectrometer
		curCalibration=spectrometer.calibration
		numLines=len(self._lines)
		res=[0]*spectrometer.channels
		activities=[line['activity'] for line in self._lines.values()]
		lastValues=list(map(spectrometer.calibration.getArea,[0]*numLines,self._lines.keys()))
		for i in range(1,spectrometer.channels):
			curValues=list(map(spectrometer.calibration.getArea,
							   [spectrometer.calibration.chToEn(i)]*numLines,
							   self._lines.keys()))
			res[i-1]=sum([(a-b)*c for a,b,c in zip(curValues,
												   lastValues,
												   activities)])
			lastValues=curValues
		return res
		
