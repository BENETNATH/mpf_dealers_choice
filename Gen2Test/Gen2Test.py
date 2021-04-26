#!/usr/bin/env python
#
#===============================================================================
#
#                         OOOO
#                       OOOOOOOO
#      PPPPPPPPPPPPP   OOO    OOO   PPPPPPPPPPPPP
#    PPPPPPPPPPPPPP   OOO      OOO   PPPPPPPPPPPPPP
#   PPP         PPP   OOO      OOO   PPP         PPP
#  PPP          PPP   OOO      OOO   PPP          PPP
#  PPP          PPP   OOO      OOO   PPP          PPP
#  PPP          PPP   OOO      OOO   PPP          PPP
#   PPP         PPP   OOO      OOO   PPP         PPP
#    PPPPPPPPPPPPPP   OOO      OOO   PPPPPPPPPPPPPP
#     PPPPPPPPPPPPP   OOO      OOO   PPP
#               PPP   OOO      OOO   PPP
#               PPP   OOO      OOO   PPP
#               PPP   OOO      OOO   PPP
#               PPP    OOO    OOO    PPP
#               PPP     OOOOOOOO     PPP
#              PPPPP      OOOO      PPPPP
#
# @file:   Gen2Test.py
# @author: Hugh Spahr
# @date:   12/12/2015
#
# @note:   Open Pinball Project
#          Copyright 2015, Hugh Spahr
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
#
# Tests for Gen2 cards based off input driver tests.
#
#===============================================================================

testVers = '00.00.10'

import sys
import serial
import array
import time
import re
import rs232Intf
import os

port = 'COM3'
testNum = 255
card = 0
data = ""
NUM_MSGS = 1
currInpData = []
matrixInpData = []
numGen2Brd = 0
gen2AddrArr = []
currWingCfg = []
cardVersion = []
cardSerNum = []
hasMatrix = []
newestVers = "0.0.0.0"

CRC8ByteLookup = \
    [ 0x00, 0x07, 0x0e, 0x09, 0x1c, 0x1b, 0x12, 0x15, 0x38, 0x3f, 0x36, 0x31, 0x24, 0x23, 0x2a, 0x2d, \
      0x70, 0x77, 0x7e, 0x79, 0x6c, 0x6b, 0x62, 0x65, 0x48, 0x4f, 0x46, 0x41, 0x54, 0x53, 0x5a, 0x5d, \
      0xe0, 0xe7, 0xee, 0xe9, 0xfc, 0xfb, 0xf2, 0xf5, 0xd8, 0xdf, 0xd6, 0xd1, 0xc4, 0xc3, 0xca, 0xcd, \
      0x90, 0x97, 0x9e, 0x99, 0x8c, 0x8b, 0x82, 0x85, 0xa8, 0xaf, 0xa6, 0xa1, 0xb4, 0xb3, 0xba, 0xbd, \
      0xc7, 0xc0, 0xc9, 0xce, 0xdb, 0xdc, 0xd5, 0xd2, 0xff, 0xf8, 0xf1, 0xf6, 0xe3, 0xe4, 0xed, 0xea, \
      0xb7, 0xb0, 0xb9, 0xbe, 0xab, 0xac, 0xa5, 0xa2, 0x8f, 0x88, 0x81, 0x86, 0x93, 0x94, 0x9d, 0x9a, \
      0x27, 0x20, 0x29, 0x2e, 0x3b, 0x3c, 0x35, 0x32, 0x1f, 0x18, 0x11, 0x16, 0x03, 0x04, 0x0d, 0x0a, \
      0x57, 0x50, 0x59, 0x5e, 0x4b, 0x4c, 0x45, 0x42, 0x6f, 0x68, 0x61, 0x66, 0x73, 0x74, 0x7d, 0x7a, \
      0x89, 0x8e, 0x87, 0x80, 0x95, 0x92, 0x9b, 0x9c, 0xb1, 0xb6, 0xbf, 0xb8, 0xad, 0xaa, 0xa3, 0xa4, \
      0xf9, 0xfe, 0xf7, 0xf0, 0xe5, 0xe2, 0xeb, 0xec, 0xc1, 0xc6, 0xcf, 0xc8, 0xdd, 0xda, 0xd3, 0xd4, \
      0x69, 0x6e, 0x67, 0x60, 0x75, 0x72, 0x7b, 0x7c, 0x51, 0x56, 0x5f, 0x58, 0x4d, 0x4a, 0x43, 0x44, \
      0x19, 0x1e, 0x17, 0x10, 0x05, 0x02, 0x0b, 0x0c, 0x21, 0x26, 0x2f, 0x28, 0x3d, 0x3a, 0x33, 0x34, \
      0x4e, 0x49, 0x40, 0x47, 0x52, 0x55, 0x5c, 0x5b, 0x76, 0x71, 0x78, 0x7f, 0x6a, 0x6d, 0x64, 0x63, \
      0x3e, 0x39, 0x30, 0x37, 0x22, 0x25, 0x2c, 0x2b, 0x06, 0x01, 0x08, 0x0f, 0x1a, 0x1d, 0x14, 0x13, \
      0xae, 0xa9, 0xa0, 0xa7, 0xb2, 0xb5, 0xbc, 0xbb, 0x96, 0x91, 0x98, 0x9f, 0x8a, 0x8d, 0x84, 0x83, \
      0xde, 0xd9, 0xd0, 0xd7, 0xc2, 0xc5, 0xcc, 0xcb, 0xe6, 0xe1, 0xe8, 0xef, 0xfa, 0xfd, 0xf4, 0xf3 ]

