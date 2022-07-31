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
# @file:   regrCfg.py
# @author: Hugh Spahr
# @date:   07/10/2016
#
# @note:   Open Pinball Project
#          Copyright 2012-2015, Hugh Spahr
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
# This configures a processor board to be used as a regression tester for the
# firmware.  Wing 0 is Neopixel, wing 1 is solenoid, wing 2 is input, and wing 3
# is an incandescent board.
#
#===============================================================================

testVers = '00.00.01'

import rs232Intf

# Config inputs as all state inputs
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

# solenoid config
solCfg  = [ [ '\x00', '\x00', '\x00', '\x00', '\x00', '\x00', \
                '\x00', '\x00', '\x00', '\x00', '\x00', '\x00', \
                rs232Intf.CFG_SOL_USE_SWITCH, '\x30', '\x04', rs232Intf.CFG_SOL_USE_SWITCH, '\x30', '\x04', \
                rs232Intf.CFG_SOL_USE_SWITCH, '\x20', '\x00', rs232Intf.CFG_SOL_USE_SWITCH, '\x20', '\x00', \
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
