#!/usr/bin/python3
# -*- coding: utf-8 -*-

#v.0.0.1

from datetime import timedelta

"""
readNuclidLibrary(str,str) -> dict

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
def readNuclidLibrary(nuclides:str,gammaLines:str):
	f=open(nuclides,'r')
	next(f);next(f); # skip tytle
	resLib=dict()
	for line in f:
		curLine=line.strip().split('\t')
		curLine[0]=renderNucName(curLine[0])
		curLine[6]=curLine[6].strip().lower()
		htValue=int(float(curLine[5].replace(',','.')))
		curNuc=dict(halfTime=timedelta(seconds=htValue if (curLine[6] is 's') else 0,
									   minutes=htValue if (curLine[6] is 'm') else 0,
									   hours=htValue if (curLine[6] is 'h') else 0,
									   days=htValue if (curLine[6] is 'd') else min(htValue*365.25,timedelta.max.days)),
					childs=list(zip(curLine[7:][::2],curLine[7:][1::2])),
					gammaLines=[])
		resLib[curLine[0]]=curNuc
	f.close()
	f=open(gammaLines,'r') 
	next(f);next(f); # skip tytle
	for line in f:
		curLine=line.strip().split('\t')
		curLine[0]=float(curLine[0])
		curLine[1]=float(curLine[1])*10**3 # convert from MeV to keV
		curLine[2]=renderNucName(curLine[2])
		if (curLine[2] in resLib):
			resLib[curLine[2]]['gammaLines'].append(tuple(curLine[:2]))
	f.close()
	return(resLib)
	
"""
renderNucName(str) -> str

Possible nuclide name views:
Am-242m; Am242m; 242m-Am; 242mAm

result: Am-242m
"""
def renderNucName(nucName):#tested v.0.0.1
	mass=[];name=[];lastIsDigit=False
	for letter in nucName.strip():
		if letter.isalpha(): 
			if lastIsDigit and letter is 'm': mass.append(letter)				
			else: name.append(letter)
			lastIsDigit=False
		if letter.isdigit(): 
			mass.append(letter)
			lastIsDigit=True

	return '-'.join([''.join(name),''.join(mass)])
