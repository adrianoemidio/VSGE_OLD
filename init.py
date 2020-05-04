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
import argparse

def startUp(args,ram):
   
    parser = argparse.ArgumentParser('O emulador mais lento do mundo!')

    parser = argparse.ArgumentParser()
    parser.add_argument("-b", help = "Arquivo de BIOS (Opcional)")
    parser.add_argument("-r", help = "ROM a ser aberta")
    args = parser.parse_args()

    print('BIOS:', args.b)
    print('ROM:', args.r)

    bi = "/home/adriano/Projects/Python/Emu_test/bios.gb"

    #Abre o arquivo como bytes
    with open(bi, "rb") as binaryfile :
        bios = bytearray(binaryfile.read())

    #Coloca o arquivo na ram
  #  for i in len(bios):
   #     ram[i] = bios[i]

    mem = list(bios)
   
    print(mem)
    print(len(mem))

    for i in range(len(mem)):
       ram[i] = mem[i]