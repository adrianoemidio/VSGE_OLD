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

import sys
import init
from memFile import *
from cpu import SimpleZ80


def main(args):
    
    #define a memória
    ram = Memory()

    init.startUp(args,ram)

    #for i in range(256):
        #print(ram[i])

    #exit()

    #Instância do processador
    z80 = SimpleZ80(ram)

    while (True):
        print(hex(ram[z80.reg_file.PC]))
        z80.runInstruction()   
 
    exit()


if __name__ == "__main__":
    main(sys.argv)