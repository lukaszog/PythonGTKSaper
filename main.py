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

    def place_mine(self):
        self.mine = True
        label = Gtk.Label("M")
        label.set_no_show_all(True)
        self.button.add(label)

    def is_mine(self):
        return self.mine

    def discover(self):
        print 'discover'
        label = self.button.get_child()
        if label is not None:
            label.show()
        self.button.set_sensitive(False)

    def is_discovered(self):
        return not self.button.get_visible()

    def set_nighbromines(self, number):
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
                self.cells[i].place_mine()

        for i, val in enumerate(self.cells):
            print self.cells[i]

    def get_index(self, row, col):
        return (row * self.cols) + col

    def discover_cell(self, row, col):
        index = self.get_index(row, col)
        print 'index', index
        self.cells[index].discover()

    def discover_all_cells(self):
        for cell in self.cells:
            cell.discover()


class Saper:
    def __init__(self, rows, cols):
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
            print 'Button connect in col {} row {}'.format(col, row)
            cell.get_button().connect('clicked', self.clicked_handler, row, col)

        self.grid.set_column_homogeneous(True)
        self.grid.set_row_homogeneous(True)
        self.vbox.pack_start(self.grid, expand=True, fill=True, padding=0)

    def clicked_handler(self, button, row, col):
        cell_index = self.grid.get_index(row, col)
        self.grid.discover_cell(row, col)



win = Saper(5, 5)
win.window.show_all()
Gtk.main()