#!/usr/bin/python3
# -*- coding: utf-8 -*-

# v.0.0.1

from datetime import datetime, timedelta


class Source:

    @staticmethod
    def getdecaycoef(dayspass: timedelta, halftime: timedelta) -> float:
        return 2 ** (-dayspass / halftime)

    def __init__(self, nuclide, activity, date):
        self.Nuclide = nuclide
        self.activity = activity
        self.date = date

    def getactivity(self, todate=datetime.now()):
        return self.activity * self.getdecaycoef(todate - self.date, self.Nuclide[0])
