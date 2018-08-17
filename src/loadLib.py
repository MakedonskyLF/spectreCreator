#!/usr/bin/python3
# -*- coding: utf-8 -*-

def readNuclidLibrary(fName):
	f=open(fName,'r')
	next(f);next(f); # skip tytle
	resLib=dict()
	for line in f:
		curLine=line.strip().split('\t')
		curLine[0]=float(curLine[0])
		curLine[1]=float(curLine[1])*10**3 # convert from MeV to keV
		curNuclide=resLib.get(curLine[2],[])
		curNuclide.append(tuple(curLine[:2]))
		resLib[curLine[2]]=curNuclide
	return(resLib)
