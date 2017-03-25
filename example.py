#!/usr/bin/python2

#------------------------------------------------------------------------------
#    Filename: minesweeper.py
#
#      Author: David C. Drake (http://davidcdrake.com)
#
# Description: A Minesweeper game developed using Python 2.7 and PyGtk 2.24.
#------------------------------------------------------------------------------

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
import random

SMALL = 0
MEDIUM = 1
LARGE = 2
DEFAULT_SIZE = SMALL
SIZE_DESCRIPTIONS = ["Small (10 x 10)",
                     "Medium (15 x 15)",
                     "Large (20 x 20)"]
ROW_COL_VALUES = [(10, 10),
                  (15, 15),
                  (20, 20)]
CELL_SIZE = 20 # pixels
MINE_RATIO = 0.10 # About 10% of the cells will contain mines.
FLAG_IMAGE = 'images/flag.jpg'
MINE_IMAGE = 'images/mine.jpg'


class Minesweeper():

    def __init__(self, size):
        self.size = size
        (self.rows, self.cols) = ROW_COL_VALUES[self.size]
        self.createWindow(self.cols * CELL_SIZE, self.rows * CELL_SIZE)
        self.createMenu()
        self.createTable(self.rows, self.cols)
        self.window.show_all()


    def createWindow(self, width, height):
        self.window = Gtk.Window()
        self.window.set_default_size(width, height)
        self.window.set_resizable(False)
        self.window.set_title('Minesweeper')
        self.window.connect('destroy', self.destroyHandler)
        self.window.connect('delete_event', self.deleteHandler)
        self.vbox = Gtk.VBox()
        self.window.add(self.vbox)


    def createMenu(self):
        self.menu = Gtk.Menu()
        self.addMenuItem('New Game', self.restartHandler)
        self.addMenuItem('Resize', self.resizeHandler)
        self.addMenuItem('Solve', self.solveHandler)
        self.addMenuItem('Quit', self.destroyHandler)
        self.root_menu = Gtk.MenuItem('Game')
        self.root_menu.set_submenu(self.menu)
        self.menubar = Gtk.MenuBar()
        self.menubar.add(self.root_menu)
        self.vbox.add(self.menubar)


    def addMenuItem(self, title, handler):
        item = Gtk.MenuItem(title)
        item.connect('activate', handler)
        self.menu.add(item)



    def createTable(self, rows, cols):
        self.table = MinesweeperTable(rows, cols)
        for cell in self.table.getCells():
            cell.get_button().connect('button_release_event',
                                      self.clickedHandler)
        self.vbox.pack_start(self.table)


    def run(self):
        Gtk.main()


    def deleteHandler(self, widget, event, data=None):
        return False


    def destroyHandler(self, widget, data=None):
        Gtk.main_quit()


    def resizeHandler(self, widget, data=None):
        label = Gtk.Label('Choose a new size:')
        dialog = Gtk.Dialog('Resize',
                            None,
                            Gtk.DIALOG_MODAL | Gtk.DIALOG_DESTROY_WITH_PARENT,
                            (SIZE_DESCRIPTIONS[SMALL], SMALL,
                             SIZE_DESCRIPTIONS[MEDIUM], MEDIUM,
                             SIZE_DESCRIPTIONS[LARGE], LARGE,
                             Gtk.STOCK_CANCEL, Gtk.RESPONSE_REJECT))
        dialog.vbox.pack_start(label)
        label.show()
        response = dialog.run()
        dialog.destroy()
        if (response == SMALL or response == MEDIUM or response == LARGE) and \
           response != self.size:
            self.size = response
            (self.rows, self.cols) = ROW_COL_VALUES[self.size]
            self.restart()

    def restartHandler(self, widget, data=None):
        self.restart()


    def restart(self):
        self.vbox.remove(self.table)
        self.createTable(self.rows, self.cols)
        self.window.show_all()


    def solveHandler(self, widget, data=None):
        self.table.revealAllCells()

    def clickedHandler(self, widget, data=None):
        if data.button == 1: # Left-click
            (row, col) = self.table.getRowColOfButton(widget)
            cell = self.table.getCells()[self.table.getIndex(row, col)]
            if self.playerHasLost(cell):
                self.restart()
                return
            else:
                self.table.revealCell(row, col)
        elif data.button == 3: # Right-click
            widget.toggleFlag()
        if self.playerHasWon():
            self.restart()


    def playerHasLost(self, cell):
        if cell.containsMine():
            self.table.revealAllCells()
            self.displayMessage('Sorry, you landed on a mine. Try again!',
                                'Game over!')
            return True
        return False


    def playerHasWon(self):
        for cell in self.table.getCells():
            if not cell.containsMine() and not cell.isRevealed():
                return False
        self.displayMessage('Congratulations, you won!',
                            'Victory!')
        return True

    def displayMessage(self, message, title=""):
        label = Gtk.Label(' ' + message + ' ')
        dialog = Gtk.Dialog(title,
                            None,
                            Gtk.DIALOG_MODAL | Gtk.DIALOG_DESTROY_WITH_PARENT,
                            (Gtk.STOCK_OK, Gtk.RESPONSE_ACCEPT))
        dialog.vbox.pack_start(label)
        label.show()
        dialog.run()
        dialog.destroy()

