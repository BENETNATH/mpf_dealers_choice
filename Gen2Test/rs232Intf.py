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
# @file:   rs232Intf.py
# @author: Hugh Spahr
# @date:   12/20/2012
#
# @note:   Open Pinball Project
#          Copyright 2012-2020, Hugh Spahr
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

testVers = '00.00.04'

#Public data
GET_SER_NUM_CMD     = '\x00'
GET_PROD_ID_CMD     = '\x01'
GET_VERS_CMD        = '\x02'
SET_SER_NUM_CMD     = '\x03'
RESET_CMD           = '\x04'
GO_BOOT_CMD         = '\x05'
CFG_SOL_CMD         = '\x06'
KICK_SOL_CMD        = '\x07'
READ_GEN2_INP_CMD   = '\x08'
CFG_INP_CMD         = '\x09'
SAVE_CFG_CMD        = '\x0b'
ERASE_CFG_CMD       = '\x0c'
GET_GEN2_CFG        = '\x0d'
SET_GEN2_CFG        = '\x0e'
CHNG_NEO_CMD        = '\x0f'
CHNG_NEO_COLOR      = '\x10'
CHNG_NEO_COLOR_TBL  = '\x11'
SET_NEO_COLOR_TBL   = '\x12'
INCAND_CMD          = '\x13'
CFG_IND_SOL_CMD     = '\x14'
CFG_IND_INP_CMD     = '\x15'
SET_IND_NEO_CMD     = '\x16'
SET_SOL_INPUT_CMD   = '\x17'
PASS_THRU_CMD       = '\x18'
READ_MATRIX_INP_CMD = '\x19'
GET_INP_TIMESTAMP   = '\x1a'
SOL_KICK_PWM        = '\x1b'

INV_CMD             = '\xf0'
EOM_CMD             = '\xff'

CARD_ID_TYPE_MASK   = '\xf0'
CARD_ID_SOL_CARD    = '\x00'
CARD_ID_INP_CARD    = '\x10'
CARD_ID_GEN2_CARD   = '\x20'

MAX_NUM_GEN2_CARD   = 0x20

NUM_G2_WING_PER_BRD = 4
WING_SOL            = '\x01'
WING_INP            = '\x02'
WING_INCAND         = '\x03'
WING_SW_MATRIX_OUT  = '\x04'
WING_SW_MATRIX_IN   = '\x05'
WING_NEO            = '\x06'
WING_HI_SIDE_INCAND = '\x07'
WING_NEO_SOL        = '\x08'
WING_SPI            = '\x09'
WING_SW_MATRIX_OUT_LOW = '\x0a'
WING_LAMP_MATRIX_COL= '\x0b'
WING_LAMP_MATRIX_ROW= '\x0c'

NUM_G2_INP_PER_BRD  = 32
NUM_G2_MATRIX_INP   = 64
NUM_INP_PER_WING    = 8
CFG_BYTES_PER_INP   = 1
NUM_MATRIX_COL      = 8

CFG_INP_STATE       = '\x00'
CFG_INP_FALL_EDGE   = '\x01'
CFG_INP_RISE_EDGE   = '\x02'

NUM_G2_SOL_PER_BRD  = 16
NUM_SOL_PER_WING    = 4
CFG_BYTES_PER_SOL   = 3
INIT_KICK_OFFSET    = 1
DUTY_CYCLE_OFFSET   = 2
CFG_SOL_DISABLE     = '\x00'
CFG_SOL_USE_SWITCH  = '\x01'
CFG_SOL_AUTO_CLR    = '\x02'
CFG_SOL_ON_OFF      = '\x04'
CFG_SOL_DLY_KICK    = '\x08'
CFG_SOL_USE_MTRX_INP= '\x10'
CFG_SOL_CAN_CANCEL  = '\x20'

#Note:  Derived from above bits
CFG_SOL_ON_OFF_USE_SW = '\x05'
CFG_SOL_USE_MTRX_AUTO_CLR= '\x12'

NUM_COLOR_TBL       = 32

NUM_INCAND_PER_WING = 8
INCAND_ROT_LEFT     = '\x00'
INCAND_ROT_RIGHT    = '\x01'
INCAND_LED_ON       = '\x02'
INCAND_LED_OFF      = '\x03'
INCAND_BLINK_SLOW   = '\x04'
INCAND_BLINK_FAST   = '\x05'
INCAND_BLINK_OFF    = '\x06'
INCAND_SET_ON_OFF   = '\x07'

INCAND_SET_CMD              = '\x80'
INCAND_SET_ON               = '\x01'
INCAND_SET_BLINK_SLOW       = '\x02'
INCAND_SET_BLINK_FAST       = '\x04'

SOL_INP_CLEAR_SOL   = '\x80'

NUM_CHARS_CLEAR_PASSTHRU = 65
