#!/usr/bin/env python
#
#===============================================================================
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
#
#===============================================================================
##
# @file    serPort.py
# @author  Hugh Spahr
# @date    6/6/2014
#
# @note    Open Pinball Project
# @note    Copyright 2014, Hugh Spahr
#
# @brief This is the serial port object.

#===============================================================================

import serial
import rs232Intf

## Card type enumeration.
#  Contains an entry for card type
class CardType:
    SOL_CARD            = 0
    INP_CARD            = 1
    
class SerPort():
    ## The constructor
    #
    #  @param  self          [in]   Object reference
    #  @param  comPort       [in]   COM port number.  Ex. COM1
    #  @return Returns info in self.error where 0 = no errors
    def __init__(self, comPort):
        self.error = 0
        self.debug = False
        self.numBrds = 0
        self.addrArr = []
        self.cardTypeArr = []
        self.currData = []
        self.kickSol = 0
        self.solKickVal = []
        self._brdCfg = []
        self._readCmd = []
        self._readInpStr = 0

        if comPort != None:
            self.debug = False
            try:
                self._ser=serial.Serial(comPort, baudrate=19200, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, timeout=.1)
            except serial.SerialException:
                print "Can't open COM port: %s" % comPort
                self.error = 100
            if self.error == 0:
                self.error = self.getInventory()
        else:
            self.debug = True
            self.error = self.getInventory()
            
    ## Get Data from serial port
    #
    #  @param  self          [in]   Object reference
    #  @param  numBytes      [in]   Number of bytes to read
    #  @return List of bytes that were read
    def getSerialData(self, numBytes):
        resp = self._ser.read(numBytes)
        return (resp)

    ## Get inventory
    #
    #  Grab the inventory and make sure a valid response was received.  Calculate
    #  number of solenoid boards and number of input boards.
    #
    #  @param  self          [in]   Object reference
    #  @return Can return CMD_OK if good, or INVENTORY_NO_RESP, BAD_INV_RESP,
    #     EXTRA_INFO_RCVD, BAD_NUM_CARDS, INV_MATCH_FAIL if an error
    #  @note   Don't know size of the response since it depends on the
    #     number of installed cards.
    def getInventory(self):
        if not self.debug:
            cmdArr = []
            cmdArr.append(rs232Intf.EOM_CMD)
            cmdArr.append(rs232Intf.EOM_CMD)
            cmdArr.append(rs232Intf.EOM_CMD)
            cmdArr.append(rs232Intf.EOM_CMD)
            cmdArr.append(rs232Intf.INV_CMD)
            cmdArr.append(rs232Intf.EOM_CMD)
            sendCmd = ''.join(cmdArr)
            self._ser.write(sendCmd)
            
            #add two extra bytes for command and EOM
            data = self.getSerialData(rs232Intf.MAX_NUM_INP_BRD + rs232Intf.MAX_NUM_SOL_BRD + 6)
            print repr(data)
        
        else:
            #Fake an inventory response
            data = []
            data.append(rs232Intf.INV_CMD)
            data.append(rs232Intf.CARD_ID_INP_CARD)
            data.append(rs232Intf.CARD_ID_SOL_CARD)
            data.append(rs232Intf.EOM_CMD)
            
        #Response must have inv command at start or return BAD_INV_RESP
        index = 0
        while ((data[index] != rs232Intf.INV_CMD) and (index < len(data))):
            index += 1
            
        #Response must have at least inv command and eom or return error
        if (len(data) == index):
            print "Inventory response fail, inventory command in response not found"
            return (101)
        if (data[index] != rs232Intf.INV_CMD):
            print "Inventory response fail.  Expected = 0x%02x, Rcvd = 0x%02x" % \
                (ord(rs232Intf.INV_CMD), data[index])
            return (102)
        index += 1
    
        while (data[index] != rs232Intf.EOM_CMD):
            if ((ord(data[index]) & ord(rs232Intf.CARD_ID_TYPE_MASK)) == ord(rs232Intf.CARD_ID_SOL_CARD)):
                self.numBrds += 1
                self.addrArr.append(ord(data[index]))
                self.cardTypeArr.append(CardType.SOL_CARD)
                self.currData.append(0)
                self.solKickVal.append(0)
    
                #add to the config/read cmd
                self._brdCfg.append(data[index])
                self._brdCfg.append(rs232Intf.CFG_SOL_CMD)
                for _ in xrange(rs232Intf.NUM_SOL_PER_BRD):
                    self._brdCfg.append(rs232Intf.CFG_SOL_USE_SWITCH)
                    self._brdCfg.append('\x20')
                    self._brdCfg.append('\x04')
                    
                self._readCmd.append(data[index])
                self._readCmd.append(rs232Intf.READ_SOL_INP_CMD)
                self._readCmd.append('\x00')
            elif ((ord(data[index]) & ord(rs232Intf.CARD_ID_TYPE_MASK)) == ord(rs232Intf.CARD_ID_INP_CARD)):
                self.numBrds += 1
                self.addrArr.append(ord(data[index]))
                self.cardTypeArr.append(CardType.INP_CARD)
                self.solKickVal.append(0)
                self.currData.append(0)
    
                #add to the config/read cmd
                self._brdCfg.append(data[index])
                self._brdCfg.append(rs232Intf.CFG_INP_CMD)
                for _ in xrange(rs232Intf.NUM_INP_PER_BRD):
                    self._brdCfg.append(rs232Intf.CFG_INP_STATE)
                    
                self._readCmd.append(data[index])
                self._readCmd.append(rs232Intf.READ_INP_BRD_CMD)
                self._readCmd.append('\x00')
                self._readCmd.append('\x00')
            index += 1
        self._brdCfg.append(rs232Intf.EOM_CMD)
        self._readCmd.append(rs232Intf.EOM_CMD)
        self._readInpStr = ''.join(self._readCmd)
        if (index + 1 != len(data)):
            return (103)
        
        #Send the config command, response should only EOM
        if not self.debug:
            sendCmd = ''.join(self._brdCfg)
            self._ser.write(sendCmd)
            data = self.getSerialData(5)
            if (len(data) != 1) or (data[0] != rs232Intf.EOM_CMD):
                return (104)
        
        return (0)

    ## Update serial port
    #
    # Look if any solenoid boards need to be kicked.  If so, send the
    # kick command.  Send status command to get state of inputs
    #
    #  @param  self          [in]   Object reference
    #  @return 0 if worked
    def update(self):
        #Check if a solenoid needs to be kicked
        if (self.kickSol != 0):
            currSolKick = self.kickSol
            self.kickSol &= ~currSolKick
            kickCmd = []
            clearCmd = []
            
            #Find out who needs to be kicked
            for index in xrange(self.numBrds):
                if (currSolKick & (1 << index)) != 0:
                    kickCmd.append(chr(self.addrArr[index]))
                    kickCmd.append(rs232Intf.KICK_SOL_CMD)
                    # Value
                    kickCmd.append(chr(self.solKickVal[index]))
                    # Mask
                    kickCmd.append(chr(self.solKickVal[index]))
                    
                    clearCmd.append(chr(self.addrArr[index]))
                    clearCmd.append(rs232Intf.KICK_SOL_CMD)
                    # Value
                    clearCmd.append('\x00')
                    # Mask
                    clearCmd.append(chr(self.solKickVal[index]))
                    self.solKickVal[index] = 0
            kickCmd.append(rs232Intf.EOM_CMD)
            
            #Send the command, response should only EOM
            if not self.debug:
                # Send the kick command
                sendCmd = ''.join(kickCmd)
                self._ser.write(sendCmd)
                data = self.getSerialData(5)
                if (len(data) != 1) or (data[0] != rs232Intf.EOM_CMD):
                    return (200)
                # Send clear the kick command
                sendCmd = ''.join(clearCmd)
                self._ser.write(sendCmd)
                data = self.getSerialData(5)
                if (len(data) != 1) or (data[0] != rs232Intf.EOM_CMD):
                    return (201)
                
        #Update the status inputs
        if not self.debug:
            sendCmd = ''.join(self._readCmd)
            self._ser.write(sendCmd)
            data = self.getSerialData(len(self._readCmd))
            if (len(data) != len(self._readCmd)):
                return (202)
            dataIndex = 0
            for cardNum in xrange(len(self.cardTypeArr)):
                if (self.cardTypeArr[cardNum] == CardType.SOL_CARD):
                    #Bytes are addr, cmd, data
                    if (ord(data[dataIndex]) != self.addrArr[cardNum]):
                        return (210)
                    if (data[dataIndex + 1] != rs232Intf.READ_SOL_INP_CMD):
                        return (211)
                    self.currData[cardNum] = ord(data[dataIndex + 2])
                    dataIndex += 3
                elif (self.cardTypeArr[cardNum] == CardType.INP_CARD):
                    #Bytes are addr, cmd, data
                    if (ord(data[dataIndex]) != self.addrArr[cardNum]):
                        return (220)
                    if (data[dataIndex + 1] != rs232Intf.READ_INP_BRD_CMD):
                        return (221)
                    self.currData[cardNum] = (ord(data[dataIndex + 2]) << 8) | ord(data[dataIndex + 3])
                    dataIndex += 4
                else:
                    return(230)
            if (data[dataIndex] != rs232Intf.EOM_CMD):
                return (240)
        return (0)            
