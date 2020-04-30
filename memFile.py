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

class Memory:

    

    #Tamanho de endereço do gameboy
    ADDR_SPACE = 0xFFFF

    #Construtor da Classe
    def __init__(self):
        #Inicializa a lista que representa o espaço de memória
        self.mem = [0 for addr in range(self.ADDR_SPACE)]
        print("iniciou..")

    def __setitem__(self,index,data):
        self.mem[index] = data
    
    def __getitem__(self,index):
        return self.mem[index]