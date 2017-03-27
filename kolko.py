#-*- coding: utf-8 -*-
import gi
# wymagamy biblioteki w wersji min 3.0
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

import random  # losowanie ruchu komputera

class App(object):
    """ UWAGA: to tylko szablon aplikacji. Należy go poprawić i uzupełnić."""

    def __init__(self):
        self.window = Gtk.Window()
        self.window.set_title("Kółko i krzyżyk")
        self.window.set_default_size(200, 200)

        self.window.connect("delete-event", Gtk.main_quit)
        self.znak = "o"  # okresla kto bedzie wykonywac ruch
        self.plansza = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

        # ukladam przyciski na siatce
        grid = Gtk.Grid()
        self.buttons = []
        for i in range(3):
            self.buttons.append([])
            for j in range(3):
                b = Gtk.Button()
                self.buttons[i].append(b)
                grid.attach(b, i, j, 1, 1)
                b.connect("clicked", self.kliknieto, i, j)
        self.window.add(grid)
        # kolumny maja miec identyczna szerokosc, wiersze identyczna wysokosc
        grid.set_column_homogeneous(True)
        grid.set_row_homogeneous(True)
        self.window.show_all()

    def zmien_znak(self):
        """Zmiana aktualnego znaku (gracza)"""
        self.znak = "x" if self.znak == "o" else "o"

    def random_click(self):
        """Wykonuje ruch komputera (losowy)"""

        # lista pustych pol (jak to zrobic w jednej linii?)
        wolne = []
        for i in range(3):
            for j in range(3):
                if self.plansza[i][j] == 0:
                    wolne.append((i,j))
        if not wolne:
            return # komniec gry - pola zajete
        return random.choice(wolne)

    def ruch(self, x, y):
        """Wykonuje ruch gracza"""
        self.plansza[x][y] = self.znak
        self.buttons[x][y].set_label(self.znak)
        self.zmien_znak()

    def kliknieto(self, btn, x, y):
        if self.plansza[x][y] == 0:
            self.ruch(x, y)
            # ruch komputera
            i, j = self.random_click()
            self.ruch(i, j)

if __name__ == "__main__":
    a = App()
    Gtk.main()