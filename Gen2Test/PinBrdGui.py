#!/usr/bin/env python
#
#===============================================================================
## @mainpage
#
#                           OOOO
#                         OOOOOOOO
#        PPPPPPPPPPPPP   OOO    OOO   PPPPPPPPPPPPP
#      PPPPPPPPPPPPPP   OOO      OOO   PPPPPPPPPPPPPP
#     PPP         PPP   OOO      OOO   PPP         PPP
#    PPP          PPP   OOO      OOO   PPP          PPP
#    PPP          PPP   OOO      OOO   PPP          PPP
#    PPP          PPP   OOO      OOO   PPP          PPP
#     PPP         PPP   OOO      OOO   PPP         PPP
#      PPPPPPPPPPPPPP   OOO      OOO   PPPPPPPPPPPPPP
#       PPPPPPPPPPPPP   OOO      OOO   PPP
#                 PPP   OOO      OOO   PPP
#                 PPP   OOO      OOO   PPP
#                 PPP   OOO      OOO   PPP
#                 PPP    OOO    OOO    PPP
#                 PPP     OOOOOOOO     PPP
#                PPPPP      OOOO      PPPPP
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

#===============================================================================
##
# @file    PinBrdGui.py
# @author  Hugh Spahr
# @date    6/6/2014
#
# @note    Open Pinball Project
# @note    Copyright 2014, Hugh Spahr
#
# @brief Main entry point to the board GUI for watching board inputs/kicking
# solenoids.

#===============================================================================

from sys import argv, exit
from Tkinter import *
from ttk import *
from serPort import SerPort, CardType
import time


