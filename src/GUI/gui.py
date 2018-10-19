#!/usr/bin/python3
# coding=utf-8
import gi
#from loadLib import *
#from spectrometer import *
#from spectrGenerator import *

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

#nucLibrary = readnuclidlibrary('../../data/NUCLIDES.TXT', '../../data/PHOTONS.TXT')
#print(SpectrGenerator(nucLibrary, Spectrometer(Calibration((0, 1 / 2.92), (35, 0.022)))))

builder = Gtk.Builder()
builder.add_from_file('./spectrGUI.glade')
window = builder.get_object('mainWin')

window.connect("destroy", Gtk.main_quit)
window.show_all()
Gtk.main()