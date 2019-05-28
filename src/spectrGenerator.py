#!/usr/bin/python3
# -*- coding: utf-8 -*-
# v.0.0.1

spectr_struct = {'counts': None,
                 'time': {'begin': 0, 'real': 0, 'live': 0},
                 'calibration': {'energy': [0, 1], 'FWHM': [0, 1]}}


class SpectrGenerator:
    def __init__(self, nucdictionary, spectrometer):
        self._lines = dict()
        self._dictionary = nucdictionary
        self._spectrometer = spectrometer
        self.cur_spectr = dict(spectr_struct)
        self.cur_spectr['calibration']['energy'] = spectrometer.calibration._enCoeff
        self.cur_spectr['calibration']['FWHM'] = spectrometer.calibration._cdfCoeff

    """
     Adding nuclide for generation.
    
     nuclide - name or list of names to add
    
     Output - dictionary:{energy:{activity:...,source:[NucName1,...]}}
    """

    def addnuclide(self, nuclide, activity, source=None):
        if not source: source = nuclide
        if isinstance(nuclide, (list, tuple)):
            for nuc in zip(nuclide, activity, source): self.addnuclide(*nuc)
            return
        if not (isinstance(source, list)): source = [source]
        nuclide = self._dictionary[nuclide]
        for child in nuclide['childs']:
            self.addnuclide(child[0],
                            child[1] * activity,
                            source.copy().append(child[0]))
        for enLine in nuclide['gammaLines']:
            self._lines[enLine[1]] = dict(activity=activity * enLine[0],
                                          source=source)  # for same energy will be used only last instance

    def addline(self, energy, activity):
        self._lines[energy] = dict(activity=activity, source=None)

    def _generator(self, spectrometer=None):
        if not spectrometer: spectrometer = self._spectrometer
        num_lines = len(self._lines)
        self.cur_spectr['counts'] = [0] * spectrometer.channels
        activities = [line['activity'] for line in self._lines.values()]
        last_values = list(map(spectrometer.calibration.getarea, [0] * num_lines, self._lines.keys()))
        for i in range(1, spectrometer.channels):
            cur_values = list(map(spectrometer.calibration.getarea,
                                  [spectrometer.calibration.geten(i)] * num_lines,
                                  self._lines.keys()))
            self.cur_spectr['counts'][i - 1] = sum([(a - b) * c for a, b, c in zip(cur_values,
                                                                                   last_values,
                                                                                   activities)])
            last_values = cur_values
            yield i

    def getspectr(self, spectrometer=None):
        spr_generator = self._generator(spectrometer)
        for _ in spr_generator: pass
        return self.cur_spectr
