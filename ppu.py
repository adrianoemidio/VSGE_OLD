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

#Arquivo contendo apenas variáveis,
#Não colocado aqui para deixar mais "limpo"
from ioRegAddr import *

#Arquivo de exibição de video na tela
from video import Video

#Nº máx de sprites
SPRITE_NUM = 40

#TODO: Arrumar uma maneira melhor de fazer isso...
class PpuState:
    
    HBLANK = 0
    VBLANK = 1
    RENDER = 2
    OAM = 3
    
class Ppu:

    #Construtor
    def __init__(self,mem):

        #Leitura do espaço de memória
        self.mem = mem

        #Flag de modo da ppu
        self.mode_flag = PpuState.HBLANK
        
        #Contador de Linhas
        self.line = 0

        #Estáncia para o vídeo
        #Colocar o tamanho do video em variáveis
        self.video = Video(160,144)

    
    def drawnLineBG(self,line):
        
        #Verifica qual a Banco de códigos de tiles utilizado
        #TODO:Substituir o No 0x08 por máscara p/ bit 3
        if self.mem[LCDC] & 0x08:
            #Code Area Selection: 9800h-9BFFh
            code_addr = 0x9C00
        
        else:
            #Code Area Selection: 9C00h-9FFFh
            code_addr = 0x9800

        #Verifica qual a Banco de dados de tiles utilizado
        #TODO:Substituir o No 0x10 por máscara p/ bit 4
        if self.mem[LCDC] & 0x10:
            #Character Data Selection: 8000h-8FFFh
            data_addr = 0x8000
        
        else:
            #Character Data Selection: 8800h-97FFh
            data_addr = 0x8800

        #Nos de tiles que serão incrementados
        inc_tile = (line >> 3)

        #Linha dentro tile que será renderizada
        sub_linha = (line & 0x07)

        #Deslocamento horizontal e vertical
        scrollx = self.mem[SCX]
        scrolly = self.mem[SCY]

        #No do tile inicial
        start_tile = ((scrollx >> 3) + ((scrolly >> 3) << 5))

        #Deslocamento para rolagem
        des_x = (scrollx & 0x07)
        des_y = (scrolly & 0x07)

        #Conta os pixeis que foram desenhados na telas
        n_pixel = 0

        #Endereço do primeiro char code
        tile_p = code_addr + inc_tile + start_tile

        #TODO:Arrumar uma maneira mais elegante de fazer essa parte
        #Desenha a linha na tela
        while n_pixel < 159:

            #Endereço dos dados do tile
            tile_addr = self.mem[tile_p]
            #Dado da linha do tile
            tile_data = [self.mem[(tile_addr * 16) + data_addr + ((sub_linha + des_y)*2)],self.mem[(tile_addr * 16) + data_addr + ((sub_linha + des_y)*2) + 1]]

            if (n_pixel == 0) and (des_x > 0):
                #Desenha na tela
                self.video.drawnTileLine(tile_data,line,n_pixel,des_x,7)
                #Incrementa o pixel atual
                n_pixel += (8 - des_x)

            elif n_pixel > 152:

                #Desenha na tela
                self.video.drawnTileLine(tile_data,line,n_pixel,0,(des_x - 1))
                #Incrementa o pixel atual
                n_pixel += 8

            else:
                #Desenha na tela
                self.video.drawnTileLine(tile_data,line,n_pixel,0,7)
                #Incrementa o pixel atual
                n_pixel += 8

            #Incrementa o endereço dos dados do tile
            tile_p += 1




                    

    #Função que realiza o DMA
    def dma(self):

        #Verifica o endereço
        if self.mem[DMA]:
            #O endereço de tranasferência é: DMA * 0x100
            addr = self.mem[DMA] << 8 
   
            #Laço para cópia
            for x in range(0xA0):
                #Copia o dado para o endereço 0xFE00 + passo
                #TODO: Colocar alguma constante no lugar de 0xFE000
                self.mem[0xFE00+x] = self.mem[addr+x]
            
