# -*- coding: utf-8 -*-
# wymagamy biblioteki w wersji min 3.0
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk


class Saper(Gtk.Window):
    def __init__(self):

        Gtk.Window.__init__(self, title="Grid Example")

        grid = Gtk.Grid()
        self.add(grid)

        buttonlist = []

        for column in range(10):
            for row in range(10):
                a = Gtk.Label()
                button = Gtk.Button(label=column)
                a.override_background_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(0.95, 0.95, 0.95, 1.0))
                grid.attach(button, column, row + 1, 1, 1)

        grid.add(grid)

    def exit(self, widget, data=None):
        Gtk.main_quit()


win = Saper()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