# Config of test setup
wingCfg = [ [ rs232Intf.WING_NEO, rs232Intf.WING_SOL, rs232Intf.WING_INP, rs232Intf.WING_INCAND ] ]

# Config inputs as all state inputs
inpCfg = [ [ rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE, \
             rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE, \
             rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE, \
             rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE, \
             rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE, \
             rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE, \
             rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE, \
             rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE ] ]

# Config for solenoid wing board in second position, first two config'd as flippers, second two config'd as one-shots
solCfg =  [ [ '\x00', '\x00', '\x00', '\x00', '\x00', '\x00',
              '\x00', '\x00', '\x00', '\x00', '\x00', '\x00',
              rs232Intf.CFG_SOL_USE_SWITCH, '\x30', '\x04', rs232Intf.CFG_SOL_USE_SWITCH, '\x30', '\x04', \
              rs232Intf.CFG_SOL_USE_SWITCH, '\x10', '\x00', rs232Intf.CFG_SOL_USE_SWITCH, '\x10', '\x00', \
              '\x00', '\x00', '\x00', '\x00', '\x00', '\x00', \
              '\x00', '\x00', '\x00', '\x00', '\x00', '\x00', \
              '\x00', '\x00', '\x00', '\x00', '\x00', '\x00', \
              '\x00', '\x00', '\x00', '\x00', '\x00', '\x00' ] ]

# Config color table
#              Entry 0                 Entry 1                 Entry 2                 Entry 3 */
colorCfg = [ [ '\xff', '\x00', '\x00', '\x00', '\xff', '\x00', '\x00', '\x00', '\xff', '\xff', '\xff', '\x00', \
               '\xff', '\x00', '\xff', '\x00', '\xff', '\xff', '\xff', '\xff', '\xff', '\x00', '\x00', '\x00', \
               '\x00', '\x00', '\x00', '\x00', '\x00', '\x00', '\x00', '\x00', '\x00', '\x00', '\x00', '\x00', \
               '\x00', '\x00', '\x00', '\x00', '\x00', '\x00', '\x00', '\x00', '\x00', '\x00', '\x00', '\x00', \
               '\x00', '\x00', '\x00', '\x00', '\x00', '\x00', '\x00', '\x00', '\x00', '\x00', '\x00', '\x00', \
               '\x00', '\x00', '\x00', '\x00', '\x00', '\x00', '\x00', '\x00', '\x00', '\x00', '\x00', '\x00', \
               '\x00', '\x00', '\x00', '\x00', '\x00', '\x00', '\x00', '\x00', '\x00', '\x00', '\x00', '\x00', \
               '\x00', '\x00', '\x00', '\x00', '\x00', '\x00', '\x00', '\x00', '\x00', '\x00', '\x00', '\x00', \
               '\x10', \
            ] ]

#calculate a crc8
def calcCrc8(msgChars):
    crc8Byte = 0xff
    for indChar in msgChars:
        indInt = ord(indChar)
        crc8Byte = CRC8ByteLookup[crc8Byte ^ indInt];
    return (chr(crc8Byte))

def getChar():
    global windows
    if windows:
        return msvcrt.getch()
    else:
        fd = sys.stdin.fileno()
        oldSettings = termios.tcgetattr(fd)

        try:
            tty.setcbreak(fd)
            answer = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, oldSettings)

        return answer

def kbHit():
    global windows
    if windows:
        return msvcrt.kbhit()
    else:
        return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])

def getAsynchChar():
    global windows
    if windows:
        return msvcrt.getch()
    else:
        return sys.stdin.read(1)

def writeNoCR(text):
    global windows
    sys.stdout.write(text)
    if windows == False:
        sys.stdout.flush()

#grab data from serial port
def getSerialData():
    global ser
    resp = ser.read(100)
    return (resp)

#send inventory cmd
def sendInvCmd():
    global ser
    cmdArr = []
    cmdArr.append(rs232Intf.INV_CMD)
    cmdArr.append(rs232Intf.EOM_CMD)
    sendCmd = ''.join(cmdArr)
    ser.write(sendCmd)

