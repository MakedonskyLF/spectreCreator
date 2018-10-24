#!/usr/bin/python3
# -*- coding: utf-8 -*-
# v.0.0.2


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
{nuclide name:dict{halfTime:_,
                   childs:list([Nuclide,portion],...),
                   gammaLines:list((probability,energy),...)}}
"""


def readnuclidlibrary(nuclides: str, gammalines: str):
    f = open(nuclides, 'r')
    next(f); next(f)  # skip tytle
    res_lib = dict()
    for line in f:
        cur_line = line.strip().split('\t')
        cur_line[6] = cur_line[6].strip().lower()
        ht_value = int(float(cur_line[5].replace(',', '.')))
        cur_nuc = dict(halfTime=timedelta(seconds=ht_value if (cur_line[6] is 's') else 0,
                                          minutes=ht_value if (cur_line[6] is 'm') else 0,
                                          hours=ht_value if (cur_line[6] is 'h') else 0,
                                          days=ht_value if (cur_line[6] is 'd') else min(ht_value * 365.25,
                                                                                         timedelta.max.days)),
                       childs=list(zip(map(render_nucname, cur_line[7:][::2]),
                                       map(float, cur_line[7:][1::2]))),
                       gammaLines=[])
        res_lib[render_nucname(cur_line[0])] = cur_nuc
    f.close()
    f = open(gammalines, 'r')
    next(f); next(f)  # skip tytle
    for line in f:
        cur_line = line.strip().split('\t')
        cur_line[0] = float(cur_line[0])
        cur_line[1] = float(cur_line[1]) * 10 ** 3  # convert from MeV to keV
        cur_line[2] = render_nucname(cur_line[2])
        if cur_line[2] in res_lib:
            res_lib[cur_line[2]]['gammaLines'].append(tuple(cur_line[:2]))
    f.close()
    return res_lib


"""
renderNucName(str) -> str

Possible nuclide name views:
Am-242m; Am242m; 242m-Am; 242mAm

result: Am-242m
"""


def render_nucname(nucname):
    mass = []; name = []
    last_is_digit = False
    for letter in nucname.strip():
        if letter.isalpha():
            if last_is_digit and letter is 'm':
                mass.append(letter)
            else:
                name.append(letter)
            last_is_digit = False
        if letter.isdigit():
            mass.append(letter)
            last_is_digit = True

    return '-'.join([''.join(name), ''.join(mass)])
