# coding=utf-8
from random import randrange

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

# stala potrzebna do stawiania min
RATIO = 0.10
# ilosc pol poziomych
SIZE_X = 10
# ilosc pol pionowych
SIZE_Y = 10


"""Klasyczna gra Saper oparta na klasach i GTK 3."""


class SaperButton(Gtk.Button):
    """Klasa reprezentujaca button."""
    def __init__(self):
        Gtk.Button.__init__(self)
        # ustawienie wymiarow buttona
        self.set_size_request(50, 50)


class Cell:
    """Klasa reprezentujaca komorke na planszy
        Pola
            mine - okresla czy pod daną komórką znajduje się mina (True / False)
            isdiscovered - określa czy pole zostało odkryte
            neighbormines - określa ilczbe min w otoczeniu komórki
            button - tworzy button.
    """
    def __init__(self):
        """Przypisanie wartości początkowych."""
        self.mine = False
        self.isdiscovered = False
        self.neighbormines = 0
        self.button = SaperButton()

    def place_mine(self):
        """Funkcja ustawia minę z wykorzystaniem Labela"""
        self.mine = True
        label = Gtk.Label()
        label.set_markup("<span color='red'><b>M</b></span>")
        label.set_no_show_all(True)
        self.button.add(label)

    def is_mine(self):
        """Funkcja zwraca wartosc, ktora mówi o tym czy  pod danym polem znajduje sie mina."""
        return self.mine

    def is_discovered(self):
        """Funkcja zwraca wartosc, która mówi o tym czy dane pole było odkryte."""
        return self.isdiscovered

    def discover(self):
        """Funkcja, która odkrywa pole."""

        label = self.button.get_child()
        if label is not None:
            # odkrycie przycisku
            label.show()
        self.isdiscovered = True
        # ustawienie przycisku na nieaktywny
        self.button.set_sensitive(False)

    def set_nighbromines(self, number):
        """Funkcja zwraca liczbę, która mówi o ilości min w otoczeniu przycisku."""

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

        # ustawienie liczby na labelu
        label.set_markup("<span color='" + str(color) + "'><b>" + str(number) + "</b></span>")
        self.button.add(label)
        # zaktualizaowanie wartosci pola
        self.neighbormines = number

    def get_nighbromines(self):
        """Funkcja zwraca ilość min w otoczeniu danego pola."""
        return self.neighbormines

    def get_button(self):
        """Funkcja odwołuje się do buttona danej komórki."""
        return self.button


class SaperGrid(Gtk.Grid):
    """Klasa reprezentuje plansze gry"""
    def __init__(self, rows, cols, ratio):
        """Konstruktor przypisuje wartosci poczatkowe potrzebne do uruchomienia planszy.
           Ustawiane wartości: rows - wysokość planszy
                               cols - szerokość planszy
                               ratio - współczynnik min
                               cells = lista komórek.
        """
        self.rows = rows
        self.cols = cols
        self.cells = []
        self.ratio = ratio
        Gtk.Grid.__init__(self)
        # pętla odpowiedzialna za stworzenie komórek
        for row in range(rows):
            for col in range(cols):
                cell = Cell()
                self.cells.append(cell)
                self.attach(cell.get_button(), row, col, 1, 1)
        # ustawienie min
        self.place_mines()
        # ustawienie liczb
        self.place_numbers()

    def get_cells(self):
        """Funkcja zwraca liste komórek."""
        return self.cells

    def get_row_col_button(self, index):
        """Funkcja zwraca numer wiersza i kolumny na  podstawie wartosci index."""
        return index / self.cols, index % self.cols

    def place_mines(self):
        """Funkcja odpowiedzialna za ustawienie min na planszy."""
        mines = 0

        while mines < (self.rows * self.cols * self.ratio):

            # losowanie współrzędnych potrzebnych do postawienia miny
            row = randrange(0, self.rows)
            col = randrange(0, self.cols)

            # pobranie indeksu
            i = self.get_index(row, col)

            # jeżeli w danym miejscu nie stoi już mina to stawiamy ją
            if not self.cells[i].is_mine():
                mines += 1
                self.cells[i].place_mine()

    def place_numbers(self):
        """Funkcja odpoweidzialna za ustawienie liczb na polach, w tych miejscach gdzie nie ma min 
            Liczby świadczą o ilości min w otoczeniu pola.
        """
        for row in range(self.rows):
            for col in range(self.cols):
                i = self.get_index(row, col)
                if not self.cells[i].is_mine():
                    n = self.get_nighbromines(row, col)
                    self.cells[i].set_nighbromines(n if n > 0 else 0)

    def get_nighbromines(self, row, col):
        """Funkcja odpowiedzialna za pobranie ilości min w otoczeniu komórki"""
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
        """Funkcja zwraca index na podstawie wiersza i kolumny"""
        return (row * self.cols) + col

    def discover_cell(self, row, col):
        """Funkcja odpowiedzialna za odkrycie komórki"""

        index = self.get_index(row, col)

        if row < 0 or row >= self.rows or col < 0 or col >= self.cols or self.cells[index].is_discovered() or self.cells[index].is_mine():
            return
        elif self.get_nighbromines(row, col) > 0:
            self.cells[index].discover()
        else:
            # rekurencyjne wywolanie w przypadku trafienia na 0
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
        """Funckja odkrywa wszystkie pola"""
        for cell in self.cells:
            cell.discover()


