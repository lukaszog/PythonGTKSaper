# -*- coding: utf-8 -*-
# wymagamy biblioteki w wersji min 3.0
import gi
from random import randrange

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk


class SaperButton(Gtk.Button):
    def __init__(self):
        Gtk.Button.__init__(self)
        self.set_size_request(50, 50)


class Cell:
    def __init__(self):
        self.mine = False
        self.neighbormines = 0
        self.button = SaperButton()

    def get_button(self):
        return self.button

    def place_mine(self):
        self.mine = True

    def is_mine(self):
        return self.mine


class SaperGrid(Gtk.Grid):
    def __init__(self, rows, cols, ratio):
        self.rows = rows
        self.cols = cols
        self.cells = []
        self.ratio = ratio
        Gtk.Grid.__init__(self)
        for column in range(rows):
            for row in range(cols):
                cell = Cell()
                self.cells.append(cell)
                self.attach(cell.get_button(), column, row, 1, 1)
        self.place_mines()
        self.place_labels()

    def get_cells(self):
        return self.cells

    def get_row_col_button(self, index):

        return (index / self.cols, index % self.cols)

    def place_mines(self):
        mines = 0
        while mines < (self.rows * self.cols * self.ratio):
            row = randrange(0, self.rows)
            col = randrange(0, self.cols)

            i = self.get_index(row, col)

            if not self.cells[i].is_mine():

                print 'Stawiam mine w polu {} {}'.format(col, row)

                mines += 1
                self.cells[i].place_mine()
                button = Gtk.Button()
                label = Gtk.Label("M")
                label.set_use_underline(True)
                button.add(label)
                self.attach(button, col, row, 1, 1)


    def place_labels(self):
        pass

    def get_index(self, row, col):
        return (row * self.cols) + col


class Saper:
    def __init__(self, rows, cols):
        self.window = Gtk.Window()
        self.rows = rows
        self.cols = cols
        self.vbox = Gtk.VBox()
        self.window.add(self.vbox)
        self.create_grid(rows, cols)
        self.grid = SaperGrid(rows, cols, 0.10)

    def create_grid(self, rows, cols):
        self.grid = SaperGrid(rows, cols, 0.10)

        for i, cell in enumerate(self.grid.get_cells()):
            print 'cell'
            print i
            cell.get_button().connect('button-press-event', self.clicked_handler, i, i)

        self.vbox.pack_start(self.grid, expand=True, fill=True, padding=0)

    def clicked_handler(self, widget, event, index, col):

        (row, col) = self.grid.get_row_col_button(index)
        print row
        print col
        cell = self.grid.get_cells()[index]

    @staticmethod
    def exit(self, widget, data=None):
        Gtk.main_quit()


win = Saper(5, 5)
win.window.show_all()
Gtk.main()