#rcv inventory resp
def rcvInvResp(append = True):
    global numGen2Brd
    global gen2AddrArr
    global currInpData
    global matrixInpData

    global hasMatrix
    global currWingCfg
    data = getSerialData();
    #First byte should be inventory cmd
    index = 1
    if (len(data) == 0):
        print "No data received.  Are the Tx/Rx jumpers installed?"
        return (100)
    if (data[0] != rs232Intf.INV_CMD):
        return (101)
    if (len(data) < index + 1):
        print "Could not find EOM."
        return (102)
    numGen2Brd = 0
    gen2AddrArr = []
    while (data[index] != rs232Intf.EOM_CMD):
        if ((ord(data[index]) & ord(rs232Intf.CARD_ID_TYPE_MASK)) == ord(rs232Intf.CARD_ID_GEN2_CARD)):
            numGen2Brd = numGen2Brd + 1
            gen2AddrArr.append(data[index])
            if (append):
                currInpData.append(0)
                currWingCfg.append(0)
                hasMatrix.append(False)
                matrixInpData.append([0,0,0,0,0,0,0,0])
        index = index + 1
        if (len(data) < index + 1):
            print "Could not find EOM."
            return (103)
    print "Found %d Gen2 brds." % numGen2Brd
    print "Addr = %s" % [hex(ord(n)) for n in gen2AddrArr]
    return (0)

#send input cfg cmd
def sendInpCfgCmd(cardNum):
    global ser
    global numGen2Brd
    global gen2AddrArr
    if (cardNum >= numGen2Brd):
        return (200)    
    cmdArr = []
    cmdArr.append(gen2AddrArr[cardNum])
    cmdArr.append(rs232Intf.CFG_INP_CMD)
    for loop in range(rs232Intf.NUM_G2_INP_PER_BRD):
        if loadCfg:
            cmdArr.append(cfgFile.inpCfg[cardNum][loop])
        else:
            cmdArr.append(inpCfg[cardNum][loop])
    cmdArr.append(calcCrc8(cmdArr))
    cmdArr.append(rs232Intf.EOM_CMD)
    sendCmd = ''.join(cmdArr)
    ser.write(sendCmd)
    return (0)

#rcv end of message resp
def rcvEomResp():
    data = getSerialData();
    if (data[0] != rs232Intf.EOM_CMD):
        return (300)
    return (0)

#send 4 byte data command
def send4ByteDataCmd(cardNum, cmd):
    global ser
    global numGen2Brd
    global gen2AddrArr
    if (cardNum >= numGen2Brd):
        return (400)
    cmdArr = []
    cmdArr.append(gen2AddrArr[cardNum])
    cmdArr.append(cmd)
    cmdArr.append('\x00')
    cmdArr.append('\x00')
    cmdArr.append('\x00')
    cmdArr.append('\x00')
    cmdArr.append(calcCrc8(cmdArr))
    cmdArr.append(rs232Intf.EOM_CMD)
    sendCmd = ''.join(cmdArr)
    ser.write(sendCmd)
    return (0)

#send read input board
def sendReadInpBrdCmd(cardNum):
    return (send4ByteDataCmd(cardNum, rs232Intf.READ_GEN2_INP_CMD))

#rcv read input cmd
def rcvReadInpResp(cardNum):
    global ser
    global numGen2Brd
    global gen2AddrArr
    global currInpData
    data = getSerialData();
    if (data[0] != gen2AddrArr[cardNum]):
        print "\nData = %d, expected = %d" % (ord(data[0]),ord(gen2AddrArr[cardNum]))
        print repr(data)
        return (500)
    if (data[1] != rs232Intf.READ_GEN2_INP_CMD):
        print "\nData = %d, expected = %d" % (ord(data[1]),ord(rs232Intf.READ_GEN2_INP_CMD))
        print repr(data)
        return (501)
    tmpData = [ data[0], data[1], data[2], data[3], data[4], data[5] ]
    crc8 = calcCrc8(tmpData)
    if (data[6] != crc8):
        print "\nBad CRC, Data = %d, expected = %d" % (ord(data[6]),crc8)
        return (502)
    if (data[7] != rs232Intf.EOM_CMD):
        print "\nData = %d, expected = %d" % (ord(data[7]),ord(rs232Intf.EOM_CMD))
        return (502)
    currInpData[cardNum] = (ord(data[2]) << 24) | (ord(data[3]) << 16) | (ord(data[4]) << 8) | ord(data[5])
    return (0)

#send read matrix command
def sendReadMatrixCmd(cardNum):
    global ser
    global numGen2Brd
    global gen2AddrArr
    if (cardNum >= numGen2Brd):
        return (1500)
    cmdArr = []
    cmdArr.append(gen2AddrArr[cardNum])
    cmdArr.append(rs232Intf.READ_MATRIX_INP_CMD)
    cmdArr.append('\x00')
    cmdArr.append('\x00')
    cmdArr.append('\x00')
    cmdArr.append('\x00')
    cmdArr.append('\x00')
    cmdArr.append('\x00')
    cmdArr.append('\x00')
    cmdArr.append('\x00')
    cmdArr.append(calcCrc8(cmdArr))
    cmdArr.append(rs232Intf.EOM_CMD)
    sendCmd = ''.join(cmdArr)
    ser.write(sendCmd)
    return (0)

