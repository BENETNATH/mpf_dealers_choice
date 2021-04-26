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
# @file:   STM32card1.py
# @author: Benoit Petit-D
# @date:   18/04/2020
#
# @note:   Open Pinball Project
#          Copyright 2012-2016, Hugh Spahr
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
# TO BE DONE
#
#===============================================================================

testVers = '00.00.01'

import rs232Intf

# Config inputs as all state inputs
wingCfg = [ [ rs232Intf.WING_NEO, rs232Intf.WING_SOL, rs232Intf.WING_SOL, rs232Intf.WING_INP ] ]

# Config inputs as all state inputs
inpCfg = [ [ rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE, \
             rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE, \
             rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE, \
             rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE, \
             rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE, \
             rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE, \
             rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE, \
             rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE, rs232Intf.CFG_INP_STATE ] ]

# solenoid config
solCfg  = [ [ '\x00', '\x00', '\x00', '\x00', '\x00', '\x00', \
                '\x00', '\x00', '\x00', '\x00', '\x00', '\x00', \
                rs232Intf.CFG_SOL_ON_OFF_USE_SW, '\x00', '\x00', rs232Intf.CFG_SOL_ON_OFF_USE_SW, '\x00', '\x00', \
                rs232Intf.CFG_SOL_ON_OFF_USE_SW, '\x00', '\x00', rs232Intf.CFG_SOL_ON_OFF_USE_SW, '\x00', '\x00', \
                rs232Intf.CFG_SOL_USE_SWITCH, '\x20', '\x00', rs232Intf.CFG_SOL_USE_SWITCH, '\x20', '\x00', \
                rs232Intf.CFG_SOL_USE_SWITCH, '\x40', '\x00', '\x00', '\x00', '\x00', \
                '\x00', '\x00', '\x00', '\x00', '\x00', '\x00', \
                '\x00', '\x00', '\x00', '\x00', '\x00', '\x00' ] ]

# Config color table
#              bytesPerPxl (1 byte), numPixels (1 byte, if 0, then 256 pixels), unused (95 bytes) 
colorCfg = [ [ '\x04', '\x0A', '\xff', '\xff', '\xff', '\xff', '\xff', '\xff', '\xff', '\xff', '\xff', '\xff', \
               '\xff', '\xff', '\xff', '\xff', '\xff', '\xff', '\xff', '\xff', '\xff', '\xff', '\xff', '\xff', \
               '\xff', '\xff', '\xff', '\xff', '\xff', '\xff', '\xff', '\xff', '\xff', '\xff', '\xff', '\xff', \
               '\xff', '\xff', '\xff', '\xff', '\xff', '\xff', '\xff', '\xff', '\xff', '\xff', '\xff', '\xff', \
               '\xff', '\xff', '\xff', '\xff', '\xff', '\xff', '\xff', '\xff', '\xff', '\xff', '\xff', '\xff', \
               '\xff', '\xff', '\xff', '\xff', '\xff', '\xff', '\xff', '\xff', '\xff', '\xff', '\xff', '\xff', \
               '\xff', '\xff', '\xff', '\xff', '\xff', '\xff', '\xff', '\xff', '\xff', '\xff', '\xff', '\xff', \
               '\xff', '\xff', '\xff', '\xff', '\xff', '\xff', '\xff', '\xff', '\xff', '\xff', '\xff', '\xff', \
               '\xff', \
            ] ]