from random import randrange

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class SaperButton(Gtk.Button):
    def __init__(self):
        Gtk.Button.__init__(self)
        self.set_size_request(50, 50)


class Cell:
    def __init__(self):
        self.mine = False
        self.isdiscovered = False
        self.neighbormines = 0
        self.button = SaperButton()

    def place_mine(self):
        self.mine = True
        label = Gtk.Label()
        label.set_markup("<span color='red'><b>M</b></span>")
        label.set_no_show_all(True)
        self.button.add(label)

    def is_mine(self):
        return self.mine

    def is_discovered(self):
        return self.isdiscovered

    def discover(self):
        label = self.button.get_child()
        if label is not None:
            label.show()
        self.isdiscovered = True
        self.button.set_sensitive(False)

    def set_nighbromines(self, number):

        label = Gtk.Label(number)
        label.set_no_show_all(True)

        color = None
        if number == 1:
            color = "orange"
        elif number == 2:
            color = "orangered"
        elif number == 3:
            color = "tomato"
        elif number >= 4:
            color = "brown"
        elif number == 0:
            color = "black"

        label.set_markup("<span color='" + str(color) + "'><b>" + str(number) + "</b></span>")
        self.button.add(label)
        self.neighbormines = number

    def get_nighbromines(self):
        return self.neighbormines

    def get_button(self):
        return self.button


class SaperGrid(Gtk.Grid):
    def __init__(self, rows, cols, ratio):
        self.rows = rows
        self.cols = cols
        self.cells = []
        self.ratio = ratio
        Gtk.Grid.__init__(self)

        for row in range(rows):
            for col in range(cols):
                cell = Cell()
                self.cells.append(cell)
                self.attach(cell.get_button(), row, col, 1, 1)

        self.place_mines()
        self.place_numbers()

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
                mines += 1
                print 'Stawiam w {}'.format(i)
                self.cells[i].place_mine()

    def place_numbers(self):
        for row in range(self.rows):
            for col in range(self.cols):
                i = self.get_index(row, col)
                if not self.cells[i].is_mine():
                    n = self.get_nighbromines(row, col)
                    if n > 0:
                        self.cells[i].set_nighbromines(n)
                    else:
                        self.cells[i].set_nighbromines(0)

    def get_nighbromines(self, row, col):
        count = 0

        if self.cells[self.get_index(row, col)].is_mine():
            return -1

        for row_in in range(row - 1, row + 2):
            for col_in in range(col - 1, col + 2):
                if row_in < 0 or row_in >= self.rows or col_in < 0 or col_in >= self.cols:
                    continue
                if self.cells[self.get_index(row_in, col_in)].is_mine():
                    count += 1
        return count

    def get_index(self, row, col):
        return (row * self.cols) + col

    def discover_cell(self, row, col):
        index = self.get_index(row, col)
        print 'index', index

        if row < 0 or row >= self.rows or col < 0 or col >= self.cols or self.cells[index].is_discovered() or self.cells[index].is_mine():
            return
        elif self.get_nighbromines(row, col) > 0:
            self.cells[index].discover()
        else:
            self.cells[index].discover()
            self.discover_cell(row, col - 1)
            self.discover_cell(row, col + 1)
            self.discover_cell(row - 1, col)
            self.discover_cell(row + 1, col)
            self.discover_cell(row + 1, col - 1)
            self.discover_cell(row + 1, col + 1)
            self.discover_cell(row - 1, col - 1)
            self.discover_cell(row - 1, col + 1)

    def discover_all_cells(self):
        for cell in self.cells:
            cell.discover()


class Saper(Gtk.Window):
    def __init__(self, rows, cols):
        super(Saper, self).__init__()
        self.window = Gtk.Window()
        self.rows = rows
        self.cols = cols
        self.vbox = Gtk.VBox()
        self.window.add(self.vbox)
        self.create_grid(rows, cols)
        self.window.connect('destroy', Gtk.main_quit)

    def create_grid(self, rows, cols):
        self.grid = SaperGrid(rows, cols, 0.10)

        for i, cell in enumerate(self.grid.get_cells()):
            (row, col) = self.grid.get_row_col_button(i)
            cell.get_button().connect('clicked', self.clicked_handler, row, col)

        button = Gtk.Button("Nowa gra")
        button.connect('clicked', lambda x: self.restart())
        self.grid.attach(button, 0, self.cols, self.rows, 1)

        self.grid.set_column_homogeneous(True)
        self.grid.set_row_homogeneous(True)
        self.vbox.pack_start(self.grid, expand=True, fill=True, padding=0)

    def restart(self):
        self.vbox.remove(self.grid)
        self.create_grid(self.rows, self.cols)
        self.window.show_all()

    def clicked_handler(self, button, row, col):
        self.grid.discover_cell(row, col)
        index = self.grid.get_index(row, col)

        if self.grid.cells[index].is_mine():
            print 'Trafilem na mine!'
            self.grid.discover_all_cells()
            self.message("Przegrales")

    def message(self, str):

        dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO,
                                   Gtk.ButtonsType.OK, str)
        dialog.format_secondary_text(
           "Wybierz Nowa gra aby zagrac jeszcze raz")
        dialog.run()
        dialog.destroy()

win = Saper(10, 10)
win.window.show_all()
Gtk.main()