#rcv read matrix response
def rcvReadMatrixResp(cardNum):
    global ser
    global numGen2Brd
    global gen2AddrArr
    global matrixInpData
    data = getSerialData();
    if (data[0] != gen2AddrArr[cardNum]):
        print "\nData = %d, expected = %d" % (ord(data[0]),ord(gen2AddrArr[cardNum]))
        print repr(data)
        return (1600)
    if (data[1] != rs232Intf.READ_MATRIX_INP_CMD):
        print "\nData = %d, expected = %d" % (ord(data[1]),ord(rs232Intf.READ_MATRIX_INP_CMD))
        print repr(data)
        return (1601)
    tmpData = [ data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8], data[9] ]
    crc8 = calcCrc8(tmpData)
    if (data[10] != crc8):
        print "\nBad CRC, Data = %d, expected = %d" % (ord(data[10]),crc8)
        return (1602)
    if (data[11] != rs232Intf.EOM_CMD):
        print "\nData = %d, expected = %d" % (ord(data[11]),ord(rs232Intf.EOM_CMD))
        return (1602)
    for index in xrange(rs232Intf.NUM_G2_MATRIX_INP/8):
        matrixInpData[cardNum][index] = ord(data[index + 2])
    return (0)

#send sol cfg cmd
def sendSolCfgCmd(cardNum):
    global ser
    global numGen2Brd
    global gen2AddrArr
    if (cardNum >= numGen2Brd):
        return (600)    
    cmdArr = []
    cmdArr.append(gen2AddrArr[cardNum])
    cmdArr.append(rs232Intf.CFG_SOL_CMD)
    for loop in xrange(rs232Intf.NUM_G2_SOL_PER_BRD):
        if loadCfg:
            cmdArr.append(cfgFile.solCfg[cardNum][loop * 3])
            cmdArr.append(cfgFile.solCfg[cardNum][(loop * 3) + 1])
            cmdArr.append(cfgFile.solCfg[cardNum][(loop * 3) + 2])
        else:
            cmdArr.append(solCfg[cardNum][loop * 3])
            cmdArr.append(solCfg[cardNum][(loop * 3) + 1])
            cmdArr.append(solCfg[cardNum][(loop * 3) + 2])
    cmdArr.append(calcCrc8(cmdArr))
    cmdArr.append(rs232Intf.EOM_CMD)
    sendCmd = ''.join(cmdArr)
    ser.write(sendCmd)
    return (0)

#send read wing cfg board
def sendReadWingCfgCmd(cardNum):
    return (send4ByteDataCmd(cardNum, rs232Intf.GET_GEN2_CFG))

#rcv read wing cfg resp
def rcvReadWingCfgResp(cardNum):
    global ser
    global gen2AddrArr
    global currWingCfg
    global hasMatrix
    data = getSerialData();
    if (data[0] != gen2AddrArr[cardNum]):
        print "\nData = %d, expected = %d" % (ord(data[0]),ord(gen2AddrArr[cardNum]))
        print repr(data)
        return (700)
    if (data[1] != rs232Intf.GET_GEN2_CFG):
        print "\nData = %d, expected = %d" % (ord(data[1]),ord(rs232Intf.GET_GEN2_CFG))
        print repr(data)
        return (701)
    tmpData = [ data[0], data[1], data[2], data[3], data[4], data[5] ]
    crc8 = calcCrc8(tmpData)
    if (data[6] != crc8):
        print "\nBad CRC, Data = %d, expected = %d" % (ord(data[6]),crc8)
        return (702)
    if (data[7] != rs232Intf.EOM_CMD):
        print "\nData = %d, expected = %d" % (ord(data[7]),ord(rs232Intf.EOM_CMD))
        return (703)
    currWingCfg[cardNum] = (ord(data[2]) << 24) | (ord(data[3]) << 16) | (ord(data[4]) << 8) | ord(data[5])
    print hex(ord(gen2AddrArr[cardNum])),"WingCfg = 0x{:08x}".format(currWingCfg[cardNum])
    print hex(ord(gen2AddrArr[cardNum])),
    for index in xrange(rs232Intf.NUM_G2_WING_PER_BRD):
        outStr = "W[%d]:" % index
        if data[index + 2] == rs232Intf.WING_SOL:
            outStr += "SOL_WING"
        elif data[index + 2] == rs232Intf.WING_INP:
            outStr += "INP_WING"
        elif data[index + 2] == rs232Intf.WING_INCAND:
            outStr += "INCAND_WING"
        elif data[index + 2] == rs232Intf.WING_SW_MATRIX_OUT:
            outStr += "SW_MATRIX_OUT_WING"
        elif data[index + 2] == rs232Intf.WING_SW_MATRIX_IN:
            outStr += "SW_MATRIX_IN_WING"
            hasMatrix[cardNum] = True
        elif data[index + 2] == rs232Intf.WING_NEO:
            outStr += "NEO_WING"
        elif data[index + 2] == rs232Intf.WING_HI_SIDE_INCAND:
            outStr += "INCAND_HI_WING"
        elif data[index + 2] == rs232Intf.WING_NEO_SOL:
            outStr += "NEO_SOL_WING"
        elif data[index + 2] == rs232Intf.WING_SPI:
            outStr += "SPI_WING"
        elif data[index + 2] == rs232Intf.WING_SW_MATRIX_OUT_LOW:
            outStr += "SW_MATRIX_OUT_LOW_WING"
        elif data[index + 2] == rs232Intf.WING_LAMP_MATRIX_COL:
            outStr += "LAMP_MATRIX_COL_WING"
        elif data[index + 2] == rs232Intf.WING_LAMP_MATRIX_ROW:
            outStr += "LAMP_MATRIX_ROW_WING"
        else:
            outStr += "Error"
        if index < rs232Intf.NUM_G2_WING_PER_BRD - 1:
            outStr += ","
            print outStr,
        else:
            print outStr
    return (0)

