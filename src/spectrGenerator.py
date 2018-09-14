#!/usr/bin/python3
# -*- coding: utf-8 -*-

#v.0.0.1

class spectrGenerator:
	def __init__(self,nucDictionary):
		self._lines=dict()
		self._dictionary=nucDictionary
		
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