class App(Gtk.Window):
    """Główna klasa rozruchowa, inicjuje widok aplikacji"""
    def __init__(self, rows, cols):
        super(App, self).__init__()
        self.grid = SaperGrid(rows, cols, RATIO)
        self.window = Gtk.Window()
        self.rows = rows
        self.cols = cols
        self.vbox = Gtk.VBox()
        self.window.add(self.vbox)
        self.create_grid()
        self.window.connect('destroy', Gtk.main_quit)

    def create_grid(self):
        # tworzenie poszczególnych połączeń do przycisków
        for i, cell in enumerate(self.grid.get_cells()):
            (row, col) = self.grid.get_row_col_button(i)
            cell.get_button().connect('clicked', self.clicked_handler, row, col)

        button = Gtk.Button("Nowa gra")
        button.connect('clicked', lambda x: self.restart())
        # dołączenie przycisku Nowa gra do planszy
        self.grid.attach(button, 0, self.cols, self.rows, 1)

        # ustawienie takiego samego rozmiaru dla wierszy i kolumn
        self.grid.set_column_homogeneous(True)
        self.grid.set_row_homogeneous(True)
        self.vbox.pack_start(self.grid, expand=True, fill=True, padding=0)

    def restart(self):
        """FUnkcja odpowiedzialna za restart gry"""
        self.vbox.remove(self.grid)
        self.create_grid(self.rows, self.cols)
        self.window.show_all()

    def clicked_handler(self, button, row, col):
        """Funkcja odpowiedzialna za obsługę kliknięcia"""
        self.grid.discover_cell(row, col)
        index = self.grid.get_index(row, col)

        # sprawdzenie czy uzytkownik wygral
        if self.player_win():
            self.grid.discover_all_cells()

        # sprawdzenie czy uzytkownik kliknal na mine
        if self.grid.cells[index].is_mine():
            self.grid.discover_all_cells()
            self.message("Przegrales")

    def player_win(self):
        """Sprawdzenie czy wszystkie pola zostały kliknięte"""
        for cell in self.grid.get_cells():
            if not cell.is_mine() and not cell.is_discovered():
                return False
        self.message('Gratulacje, wygrales!')
        return True

    def message(self, msg):
        """Funkcja odpowiedzialna za wyświetlenie okna dialogowego"""
        dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO,
                                   Gtk.ButtonsType.OK, msg)
        dialog.format_secondary_text(
           "Wybierz Nowa gra aby zagrac jeszcze raz")
        dialog.run()
        dialog.destroy()

if __name__ == "__main__":
    win = App(SIZE_X, SIZE_Y)
    win.window.show_all()
    Gtk.main()