#send wing cfg cmd
def sendWingCfgCmd(cardNum):
    global ser
    global numGen2Brd
    global gen2AddrArr
    if (cardNum >= numGen2Brd):
        return (800)    
    cmdArr = []
    cmdArr.append(gen2AddrArr[cardNum])
    cmdArr.append(rs232Intf.SET_GEN2_CFG)
    for loop in range(rs232Intf.NUM_G2_WING_PER_BRD):
        if loadCfg:
            cmdArr.append(cfgFile.wingCfg[cardNum][loop])
        else:
            cmdArr.append(wingCfg[cardNum][loop])
    cmdArr.append(calcCrc8(cmdArr))
    cmdArr.append(rs232Intf.EOM_CMD)
    sendCmd = ''.join(cmdArr)
    ser.write(sendCmd)
    return (0)

#send color table cfg cmd
def sendColorCfgCmd(cardNum):
    global ser
    global numGen2Brd
    global gen2AddrArr
    if (cardNum >= numGen2Brd):
        return (900)    
    cmdArr = []
    cmdArr.append(gen2AddrArr[cardNum])
    cmdArr.append(rs232Intf.SET_NEO_COLOR_TBL)
    for loop in range((rs232Intf.NUM_COLOR_TBL * 3) + 1):
        if loadCfg:
            cmdArr.append(cfgFile.colorCfg[cardNum][loop])
        else:
            cmdArr.append(colorCfg[cardNum][loop])
    cmdArr.append(calcCrc8(cmdArr))
    cmdArr.append(rs232Intf.EOM_CMD)
    sendCmd = ''.join(cmdArr)
    ser.write(sendCmd)
    return (0)

#Find newest image
def findNewestImage():
    global newestVers
    # Assumes standard directory structure for OPP repository
    for file in os.listdir("../../Creator/Gen2Images"):
        if file.endswith(".cyacd"):
            fileVers = file.replace('Gen2.rev','',1).replace('.cyacd','',1)
            if (fileVers > newestVers):
                newestVers = fileVers
    if (newestVers == "0.0.0.0"):
        print "Error, could not find firmware images."
        return True
    return False

#send get version command
def sendGetVersCmd(cardNum):
    return (send4ByteDataCmd(cardNum, rs232Intf.GET_VERS_CMD))

#send serial number command
def sendGetSerNumCmd(cardNum):
    return (send4ByteDataCmd(cardNum, rs232Intf.GET_SER_NUM_CMD))

#rcv get version response
def rcvGetVersResp(cardNum):
    global ser
    global numGen2Brd
    global gen2AddrArr
    global cardVersion
    data = getSerialData();
    if (data[0] != gen2AddrArr[cardNum]):
        print "\nData = %d, expected = %d" % (ord(data[0]),ord(gen2AddrArr[cardNum]))
        print repr(data)
        return (1000)
    if (data[1] != rs232Intf.GET_VERS_CMD):
        print "\nData = %d, expected = %d" % (ord(data[1]),ord(rs232Intf.READ_GEN2_INP_CMD))
        print repr(data)
        return (1001)
    tmpData = [ data[0], data[1], data[2], data[3], data[4], data[5] ]
    crc8 = calcCrc8(tmpData)
    if (data[6] != crc8):
        print "\nBad CRC, Data = %d, expected = %d" % (ord(data[6]),crc8)
        return (1002)
    if (data[7] != rs232Intf.EOM_CMD):
        print "\nData = %d, expected = %d" % (ord(data[7]),ord(rs232Intf.EOM_CMD))
        return (1003)
    cardVersion.append(str(ord(data[2])) + "." + str(ord(data[3])) + "." + str(ord(data[4])) + "." + str(ord(data[5])))
    print "Card %d, firmware version = %s" % (cardNum, cardVersion[cardNum])
    if (cardVersion[cardNum] < "0.2.0.1"):
        print "!!! Firmware upgrades not support before version 0.2.0.1.  Exiting"
        return (1004)
    return (0)

