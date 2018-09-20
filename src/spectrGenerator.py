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
		print(source)
		for child in nuclide['childs']:
			self.addNuclide(child[0],
							child[1]*activity,
							source.copy()+[child[0]])
		for enLine in nuclide['gammaLines']:
			self._lines[enLine[1]]=dict(activity=activity*enLine[0],source=source)
			
	def addLine(self,energy,activity)
		self._lines[energy]=dict(activity=activity,source=None)

	def getSpectr(self,spectrometer=None)
		#generate gausian peaks: channels, limits
		if spectrometer: spectrometer=self._spectrometer
		curCalibration=spectrometer.calibration
		lastValues=map(calibration.getArea,[0]*len(self._lines),self._lines.keys())
		
		#output
		