class MinesweeperTable(Gtk.Table):

    def __init__(self,
                 rows,
                 cols,
                 mineRatio=MINE_RATIO,
                 homogeneous=True):
        Gtk.Table.__init__(self, rows, cols, homogeneous)
        self.rows = rows
        self.cols = cols
        self.mineRatio = mineRatio
        self.cells = []
        for row in range(rows):
            for col in range(cols):
                cell = MinesweeperCell()
                self.cells.append(cell)
                self.attach(cell.getButton(), col, col + 1, row, row + 1)
        self.placeMines()
        self.placeLabels()


    def placeMines(self):
        mines = 0
        while mines < (self.rows * self.cols * self.mineRatio):
            row = random.randrange(0, self.rows)
            col = random.randrange(0, self.cols)
            i = self.getIndex(row, col)
            if not self.cells[i].containsMine():
                mines += 1
                self.cells[i].placeMine()
                self.attach(MinesweeperImage(MINE_IMAGE),
                            col,
                            col + 1,
                            row,
                            row + 1)

    def placeLabels(self):
        for row in range(self.rows):
            for col in range(self.cols):
                i = self.getIndex(row, col)
                if not self.cells[i].containsMine():
                    n = self.getAdjacentMineCount(row, col)
                    if n > 0:
                        self.cells[i].setAdjacentMines(n)
                        self.attach(Gtk.Label(str(n)),
                                    col,
                                    col + 1,
                                    row,
                                    row + 1)

    def getCells(self):
        return self.cells


    def getAdjacentMineCount(self, row, col):
        count = 0
        if self.cells[self.getIndex(row, col)].containsMine():
            return -1
        for r in range(row - 1, row + 2):
            for c in range(col - 1, col + 2):
                if r < 0 or r >= self.rows or c < 0 or c >= self.cols:
                    continue
                if self.cells[self.getIndex(r, c)].containsMine():
                    count += 1
        return count


    def revealCell(self, row, col):
        i = self.getIndex(row, col)
        if row < 0 or row >= self.rows or col < 0 or col >= self.cols or \
           self.cells[i].isRevealed() or self.cells[i].containsMine():
            return
        elif self.cells[i].getAdjacentMines() > 0:
            self.cells[i].reveal()
        else:
            self.cells[i].reveal()
            self.revealCell(row, col - 1)
            self.revealCell(row, col + 1)
            self.revealCell(row - 1, col)
            self.revealCell(row + 1, col)
            self.revealCell(row + 1, col - 1)
            self.revealCell(row + 1, col + 1)
            self.revealCell(row - 1, col - 1)
            self.revealCell(row - 1, col + 1)

    def revealAllCells(self):
        for cell in self.cells:
            cell.reveal()


    def getIndex(self, row, col):
        return (row * self.cols) + col


    def getRowCol(self, index):
        return (index / self.cols, index % self.cols)


    def getRowColOfButton(self, button):
        for i in range(self.rows * self.cols):
            if self.cells[i].get_button() == button:
                return self.getRowCol(i)
        return (-1, -1) # Button was not found.

class MinesweeperCell:

    def __init__(self):
        self.mine = False
        self.adjacentMines = 0
        self.button = MinesweeperButton()


    def placeMine(self):
        self.mine = True


    def containsMine(self):
        return self.mine


    def setAdjacentMines(self, num):
        self.adjacentMines = num


    def getAdjacentMines(self):
        return self.adjacentMines


    def reveal(self):
        self.button.hide()


    def isRevealed(self):
        return (not self.button.get_visible())


    def getButton(self):
        return self.button


class MinesweeperButton(Gtk.Button):

    def __init__(self):
        Gtk.Button.__init__(self)
        self.set_size_request(CELL_SIZE, CELL_SIZE)


    def toggleFlag(self):
        if self.get_image():
            if self.get_image().get_visible():
                self.get_image().set_visible(False)
            else:
                self.get_image().set_visible(True)
        else:
            self.set_image(MinesweeperImage(FLAG_IMAGE))


class MinesweeperImage(Gtk.Image):

    def __init__(self, filename):
        Gtk.Image.__init__(self)
        pixbuf = Gdk.pixbuf_new_from_file(filename)
        pixbuf = pixbuf.scale_simple(CELL_SIZE - 1,
                                     CELL_SIZE - 1,
                                     Gdk.INTERP_BILINEAR)
        self.set_from_pixbuf(pixbuf)

def main():
    game = Minesweeper(DEFAULT_SIZE)
    game.run()

if __name__ == '__main__':
    main()