#rcv get serial number response
def rcvGetSerNumResp(cardNum):
    global ser
    global numGen2Brd
    global gen2AddrArr
    global cardSerNum
    data = getSerialData();
    if (data[0] != gen2AddrArr[cardNum]):
        print "\nData = %d, expected = %d" % (ord(data[0]),ord(gen2AddrArr[cardNum]))
        print repr(data)
        return (1100)
    if (data[1] != rs232Intf.GET_SER_NUM_CMD):
        print "\nData = %d, expected = %d" % (ord(data[1]),ord(rs232Intf.GET_SER_NUM_CMD))
        print repr(data)
        return (1101)
    tmpData = [ data[0], data[1], data[2], data[3], data[4], data[5] ]
    crc8 = calcCrc8(tmpData)
    if (data[6] != crc8):
        print "\nBad CRC, Data = %d, expected = %d" % (ord(data[6]),crc8)
        return (1102)
    if (data[7] != rs232Intf.EOM_CMD):
        print "\nData = %d, expected = %d" % (ord(data[7]),ord(rs232Intf.EOM_CMD))
        return (1102)
    cardSerNum.append((ord(data[2]) << 24) | (ord(data[3]) << 16) | (ord(data[4]) << 8) | ord(data[5]))
    if (cardSerNum[cardNum] != 0xffffffff):
        print "Card %d, has serial num 0x%08x programmed, so it must be preserved" % (cardNum, cardSerNum[cardNum])
    return (0)

#send pass through command so card ignores serial data
#note:  No EOM command because after this command card will simply repeat data
def sendPassThruCmd(cardNum):
    global ser
    global numGen2Brd
    global gen2AddrArr
    if (cardNum >= numGen2Brd):
        return (1200)
    cmdArr = []
    cmdArr.append(gen2AddrArr[cardNum])
    cmdArr.append(rs232Intf.PASS_THRU_CMD)
    cmdArr.append(calcCrc8(cmdArr))
    sendCmd = ''.join(cmdArr)
    ser.write(sendCmd)
    return (0)

#send go boot command
#note:  No EOM command because after this command card will be in the bootloader
def sendGoBootCmd(cardNum):
    global ser
    global numGen2Brd
    global gen2AddrArr
    if (cardNum >= numGen2Brd):
        return (1300)
    cmdArr = []
    cmdArr.append(gen2AddrArr[cardNum])
    cmdArr.append(rs232Intf.GO_BOOT_CMD)
    cmdArr.append(calcCrc8(cmdArr))
    sendCmd = ''.join(cmdArr)
    ser.write(sendCmd)
    return (0)

#send re-enable pass thru cards
def sendReenablePassThruCards():
    global ser
    cmdArr = []
    for index in xrange(rs232Intf.NUM_CHARS_CLEAR_PASSTHRU):
        cmdArr.append(rs232Intf.EOM_CMD)
    sendCmd = ''.join(cmdArr)
    ser.write(sendCmd)

    # Receive all the EOM characters
    data = getSerialData();
    while (len(data) != 0):
        data = getSerialData();
    return (0)

def sendSetSerNumCmd(cardNum, data):
    global ser
    global numGen2Brd
    global gen2AddrArr
    if (cardNum >= numGen2Brd):
        return (1400)    
    cmdArr = []
    cmdArr.append(gen2AddrArr[cardNum])
    cmdArr.append(rs232Intf.SET_SER_NUM_CMD)
    cmdArr.append(chr((data >> 24) & 0xff))
    cmdArr.append(chr((data >> 16) & 0xff))
    cmdArr.append(chr((data >> 8) & 0xff))
    cmdArr.append(chr(data & 0xff))
    cmdArr.append(calcCrc8(cmdArr))
    cmdArr.append(rs232Intf.EOM_CMD)
    sendCmd = ''.join(cmdArr)
    ser.write(sendCmd)
    return (0)

def endTest(error):
    global ser
    global errMsg
    print "\nError code =", error
    ser.close()
    print "\nPress any key to close window"
    ch = getChar()
    sys.exit(error)

def test1(card):
    global hasMatrix
    global currInpData
    global matrixInpData

    print "Press 'x' or 'X' to end the test."
    count = 0
    exitReq = False
    while (not exitReq):
        sendReadInpBrdCmd(card)
        error = rcvReadInpResp(card)
        if error:
            print "\nCount = %d" % count
            endTest(error)

        if hasMatrix[card]:
            sendReadMatrixCmd(card)
            error = rcvReadMatrixResp(card)
            if error:
                print "\nCount = %d" % count
                endTest(error)

        outArr = []
        outArr.append('\r')
        for loop in range(rs232Intf.NUM_G2_INP_PER_BRD):
            if (currInpData[card] & (1 << (rs232Intf.NUM_G2_INP_PER_BRD - loop - 1))):
                outArr.append('1')
            else:
                outArr.append('0')
        if hasMatrix[card]:
            for loop in range(rs232Intf.NUM_G2_MATRIX_INP):
                index = loop/8
                offset = loop & 0x7
                if (offset == 0):
                    outArr.append(' ')
                if (matrixInpData[card][index] & (1 << offset)):
                    outArr.append('1')
                else:
                    outArr.append('0')

        writeNoCR(''.join(outArr))
        count = count + 1
        
        #Check if exit is requested, if non-windows, must hit ctl-c
        while kbHit():
            char = getAsynchChar()
            if ((char == 'x') or (char == 'X')):
                print "\nCount = %d" % count
                exitReq = True

