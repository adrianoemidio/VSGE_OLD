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

from sdl2 import *

class Video:

    def __init__(self,width,height):

        #Variável para dizer se o sdl foi inicializado corretamente
        self.sdl_ok = 1

        #Inicializa tudo do SLD
        #TODO: Inicilaizar só a parte vídeo
        if SDL_Init(SDL_INIT_EVERYTHING) < 0:
            self.sdl_ok = 0
        
        #Inicializa a janela
        self.app_win = SDL_CreateWindow(b"VSGBE ALPHA",SDL_WINDOWPOS_UNDEFINED,SDL_WINDOWPOS_UNDEFINED,width,height,SDL_WINDOW_SHOWN)
       
        #Verifica se a janela foi criada corretamente
        if not(self.app_win):
            self.sdl_ok = 0
 
        #inicializa o renderer para janela do aplicativo
        self.frame_rend = SDL_CreateRenderer(self.app_win,-1,SDL_RENDERER_ACCELERATED)

        #Cria uma textura para ser utilizada como frame buffer
        #TODO: Remover nº mágicos do tamanho do buffer
        #self.frame_surf = SDL_CreateRGBSurface(0, 160, 144, 32, 0xff000000, 0x00ff0000, 0x0000ff00, 0x0000ff00)
        #self.frame_surf = SDL_CreateTexture(self.frame_rend,SDL_PIXELFORMAT_RGBA8888, SDL_TEXTUREACCESS_STREAMING, 160, 144 )
        self.BG_texture = SDL_CreateTexture(self.frame_rend,SDL_PIXELFORMAT_RGBA8888, SDL_TEXTUREACCESS_STATIC, 160, 144) 

        #Buffer para atualizar o backgorund
        #TODO: Remover Números mágicos
        self.BG_buff = [0x7F007F00 for pixel in range(23040)]


    def drawnTileLine(self,tile_line,line,start_pix,bit_start,bit_end):
        
        #Decodifica os tiles para formato RGBA
        line_rgba = self.decodeRGBA(tile_line,bit_start,bit_end)

        #Escreve a linha no buffer
        for i in range(0,len(line_rgba)):
            self.BG_buff[((line * 160) + start_pix + i)] = line_rgba[i]



    #TODO:Melhorar isso...
    def decodeRGBA(self,tile_line,start,end):
        #Realiza um ou entre cada bit das duas posições da matriz
        #TODO: Deixar isso mais claro...
        out = [(((tile_line[1]&(1<<bit)) << 1) | (tile_line[0]&(1<<bit))) >> bit for bit in range(start,(end+1),1)]
        
        #Converte a cor do gb para RGBA
        for i in range(0,len(out)):
            #Verde mais escuro (Preto)
            if out[i] == 0:
                out[i] = 0x0F380F00
            #Verde escuro
            elif out[i] == 1:
                out[i] = 0x30623000
            #Verde médio
            elif out[i] == 2:
                out[i] = 0x8bac0f00
            #Verde claro
            elif out[i] == 3:
                out[i] = 0x9bbc0f00

        return out