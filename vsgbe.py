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
from memFile import *
from cpu import SimpleZ80


def main(args):
    
    #define a memória
    ram = Memory()

    #Instância do processador
    z80 = SimpleZ80(ram)
    
    print(ram[0])
    
    #Define a instrução a executar ADD A,25
    ins = [0xC6,25,0] 

    #Executa a instrução
    z80.execute(ins)

    ins = [0xEA,10,0]

    #Executa a instrução
    z80.execute(ins)

    #Resultado
    print(z80.reg_file.A)
    print(z80.clkElapsed)
    print(ram[10])


if __name__ == "__main__":
    main(sys.argv)