#Main code
try:
    # for Windows-based systems
    import msvcrt # If successful, we are on Windows
    windows = True
except ImportError:
    # for POSIX-based systems (with termios & tty support)
    import tty, sys, termios, select  # raises ImportError if unsupported
    windows = False
end = False
boot = False
saveCfg = False
eraseCfg = False
loadCfg = False
upgrade = False
progSer = False
for arg in sys.argv:
  if arg.startswith('-port='):
    port = arg.replace('-port=','',1)
  elif arg.startswith('-test='):
    testNum = int(arg.replace('-test=','',1))
  elif arg.startswith('-card='):
    card = int(arg.replace('-card=','',1))
  elif arg.startswith('-ser='):
    serNum = int(arg.replace('-ser=','',1))
    progSer = True
  elif arg.startswith('-?'):
    print "python Gen2Test.py [OPTIONS]"
    print "    -?                 Options Help"
    print "    -port=portName     COM port number, defaults to COM1"
    print "    -test=testNum      test number, defaults to 0"
    print "    -card=cardNum      card number, 0-based, defaults to 0"
    print "    -ser=serNum        program serial number"
    print "    -boot              force a single board into bootloader"
    print "    -saveCfg           save a cfg on a single board."
    print "        Only 1 board can be attached.  Load configuration option must also be set."
    print "    -eraseCfg          erase a cfg on a single board."
    print "        Only 1 board can be attached.\n"
    print "    -loadCfg           configuration is read from cfgFile.py"
    print "        Only 1 board can be attached.  Uses wingCfg, solCfg, inpCfg and colorCfg\n"
    print "    -upgrade           upgrade firmware to newest version"
    print "-test=0: Send inventory and verify response 10000 times."
    print "-test=1: Read card indicated by -card param continuously.  ('x' or ctl-c exits)"
    end = True
  elif arg.startswith('-boot'):
    boot = True
  elif arg.startswith('-saveCfg'):
    saveCfg = True
  elif arg.startswith('-eraseCfg'):
    eraseCfg = True
  elif arg.startswith('-loadCfg'):
    loadCfg = True
    if arg.startswith('-loadCfg='):
      # Remove "-loadCfg=" from front, and get rid of ".py" from end if it exists
      loadFileName = arg.replace('-loadCfg=','',1).replace('.py','',1)
    else:
      loadFileName = "cfgFile"
  elif arg.startswith('-upgrade'):
    upgrade = True
    findNewestImage()

if end:
    print "\nPress any key to close window"
    ch = getChar()
    sys.exit(0)
try:
    ser=serial.Serial(port, baudrate=115200, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, timeout=.1)
except serial.SerialException:
    print "\nCould not open " + port
    print "\nPress any key to close window"
    ch = getChar()
    sys.exit(1)
print "Sending inventory cmd"
bad = False
sendInvCmd()
rcvInvResp()
for index in xrange(numGen2Brd):
    sendGetVersCmd(index)
    error = rcvGetVersResp(index)
    if error != 0:
        print "\nPress any key to close window"
        ch = getChar()
        sys.exit(1)
    sendReadWingCfgCmd(index)
    rcvReadWingCfgResp(index)

    # If upgrading, collect versions of firmware plus serial numbers
    if upgrade:
        sendGetSerNumCmd(index)
        error = rcvGetSerNumResp(index)
        if error != 0:
            print "\nPress any key to close window"
            ch = getChar()
            sys.exit(1)

if (boot):
    #Make test num invalid
    testNum = 255
    if (numGen2Brd == 1):
        sendGoBootCmd(0)
        print "Sent Go Boot command."
        time.sleep(1)
    else:
        print "Only one board should be attached"
        bad = True
