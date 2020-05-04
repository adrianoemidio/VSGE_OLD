#   This file is part of VSGBE.
#
#    VSGBE is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    VSGBE is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with VSGBE.  If not, see <https://www.gnu.org/licenses/>.

#!/usr/bin/python

#Endereço dos registros especiais na memória
#Em certos aspectos, seria melhir referenciar pelo nomes,
#porém não sei qual a melhor maneira de se definir contantes em python.. :(
P1 = 0xFF00   
SB = 0xFF01   
SC = 0xFF02   
DIV = 0xFF04   
TIMA = 0xFF05   
TMA = 0xFF06   
TAC = 0xFF07   
IF = 0xFF0F   
NR10 = 0xFF10   
NR11 = 0xFF11   
NR12 = 0xFF12   
NR13 = 0xFF13   
NR14 = 0xFF14   
NR21 = 0xFF16   
NR22 = 0xFF17   
NR23 = 0xFF18   
NR24 = 0xFF19   
NR30 = 0xFF1A   
NR31 = 0xFF1B   
NR32 = 0xFF1C   
NR33 = 0xFF1D   
NR34 = 0xFF1E   
NR41 = 0xFF20   
NR42 = 0xFF21   
NR43 = 0xFF22   
NR44 = 0xFF23   
NR50 = 0xFF24   
NR51 = 0xFF25   
NR52 = 0xFF26   
#FF30 - FF3F (Wave Pattern RAM)
LCDC = 0xFF40   
STAT = 0xFF41   
SCY = 0xFF42   
SCX = 0xFF43   
LY = 0xFF44   
LYC = 0xFF45   
DMA = 0xFF46   
BGP = 0xFF47   
OBP0 = 0xFF48   
OBP1 = 0xFF49   
WY = 0xFF4A   
WX = 0xFF4B   
IE = 0xFFFF   


