#!/usr/bin/python3
# coding=utf-8
import gi
from loadLib import *
from spectrometer import *
from spectrGenerator import *

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

nuc_lib = None


def load_dict(chooser):
    name = chooser.get_filename()
    if name:
        global nuc_lib
        nuc_lib = readnuclidlibrary(name + '/NUCLIDES.TXT', name + '/PHOTONS.TXT')
        nuclide_list.clear()
        for cur_nuc in nuc_lib:
            nuclide_list.append([False, cur_nuc, 0])


def switch_use(_, path):
    iter = nuclide_list.get_iter(path)
    # Get value at 2nd column
    nuclide_list.set_value(iter, 0, not nuclide_list.get_value(iter, 0))
    if nuclide_list.get_value(iter, 0):
        tree.grab_focus()
        tree.set_cursor(nuclide_list.get_path(iter), tree.get_column(2), True) #TODO make focus if nuclided used


def set_activity(_, path, new_text):
    iter = nuclide_list.get_iter(path)
    if not (new_text):
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
    try:
        ch_count = int(builder.get_object('ch_count').get_text())
        en_min = int(builder.get_object('en_min').get_text())
        en_max = int(builder.get_object('en_max').get_text())
        ch_a = float(builder.get_object('ch_a').get_text())
        ch_b = float(builder.get_object('ch_b').get_text())
        sigma_a = float(builder.get_object('sigma_a').get_text())
        sigma_b = float(builder.get_object('sigma_b').get_text())
    except ValueError:
        print('ValueError')
        return
    print('OK')
    spectrGen = SpectrGenerator(nuc_lib,
                                Spectrometer(Calibration((ch_a, ch_b), (sigma_a, sigma_b)), ch_count, en_min, en_max))
    rootiter = nuclide_list.get_iter_first()
    while rootiter is not None:
        if nuclide_list[rootiter][0]:
            spectrGen.addnuclide(nuclide_list[rootiter][1],nuclide_list[rootiter][2])
        rootiter = nuclide_list.iter_next(rootiter)
    spectr = spectrGen.getspectr()

    f = open('test.csv', 'w')
    f.write('\n'.join([str(ch).replace('.', ',') for ch in spectr]))
    f.close()


builder = Gtk.Builder()
builder.add_from_file('./spectrGUI.glade')
window = builder.get_object('mainWin')
dict_file = builder.get_object('dict_file')
nuclide_list = builder.get_object('nuclide_list')
tree = builder.get_object('tree')

dict_file.select_filename('../../data')
load_dict(dict_file)

dict_file.connect('file-set', load_dict)

builder.get_object('use_flag').connect('toggled', switch_use)
builder.get_object('activity').connect('edited', set_activity)
builder.get_object('bt_execute').connect('clicked', execute)

window.connect("destroy", Gtk.main_quit)
window.show_all()
Gtk.main()