elif (saveCfg):
    #Make test num invalid
    testNum = 255
    if loadCfg:
        cfgFile = __import__(loadFileName)
        print "loadFileName = %s" % loadFileName
    if (numGen2Brd == 1):
        #Save config for Gen2 board
        print "Sending wing cfg."
        sendWingCfgCmd(0)
        error = rcvEomResp()
        if error: endTest(error)
        #Check if the input table/solenoid table should be filled out
        sendSolTable = False
        sendInpTable = False
        for loop in range(rs232Intf.NUM_G2_WING_PER_BRD):
            if loadCfg:
                cfg = cfgFile.wingCfg[0][loop]
            else:
                cfg = wingCfg[0][loop]
            if (cfg == rs232Intf.WING_SOL):
                sendSolTable = True
                sendInpTable = True
            if (cfg == rs232Intf.WING_INP):
                sendInpTable = True
        if sendInpTable:
            print "Sending input cfg."
            sendInpCfgCmd(0)
            error = rcvEomResp()
            if error: endTest(error)
        else:
            print "Skipping sending input cfg."
        if sendSolTable:
            print "Sending solenoid cfg."
            sendSolCfgCmd(0)
            error = rcvEomResp()
            if error: endTest(error)
        else:
            print "Skipping sending solenoid cfg."
        if loadCfg:
            try:
                cfgFile.colorCfg
            except AttributeError:
                colorTblExists = False
            else:
                colorTblExists = True
            if colorTblExists:
                print "Sending color table cfg."
                sendColorCfgCmd(0)
                error = rcvEomResp()
                if error: endTest(error)
            else:
                print "Skipping sending color table."
        else:
            print "Sending color table cfg."
            sendColorCfgCmd(0)
            error = rcvEomResp()
            if error: endTest(error)
        print "Sending save cfg command."
        cmdArr = []
        cmdArr.append(gen2AddrArr[0])
        cmdArr.append(rs232Intf.SAVE_CFG_CMD)
        cmdArr.append(calcCrc8(cmdArr))
        sendCmd = ''.join(cmdArr)
        ser.write(sendCmd)
        print "Done save cfg command."
        time.sleep(1)
    else:
        print "Only one board should be attached"
        bad = True        
elif (eraseCfg):
    #Make test num invalid
    testNum = 255
    cmdArr = []
    if (numGen2Brd == 1):
        #Erase config for Gen2 board
        cmdArr.append(gen2AddrArr[0])
        cmdArr.append(rs232Intf.ERASE_CFG_CMD)
        cmdArr.append(calcCrc8(cmdArr))
        sendCmd = ''.join(cmdArr)
        ser.write(sendCmd)
        print "Sent erase cfg command."
        time.sleep(1)
    else:
        print "Only one board should be attached"
        bad = True
elif (upgrade):
    print "Beginning upgrade process"
    for upgCard in xrange(numGen2Brd):
        if (cardVersion[upgCard] < newestVers):
            print "Upgrading card %d" % upgCard

            # Change all other cards to pass through information
            for index in xrange(numGen2Brd):
                if (index != upgCard):
                   sendPassThruCmd(index)

            # Now force upgraded card to go into the bootloader
            sendGoBootCmd(upgCard)

            # Close serial port so firmware update can be called
            ser.close()

            # Make a system call to upgrade the firmware
            os.chdir("..\cyflash")
            cmdLine = sys.executable + " -m cyflash.__main__ --serial " + port + " --serial_baudrate 115200 ../../Creator/Gen2Images/Gen2.rev" + newestVers + ".cyacd"
            print "Running cmdLine = \"" + cmdLine + "\""
            os.system(cmdLine)
            os.chdir("..\Gen2Test")

            # reconnect to the serial port
            print "Reconnecting to COM port"
            ser=serial.Serial(port, baudrate=115200, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, timeout=.1)
            print "Re-enabling pass thru cards"
            for reenable in xrange(numGen2Brd - 1):
                sendReenablePassThruCards()

            # rerun the inventory command so all cards have addresses
            # don't rerun receive processing so cards aren't counted again
            sendInvCmd()
            rcvInvResp(False)

            # if serial number is non-zero, reprogram it
            if (cardSerNum[upgCard] != 0):
                print "Re-programming serial number"
                sendSetSerNumCmd(upgCard, cardSerNum[upgCard]) 
                rcvEomResp()
    print "Finished upgrade process"
elif (progSer):
    print "Programming serial number"
    print "serNum = %d" % serNum
    sendSetSerNumCmd(card, serNum)
    rcvEomResp()
    sendGetSerNumCmd(card)
    error = rcvGetSerNumResp(card)
    if error != 0:
        print "\nPress any key to close window"
        ch = getChar()
        sys.exit(1)

if (testNum == 0):
    for superLoop in range(10000):
        sendInvCmd()
        data = getSerialData();
        if (data[0] != rs232Intf.INV_CMD):
            print "Bad resp, index = %d, data = %d" % (0, ord(data[0]))
            bad = True
        if (data[1] != '\x20'):
            print repr(data)
            print "Bad resp, index = %d, data = %d" % (1, ord(data[1]))
            bad = True
        if (data[2] != rs232Intf.EOM_CMD):
            print repr(data)
            print "Bad resp, index = %d, data = %d" % (2, ord(data[2]))
            bad = True
        if (bad):
            break;
        print "\nSuccessful loop."
elif (testNum == 1):
    if windows:
        test1(card)
    else:
        old_settings = termios.tcgetattr(sys.stdin)
        try:
            tty.setcbreak(sys.stdin.fileno())
            test1(card)

        finally:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)

ser.close()
sys.exit(0)
