#!/usr/bin/python3
# coding=utf-8
# for independent run
import sys

sys.path.append("../")

import gi
import loadLib
import spectrometer
import spectrGenerator
from GUI.spectrGraph import SpectrGraph

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import GObject

from matplotlib.figure import Figure
from matplotlib.backends.backend_gtk3cairo import (
    FigureCanvasGTK3Cairo as FigureCanvas)


nuc_lib = None


def load_dict(chooser):
    name = chooser.get_filename()
    if name:
        global nuc_lib
        nuc_lib = loadLib.readnuclidlibrary(name + '/NUCLIDES.TXT', name + '/PHOTONS.TXT')
        nuclide_list.clear()
        for cur_nuc in nuc_lib:
            nuclide_list.append([False, cur_nuc, 0])


def switch_use(_, path):
    iter = nuclide_list.get_iter(path)
    # Get value at 2nd column
    nuclide_list.set_value(iter, 0, not nuclide_list.get_value(iter, 0))
    if nuclide_list.get_value(iter, 0):
        tree.grab_focus()
        tree.set_cursor(nuclide_list.get_path(iter), tree.get_column(2), True)  # TODO make focus if nuclided used


def set_activity(_, path, new_text):
    iter = nuclide_list.get_iter(path)
    if not new_text:
        nuclide_list.set_value(iter, 2, 0)
        nuclide_list.set_value(iter, 0, False)
        return
    try:
        value = float(new_text)
    except ValueError:
        return
    if value >= 0:
        nuclide_list.set_value(iter, 2, value)
        nuclide_list.set_value(iter, 0, True)
        return


def execute(_):
    def execute_step(spectr_generator, progress_bar):
        step_generator = spectr_generator._generator()
        for i in step_generator:
            progress_bar.set_fraction(i / spectr_generator._spectrometer.channels)
            yield True

        spectr = spectr_generator.cur_spectr

        draw_spectr(spectr['counts'])
        save_spectr('test.csv', spectr)
        progress_win.hide()
        yield False

    try:
        ch_count = int(builder.get_object('ch_count').get_text())
        en_min = int(builder.get_object('en_min').get_text())
        en_max = int(builder.get_object('en_max').get_text())
        ch_a = float(builder.get_object('ch_a').get_text())
        ch_b = float(builder.get_object('ch_b').get_text())
        sigma_a = float(builder.get_object('sigma_a').get_text())
        sigma_b = float(builder.get_object('sigma_b').get_text())
    except ValueError:
        return
    spectr_gen = spectrGenerator.SpectrGenerator(nuc_lib,
                                                 spectrometer.Spectrometer(spectrometer.Calibration((ch_a, ch_b), (sigma_a, sigma_b)), ch_count, en_min, en_max))
    rootiter = nuclide_list.get_iter_first()

    while rootiter is not None:
        if nuclide_list[rootiter][0]:
            spectr_gen.addnuclide(nuclide_list[rootiter][1], nuclide_list[rootiter][2])
        rootiter = nuclide_list.iter_next(rootiter)

    progress_win.show()
    worker = execute_step(spectr_gen, p_bar)
    GObject.idle_add(next, worker)


def draw_spectr(spectr):
    figure = Figure(figsize=(8, 6))
    axis = figure.add_subplot(111)
    axis.plot(spectr)

    canvas = FigureCanvas(figure)  # a Gtk.DrawingArea
    canvas.set_size_request(800, 600)
    win = Gtk.Window()
    win.set_default_size(800, 600)
    sw = Gtk.ScrolledWindow()
    win.add(sw)
    sw.add_with_viewport(canvas)
    win.show_all()  # TODO Make good interface (name...)


def save_spectr(f_name, spectr):
    f = open(f_name, 'w')
    f.write('\n'.join([str(ch).replace('.', ',') for ch in spectr]))
    f.close()

def save_spr(_):
    w = Gtk.Window()
    w.add(SpectrGraph())
    w.show_all()

builder = Gtk.Builder()
builder.add_from_file('./spectrGUI.glade')
window = builder.get_object('mainWin')
dict_file = builder.get_object('dict_file')
nuclide_list = builder.get_object('nuclide_list')
tree = builder.get_object('tree')
progress_win = builder.get_object('progress_win')
p_bar = builder.get_object('p_bar')

dict_file.select_filename('../../data')
load_dict(dict_file)

dict_file.connect('file-set', load_dict)

builder.get_object('use_flag').connect('toggled', switch_use)
builder.get_object('activity').connect('edited', set_activity)
builder.get_object('bt_execute').connect('clicked', execute)
builder.get_object('bt_save').connect('clicked', save_spr)

window.connect("destroy", Gtk.main_quit)
window.show_all()
Gtk.main()
