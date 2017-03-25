#!/usr/bin/env python

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import pygtk

pygtk.require('2.0')
import gtk, sys, random

#arrays of buttons and labels for those buttons ("M", " ", or a number)
buttons = []
labels = []

#default values overridable from command line
width = 10
height = 10
numMines = 10

def modifyButtonColor (prelight, normal, i, j):
    """modifies the colour of buttons[i][j], which is really annoying"""
    if prelight != "nocolor":
        buttons [i] [j].modify_bg (gtk.STATE_PRELIGHT, gtk.gdk.color_parse (prelight))
    if normal != "nocolor":
        buttons [i] [j].modify_bg (gtk.STATE_NORMAL, gtk.gdk.color_parse (normal))

class Minesweeper:
    #see resetGame method for behaviour
    gameOver = False
    resetting = False
    
    #hidden map of where the mines actually are
    mineMap = []

    #state of each button - unclicked ("neutral"), clicked, or flagged
    state = []
    numFlags = 0
    clicksToGo = -1
    ctgLabel = gtk.Label ()

    def addMines (self):
        """sets up the mineMap array, and fills in the hints"""
        for mine in range (numMines):
            i = random.randint (1, width) - 1
            j = random.randint (1, height) - 1
            while self.mineMap [i] [j] == "M":
                i = random.randint (1, width) - 1
                j = random.randint (1, height) - 1
            self.mineMap [i] [j] = "M"

            #and add 1 to the count of each adjacent square
            self.addHint (i-1, j-1)
            self.addHint (i-1, j)
            self.addHint (i-1, j+1)
            self.addHint (i, j-1)
            self.addHint (i, j+1)
            self.addHint (i+1, j-1)
            self.addHint (i+1, j)
            self.addHint (i+1, j+1)

    def addHint (self, i, j):
        """doesn't add to squares outside boundaries or with a mine"""
        if i < 0 or j < 0 or i >= width or j >= height:
            return
        if self.mineMap [i] [j] == "M":
            return
        self.mineMap [i] [j] += 1

    def convertHintsToStrings (self):
        """converts numbers in mineMap to strings after setting up mineMap"""
        for i in range (width):
            for j in range (height):
                if self.mineMap [i] [j] != "M":
                    self.mineMap [i] [j] = str (self.mineMap [i] [j])

    def resetGame (self):
        """sets up a new game"""
        self.resetting = True
        self.gameOver = False
        self.clicksToGo = width * height
        self.ctgLabel.set_text ("Clicks to go: %d" % self.clicksToGo)
        self.numFlags = 0
        for i in range (width):
            for j in range (height):
                self.mineMap [i] [j] = 0
                self.state [i] [j] = "neutral"
                labels [i] [j].set_text ("     ")
                modifyButtonColor ("black", "black", i, j)
                buttons [i] [j].set_active (False)
        self.addMines ()
        self.convertHintsToStrings ()
        self.resetting = False

    def expandZeros (self, c, r):
        """checks every adjacent square to a clicked square with 0 adjacent 
            mines"""
        list = []
        list.append ([c-1, r-1])
        list.append ([c-1, r])
        list.append ([c-1, r+1])
        list.append ([c, r-1])
        list.append ([c, r+1])
        list.append ([c+1, r-1])
        list.append ([c+1, r])
        list.append ([c+1, r+1])
        for box in list:
            i = box [0]
            j = box [1]
            if i >= 0 and j >= 0 and i < width and j < height:
                if self.state [i] [j] == "neutral":
                    self.leftClick (i, j)

    def checkWin (self):
        """if you win, it changes the mine squares to be green"""
        if self.clicksToGo - (numMines - self.numFlags) == 0:
            self.gameOver = True
            for i in range (width):
                for j in range (height):
                    if self.state [i] [j] != "clicked":
                        modifyButtonColor ("green", "green", i, j)
            self.gameOver = True
            self.ctgLabel.set_text ("You win!")

    def lose (self):
        """reveals the map and ends the game"""
        for i in range (width):
            for j in range (height):
                self.state [i] [j] = "clicked"
                if self.mineMap [i] [j] == "0":
                    labels [i] [j].set_text ("     ")
                else:
                    labels [i][j].set_text (str(self.mineMap [i] [j]))
                modifyButtonColor ("gray", "gray", i, j)
                buttons [i] [j].set_active (True)
        self.gameOver = True
        self.ctgLabel.set_text ("You lose!")

    def leftClick (self, i, j):
        """does what is required for unclicked squares
            Mine: lose the game
            A number: display that number
            No adjacent mines: check adjacent squares automatically"""

        buttons [i] [j].set_active (True)
        if self.state [i] [j] != "neutral":
            return

        #"clicks" the button and updates values
        value = self.mineMap [i] [j]
        if self.mineMap [i] [j] != "0":
            labels [i] [j].set_text (self.mineMap [i] [j])
        modifyButtonColor ("gray", "gray", i, j)
        self.state [i] [j] = "clicked"
        self.clicksToGo -= 1
        self.ctgLabel.set_text ("Clicks to go: %d" % self.clicksToGo)
        
        #if you clicked a mine!
        if value == "M":
            self.lose ()
        #if you clicked a square with no adjacent mines
        elif value == "0":
            self.expandZeros (i, j)
        self.checkWin ()

    def rightClick (self, widget, i, j):
        """toggles flagged state for unclicked squares"""
        if self.state [i] [j] == "clicked":
            return
        elif self.state [i] [j] == "flagged":
            self.state [i] [j] = "neutral"
            modifyButtonColor ("black", "black", i, j)
            self.numFlags -= 1
            self.clicksToGo += 1
            self.ctgLabel.set_text ("Clicks to go: %d" % self.clicksToGo)
        else:
            self.state [i] [j] = "flagged"
            modifyButtonColor ("red", "red", i, j)
            self.numFlags += 1
            self.clicksToGo -= 1
            self.ctgLabel.set_text ("Clicks to go: %d" % self.clicksToGo)
        self.checkWin ()

    def on_button_press_event (self, widget, event, data):
        """separates left clicks from right clicks. Also suppresses clicks if
            the game shouldn't be running"""
        i = data [0]
        j = data [1]
        
        if self.resetting or self.gameOver:
            if self.state [i] [j] == "clicked":
                buttons [i] [j].set_active (False)
            return

        if event.type == gtk.gdk.BUTTON_PRESS and event.button == 3:
            self.rightClick (widget, i, j)
        elif event.type == gtk.gdk.BUTTON_PRESS and event.button == 1:
            self.leftClick (i, j)

    # This callback quits the program
    def delete_event(self, widget, event, data=None):
        gtk.main_quit()
        return False

    def __init__(self):
        # Create a new window
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_title("Minesweeper")
        self.window.set_border_width (10)
        self.window.connect("delete_event", self.delete_event)

        #fill a table, simultaneously creating four data lists
        table = gtk.Table (height + 3, width, True)
        for i in range (width):
            buttons.append ([])
            labels.append ([])
            self.mineMap.append ([])
            self.state.append ([])
            for j in range (height):
                #game stuff
                self.mineMap [i].append (0)
                self.state [i].append ("neutral")

                #gui stuff
                buttons [i].append (gtk.ToggleButton ())
                labels [i].append (gtk.Label ())
                buttons [i][j].add (labels [i][j])
                buttons [i][j].connect ("button-press-event", self.on_button_press_event, [i, j])
                table.attach (buttons [i] [j], i, i + 1, j, j + 1)
                buttons [i][j].show ()
                labels [i][j].show ()

        #quit button
        button = gtk.Button("Quit")
        button.connect("clicked", lambda w: gtk.main_quit())
        table.attach (button, 0, width, height, height + 1)
        button.show()

        #restart button
        button = gtk.Button ("Restart")
        button.connect ("clicked", lambda w: self.resetGame ())
        table.attach (button, 0, width, height + 1, height + 2)
        button.show ()

        #"clicks to go" text field
        table.attach (self.ctgLabel, 0, width, height + 2, height + 3)
        self.ctgLabel.show ()

        #set up the first game
        self.resetGame ()

        #show the game
        self.window.add (table)
        table.show ()
        self.window.show()

def main():
    gtk.main()
    return 0       

if __name__ == "__main__":
    if len (sys.argv) == 4:
        width = int (sys.argv [1])
        height = int (sys.argv [2])
        numMines = int (sys.argv [3])
    elif len (sys.argv) == 3:
        width = int (sys.argv [1])
        height = int (sys.argv [2])
    elif len (sys.argv) != 1:
        print "Usage: ", sys.argv [0], " width height [numMines]"
        sys.exit (1)
    Minesweeper()
    main()
