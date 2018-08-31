#!/usr/bin/python3
# -*- coding: utf-8 -*-

#v.0.0.1

"""
readNuclidLibrary(str) -> dict

Load gamma library of following format:
/"
tytle line 1
tytle line 2
0.212950	0.012000	Ac-225  
0.005500	0.062900	Ac-225 
...
/"

output dictionary format:
{nucName:[(probability,energy (kEv)),...]}
"""
#TODO 
def readNuclidLibrary(fName):
	f=open(fName,'r')
	next(f);next(f); # skip tytle
	resLib=dict()
	for line in f:
		curLine=line.strip().split('\t')
		curLine[0]=float(curLine[0])
		curLine[1]=float(curLine[1])*10**3 # convert from MeV to keV
		curLine[2]=renderNucName(curLine[2])
		curNuclide=resLib.get(curLine[2],[])
		curNuclide.append(tuple(curLine[:2]))
		resLib[curLine[2]]=curNuclide
	return(resLib)
	
"""
renderNucName(str) -> str

Possible nuclide name views:
Am-242m; Am242m; 242m-Am; 242mAm

result: Am-242m
"""
def renderNucName(nucName):#tested v.0.0.1
	mass=[];name=[];lastIsDigit=False
	for letter in nucName:
		if letter.isalpha(): 
			if lastIsDigit and letter is 'm': mass.append(letter)				
			else: name.append(letter)
			lastIsDigit=False
		if letter.isdigit(): 
			mass.append(letter)
			lastIsDigit=True

	return '-'.join([''.join(name),''.join(mass)])
