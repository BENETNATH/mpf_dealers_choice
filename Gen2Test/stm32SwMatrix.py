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
# @file:   stm32SwMatrix.py
# @author: Hugh Spahr
# @date:   12/18/2019
#
# @note:   Open Pinball Project
#          Copyright 2012-2019, Hugh Spahr
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
# This is the serial port interface file that is included for serial port
# command definitions.
#
#===============================================================================

testVers = '00.00.01'

import rs232Intf

# Config inputs as all state inputs
wingCfg = [ [ rs232Intf.WING_SOL, rs232Intf.WING_SOL, rs232Intf.WING_SW_MATRIX_OUT, rs232Intf.WING_SW_MATRIX_IN ] ]

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
solCfg  = [ [ rs232Intf.CFG_SOL_USE_MTRX_AUTO_CLR, '\x40', '\x03', rs232Intf.CFG_SOL_USE_MTRX_AUTO_CLR, '\x10', '\x23', \
                rs232Intf.CFG_SOL_USE_MTRX_AUTO_CLR, '\x18', '\x21', rs232Intf.CFG_SOL_USE_MTRX_AUTO_CLR, '\x18', '\x22', \
                rs232Intf.CFG_SOL_USE_MTRX_AUTO_CLR, '\x18', '\x20', rs232Intf.CFG_SOL_USE_MTRX_AUTO_CLR, '\x10', '\x10', \
                rs232Intf.CFG_SOL_USE_MTRX_AUTO_CLR, '\x10', '\x00', rs232Intf.CFG_SOL_USE_MTRX_AUTO_CLR, '\x20', '\x24', \
                '\x00', '\x00', '\x00', '\x00', '\x00', '\x00', \
                '\x00', '\x00', '\x00', '\x00', '\x00', '\x00', \
                '\x00', '\x00', '\x00', '\x00', '\x00', '\x00', \
                '\x00', '\x00', '\x00', '\x00', '\x00', '\x00' ] ]