## GUI Frame
#
#  Create TK GUI frame.
#
#  @param  argv          [in]   Passed in arguments
#  @return None 
class GuiFrame(Frame):
  
    ## The constructor
    #
    #  @param  self          [in]   Object reference
    #  @param  parent        [in]   Root object reference
    #  @param  serObj        [in]   Serial port object reference
    #  @return None
    def __init__(self, parent, serObj):
        self.exit = False
        self.parent = parent
        self.serObj = serObj
        self.strVar = []
        self.comboBox = []
        self.optBoxStr = []
        self.status = None
        self.persistValue = []
        self.persistTime = []
        
        self.initUI()
    
    ## Button press
    #
    #  Called when the button is pressed.  
    #
    #  @param  self          [in]   Object reference
    #  @param  cardNum       [in]   Card number
    #  @return None
    def btnPress(self, cardNum):
        #Get the value of the combobox
        data = int(self.comboBox[cardNum].get())
        self.serObj.solKickVal[cardNum] = (1 << (data - 1))
        self.serObj.kickSol |= (1 << cardNum)
        
    ## Init UI
    #
    #  Initialize the user interface.  Create the cmd panel at the
    #  top which contains the status and column headings.  Walk
    #  through the cardType array and create a panel for each card.
    #
    #  @param  self          [in]   Object reference
    #  @return None
    def initUI(self):
        self.parent.wm_title("Pin Board GUI")
        self.parent.columnconfigure(0, weight=1)
        self.parent.rowconfigure(0, weight=1)
        self.bgndFrm = Frame(self.parent)
        self.bgndFrm.grid()
        
        self.cmdPanel()
        
        for index in xrange(len(self.serObj.cardTypeArr)):
            if self.serObj.cardTypeArr[index] == CardType.INP_CARD:
                self.inpPanel(index)
            if self.serObj.cardTypeArr[index] == CardType.SOL_CARD:
                self.solPanel(index)
        
    ## Create command panel
    #
    #  Create the command panel.  It contains the status string var which
    #  contains the status of the GUI.  (Errors are presented as a decimal
    #  number.)
    #
    #  @param  self          [in]   Object reference
    #  @return None
    def cmdPanel(self):
        tmpFrm = Frame(self.bgndFrm, borderwidth = 5, relief=RAISED)
        tmpFrm.grid()
        tmpFrm.grid(column = 0, row = 0)
        tmpLbl = Label(tmpFrm, text="Board", width = 20, anchor=CENTER)
        tmpLbl.grid(column = 0, row = 0, columnspan = 2,  padx=4, pady=8)
        tmpLbl = Label(tmpFrm, text="Addr", width = 8, anchor=CENTER)
        tmpLbl.grid(column = 2, row = 0, padx=4, pady=8)
        tmpLbl = Label(tmpFrm, text="Status", width = 10, anchor=CENTER)
        tmpLbl.grid(column = 3, row = 0, padx=4, pady=8)
        tmpLbl = Label(tmpFrm, text="", width = 13)
        tmpLbl.grid(column = 4, row = 0)
        self.status = StringVar()
        self.status.set("None")
        tmpLbl = Label(tmpFrm, textvariable=self.status, relief=SUNKEN, width=12, anchor=CENTER)
        tmpLbl.grid(column = 5, row = 0)
        
    ## Create input card panel
    #
    #  Create an input card command panel.  It contains the address of the card,
    #  and a status field for report current input status from the card.
    #
    #  @param  self          [in]   Object reference
    #  @param  panelNum      [in]   Index of card (0 based)
    #  @return None
    def inpPanel(self, panelNum):
        tmpFrm = Frame(self.bgndFrm, borderwidth = 5, relief=RAISED)
        tmpFrm.grid()
        tmpFrm.grid(column = 0, row = panelNum + 1)
        inpBrdNum = (self.serObj.addrArr[panelNum] & 0xf) + 1
        tmpLbl = Label(tmpFrm, text="Input Brd #%d" % inpBrdNum, width = 20, anchor=CENTER)
        tmpLbl.grid(column = 0, row = 0, columnspan = 2,  padx=4, pady=8)
        tmpLbl = Label(tmpFrm, text="0x%02x" % self.serObj.addrArr[panelNum], relief=SUNKEN, anchor=CENTER, width = 8)
        tmpLbl.grid(column = 2, row = 0, padx=8, pady=8)
        tmpStrVar = StringVar()
        data = 0
        tmpStrVar.set("0x%04x" % data)
        self.strVar.append(tmpStrVar)
        self.persistValue.append([])
        self.persistTime.append([])
        self.comboBox.append(None)
        tmpLbl = Label(tmpFrm, textvariable=tmpStrVar, relief=SUNKEN, width=10, anchor=CENTER)
        tmpLbl.grid(column = 3, row = 0, padx=8, pady=8)
        tmpLbl = Label(tmpFrm, text="", width = 12)
        tmpLbl.grid(column = 4, row = 0)
        tmpLbl = Label(tmpFrm, text="", width = 11)
        tmpLbl.grid(column = 5, row = 0)
    
    ## Create solenoid card panel
    #
    #  Create an solenoid card command panel.  It contains the address of the card,
    #  a status field for report current input status, and a button to kick a
    #  solenoid.  A choice box is used to choose which solenoid on the card.
    #
    #  @param  self          [in]   Object reference
    #  @param  panelNum      [in]   Index of card (0 based)
    #  @return None
    def solPanel(self, panelNum):
        tmpFrm = Frame(self.bgndFrm, borderwidth = 5, relief=RAISED)
        tmpFrm.grid()
        tmpFrm.grid(column = 0, row = panelNum + 1)
        solBrdNum = (self.serObj.addrArr[panelNum] & 0xf) + 1
        tmpLbl = Label(tmpFrm, text="Solenoid Brd #%d" % solBrdNum, width = 20, anchor=CENTER)
        tmpLbl.grid(column = 0, row = 0, columnspan = 2,  padx=4, pady=8)
        tmpLbl = Label(tmpFrm, text="0x%02x" % self.serObj.addrArr[panelNum], relief=SUNKEN, anchor=CENTER, width = 8)
        tmpLbl.grid(column = 2, row = 0, padx=8, pady=8)
        tmpStrVar = StringVar()
        data = 0
        tmpStrVar.set("0x%02x" % data)
        self.strVar.append(tmpStrVar)
        self.persistValue.append([])
        self.persistTime.append([])
        tmpLbl = Label(tmpFrm, textvariable=tmpStrVar, relief=SUNKEN, width=10, anchor=CENTER)
        tmpLbl.grid(column = 3, row = 0, padx=8, pady=8)
        tmpBtn = Button(tmpFrm, width = 12, text="Kick Sol", command=lambda tmp=panelNum: self.btnPress(tmp))
        tmpBtn.grid(column = 4, row = 0, padx=4, pady=8)
        tmpStrVar = StringVar()
        self.optBoxStr = tmpStrVar
        tmpCB = Combobox(tmpFrm, textvariable=tmpStrVar, width=6, state="readonly")
        tmpCB["values"] = ("1", "2", "3", "4", "5", "6", "7", "8")
        tmpCB.current(0)
        self.comboBox.append(tmpCB)
        tmpCB.grid(column = 5, row = 0)
        
    ## Update read input states
    #
    #  Update the state variables using input read from the cards.  Field in
    #  GUI is only updated if it changes.
    #
    #  @param  self          [in]   Object reference
    #  @return None
    def updateState(self):
        for cardNum in xrange(len(self.serObj.cardTypeArr)):
            if (self.serObj.cardTypeArr[cardNum] == CardType.INP_CARD):
                self.strVar[cardNum].set("0x%04x" % self.serObj.currData[cardNum])
            elif (self.serObj.cardTypeArr[cardNum] == CardType.SOL_CARD):
                # Solenoid's data doesn't persist, so an edge is only presented once.
                # Add persistence so it is easier to see for the user
                data = self.serObj.currData[cardNum]
                currTime = time.time()
                if (data != 0):
                    self.persistTime[cardNum].append(currTime)
                    self.persistValue[cardNum].append(data)
                # OR in previous non-zero values that are persisting
                # Walk backwards through the list so items can be removed
                for index in xrange(len(self.persistValue[cardNum]) - 1, -1, -1):
                    data |= self.persistValue[cardNum][index]
                    # Time is in seconds, so this will persist for more than 1 sec
                    if (currTime - self.persistTime[cardNum][index] > 1):
                        del self.persistValue[cardNum][index]
                        del self.persistTime[cardNum][index]
                self.strVar[cardNum].set("0x%02x" % data)

    ## GUI exit
    #
    #  Set the exit flag.
    #
    #  @param  self          [in]   Object reference
    #  @return None
    def gui_exit(self):
        self.exit = True

## Main
#
#  Read passed in arguments and set seral port number.  Run
#  inventory command to get inventory of cards.  Create
#  TK window.
#
#  @param  argv          [in]   Passed in arguments
#  @return None 
def main(argv=None):

    end = False

    comPort = None
    if argv is None:
        argv = sys.argv
    for arg in argv:
        if arg.startswith('-port='):
            comPort = arg[6:]
        elif arg.startswith('-?'):
            print "python PinBrdGui.py [OPTIONS]"
            print "    -?                 Options Help"
            print "    -port=             COM port number (ex. COM1)"
            end = True
    if end:
        return 0
    
    #Open the COM port
    serPortObj = SerPort(comPort)
    if serPortObj.error != 0:
        return (serPortObj.error)
        
    root = Tk()
    gui = GuiFrame(root, serPortObj)
    root.wm_protocol ("WM_DELETE_WINDOW", gui.gui_exit)
    while not gui.exit:
        retVal = serPortObj.update()
        if retVal:
            gui.status.set("%d" % retVal)
        gui.updateState()
        root.update()
    return (0)

if __name__ == "__main__":
    sys.exit(main())
