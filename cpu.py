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

from regFile import RegisterFile

#TODO: Arrumar uma maneira melhor de fazer isso...
class CpuState:
    RUN = 1
    STOP = 2
    HALT = 3

class SimpleZ80:

    #Variaveis da CPU

    #interrupção
    IE = 0

    #Estado da CPU
    cpuState = CpuState.RUN

    #Ciclos de clock desde a última instrução
    clkElapsed = 0

    #Construtor
    def __init__(self,mem):
        self.mem = mem
        self.reg_file = RegisterFile() 
        self.IE = 0
        self.IsRunnig = 0
        self.clkElapsed = 0
        self.cpuState = CpuState.RUN
    
    # CPU em funcionamento
    def run(self):
        while self.cpuState == CpuState.RUN:
            #Carrega Instrução (Fecth)
            opcode = self.mem[self.reg_file.PC],self.mem[(self.reg_file.PC + 1)],self.mem[(self.reg_file.PC + 2)]
            #Decodifica e excuta
            self.execute(opcode)

    #Roda uma instrução
    def runInstruction(self):
        #Carrega Instrução (Fecth)
        opcode = self.mem[self.reg_file.PC],self.mem[(self.reg_file.PC + 1)],self.mem[(self.reg_file.PC + 2)]
        #Decodifica e excuta
        self.execute(opcode)

    #Função que excutará os códigos passados pelo opcode[3]
    def execute(self,opcode):
        #Verifica se a instrução é do tipo com prefixo        
        if opcode[0] == 0xCB:
            self.execPre(opcode[1])
        else:
            if opcode[0] >= 0xC0:
               self.execG3(opcode)
            elif opcode[0] >= 0x80:
                self.execG2(opcode[0])
            elif opcode[0] >= 0x40:
                self.execG1(opcode[0])
            else:
                self.execG0(opcode)            



    #Opcode sem prefixo Grupo 0
    def execG0(self,opcode):
        
        #varivel temporária para indentificar o tipo de instrução
        z = opcode[0] & 0x07

        if z == 0:
            self.execG0S0(opcode)
        elif z == 1:
            self.execG0S1(opcode)
        elif z == 2:
            self.execG0S2(opcode)
        elif z == 3:
            self.execG0S3(opcode)
        elif z == 4:

            #varivel temporária para indentificar o subgrupo da instrução
            y = (opcode[0] & 0x38) >> 3

            #Zera bit N do Flag
            self.reg_file.clrFlagBit("N")

            if y == 6:
                #Executa INC (HL)
                self.mem[self.reg_file.HL] += 1
                
                #Verifica overflow
                if self.mem[self.reg_file.HL] > 0xFF:
                    self.mem[self.reg_file.HL] = 0
                    self.reg_file.setFlagBit("H")
                    self.reg_file.setFlagBit("Z")
                else:
                    self.reg_file.clrFlagBit("H")
                    self.reg_file.clrFlagBit("Z")

                #Atulaiza o contador de programa
                self.reg_file.PC += 1
            
                #Atualiza o clock
                self.clkElapsed = 12


            else:
                #Executa INC r8
                self.reg_file.writeReg8(y,(self.reg_file.readReg8(y) + 1))
                
                #Verifica overflow
                if self.reg_file.readReg8(y) > 0xFF:
                    self.reg_file.writeReg8(y,0)
                    self.reg_file.setFlagBit("H")
                    self.reg_file.setFlagBit("Z")
                else:
                    self.reg_file.clrFlagBit("H")
                    self.reg_file.clrFlagBit("Z")

                #Atulaiza o contador de programa
                self.reg_file.PC += 1
            
                #Atualiza o clock
                self.clkElapsed = 4

        elif z == 5:

            #varivel temporária para indentificar o subgrupo da instrução
            y = (opcode[0] & 0x38) >> 3

            #Seta bit N do Flag
            self.reg_file.setFlagBit("N")

            if y == 6:
                #Executa DEC (HL)
                self.mem[self.reg_file.HL] -= 1
                
                #Verifica underflow
                if self.mem[self.reg_file.HL] == 0:
                    self.reg_file.clrFlagBit("H")
                    self.reg_file.setFlagBit("Z")

                elif self.mem[self.reg_file.HL] < 0:
                    self.mem[self.reg_file.HL]  = 0xFF
                    self.reg_file.setFlagBit("H")
                    self.reg_file.clrFlagBit("Z")
                else:
                    self.reg_file.clrFlagBit("H")
                    self.reg_file.clrFlagBit("Z")

                #Atulaiza o contador de programa
                self.reg_file.PC += 1
            
                #Atualiza o clock
                self.clkElapsed = 12


            else:
                #Executa DEC r8
                self.reg_file.writeReg8(y,(self.reg_file.readReg8(y) - 1))
                
                #Verifica underflow
                if self.reg_file.readReg8(y) == 0:
                    self.reg_file.clrFlagBit("H")
                    self.reg_file.setFlagBit("Z")

                elif self.reg_file.readReg8(y) < 0:
                    self.reg_file.writeReg8(y,0xFF)
                    self.reg_file.setFlagBit("H")
                    self.reg_file.clrFlagBit("Z")
                else:
                    self.reg_file.clrFlagBit("H")
                    self.reg_file.clrFlagBit("Z")

                #Atulaiza o contador de programa
                self.reg_file.PC += 1
            
                #Atualiza o clock
                self.clkElapsed = 4
        
        elif z == 6:

            #varivel temporária para indentificar o subgrupo da instrução
            y = (opcode[0] & 0x38) >> 3

            if y == 6:
                #Executa LD (HL),d8
                self.mem[self.reg_file.HL] = opcode[1]

                #Atulaiza o contador de programa
                self.reg_file.PC += 2
            
                #Atualiza o clock
                self.clkElapsed = 12

            else:
                #Executa LD r8,d8
                self.reg_file.writeReg8(y,opcode[1])

                #Atulaiza o contador de programa
                self.reg_file.PC += 2
            
                #Atualiza o clock
                self.clkElapsed = 8

        else:
           self.execG0S7(opcode)

    #Opcode sem prefixo Grupo 1
    def execG1(self,opcode):
        #Verifca se é instrução HALT OU LD
        if opcode == 0x76:
            #execulta a instrução halt
            self.cpuState == CpuState.HALT

            #Atulaiza o contador de programa
            self.reg_file.PC += 1
          
            #Atualiza o clock
            self.clkElapsed = 4

        
        else:

            #Instrução LD 
            
            #Registro de Origem
            z = opcode & 0x07

            #Registro de destino
            y = (opcode & 0x38) >> 3
            
            #Verifica se a origem não é a memória
            if z == 6:
                #Executa LD r8,(HL) 
                self.reg_file.writeReg8(y,self.mem[self.reg_file.HL])

                #Atulaiza o contador de programa
                self.reg_file.PC += 1
            
                #Atualiza o clock
                self.clkElapsed = 8

            elif y == 6:
                #Executa LD (HL),r8 
                self.mem[self.reg_file.HL] = self.reg_file.readReg8(z)

                #Atulaiza o contador de programa
                self.reg_file.PC += 1
            
                #Atualiza o clock
                self.clkElapsed = 8

            else:
                #Executa LD r8,r8 
                self.reg_file.writeReg8(y,self.reg_file.readReg8(z))

                #Atulaiza o contador de programa
                self.reg_file.PC += 1
            
                #Atualiza o clock
                self.clkElapsed = 4
            
       
    #Opcode sem prefixo Grupo 2
    def execG2(self,opcode):
        
        #varivel temporária para indentificar o subgrupo da instrução
        y = (opcode & 0x38) >> 3

        #Registro de Origem
        z = opcode & 0x07

        #Chama a função que executa as operações lógicas e aritméticas
        self.ula(y,z)

    
    #Opcode sem prefixo Grupo 3
    def execG3(self,opcode):

        #varivel temporária para indentificar o subgrupo da instrução
        z = opcode[0] & 0x07
        y = (opcode[0] & 0x38) >> 3

        if z == 0:
            self.execG3S0(opcode)
        elif z == 1:
            self.execG3S1(opcode[0])
        elif z == 2:
            self.execG3S2(opcode)
        elif z == 3:
            self.execG3S3(opcode)
        elif z == 4:
            self.execG3S4(opcode)
        elif z == 5:
            self.execG3S5(opcode)
        elif z == 6:
            self.execG3S6(opcode)
        else:
            #Executa RST y*8
            self.mem[(self.reg_file.SP - 1)] = ((self.reg_file.PC & 0xFF00) >> 8)
            self.mem[(self.reg_file.SP - 2)] = (self.reg_file.PC & 0xFF)
            self.reg_file.SP -= 2
            self.reg_file.PC = (y*8)
          
            #Atualiza o clock
            self.clkElapsed = 16

    #Opcode com prefixo CB
    def execPre(self,opcode):
        #varivel temporária para indentificar o subgrupo da instrução
        x = (opcode & 0xC0) >> 6

        #varivel temporária para indentificar o subgrupo da instrução
        y = (opcode & 0x38) >> 3

        #varivel temporária para indentificar o subgrupo da instrução
        z = opcode & 0x07

        if x == 0:
            
            #Limpa bits do flag
            self.reg_file.clrFlagBit("H")
            self.reg_file.clrFlagBit("N")
            self.reg_file.clrFlagBit("Z")

            if y == 0:

                #Limpa o carry
                self.reg_file.clrFlagBit("C")
                
                if z == 6:
                    
                    #Verifica o bit de overflow
                    if (self.mem[self.reg_file.HL] & 0x80): self.reg_file.setFlagBit("C")

                    #Executa RLC (HL)
                    self.mem[self.reg_file.HL] = (self.mem[self.reg_file.HL] << 1) & 0xFF

                    #Copia o carry para bit 0
                    self.mem[self.reg_file.HL] |= self.reg_file.getFlagBit("C")

                    #Verifica o flag Zero
                    if self.mem[self.reg_file.HL] == 0:
                        self.reg_file.setFlagBit("Z")

                    #Atulaiza o contador de programa
                    self.reg_file.PC += 2
                
                    #Atualiza o clock
                    self.clkElapsed = 16
                
                else:
                      
                    #Verifica o bit de overflow
                    if (self.reg_file.readReg8(z) & 0x80): self.reg_file.setFlagBit("C")

                    #Executa RLC r8
                    self.reg_file.writeReg8(z,(self.reg_file.readReg8(z) << 1) & 0xFF)

                    #Copia o carry para bit 0
                    self.reg_file.writeReg8(z,(self.reg_file.readReg8(z) | self.reg_file.getFlagBit("C")))

                    #Verifica o flag Zero
                    if self.reg_file.readReg8(z) == 0:
                        self.reg_file.setFlagBit("Z")

                    #Atulaiza o contador de programa
                    self.reg_file.PC += 2
                
                    #Atualiza o clock
                    self.clkElapsed = 18

            elif y == 1:

                #Limpa o carry
                self.reg_file.clrFlagBit("C")
                
                if z == 6:
                    
                    #Verifica o bit de overflow
                    if (self.mem[self.reg_file.HL] & 0x80): self.reg_file.setFlagBit("C")

                    #Executa RRC (HL)
                    self.mem[self.reg_file.HL] = (self.mem[self.reg_file.HL] >> 1) & 0xFF

                    #Copia o carry para bit 7
                    self.mem[self.reg_file.HL] |= self.reg_file.getFlagBit("C")

                    #Verifica o flag Zero
                    if self.mem[self.reg_file.HL] == 0:
                        self.reg_file.setFlagBit("Z")

                    #Atulaiza o contador de programa
                    self.reg_file.PC += 2
                
                    #Atualiza o clock
                    self.clkElapsed = 16
                
                else:
                      
                    #Verifica o bit de overflow
                    if (self.reg_file.readReg8(z) & 0x01): self.reg_file.setFlagBit("C")

                    #Executa RRC r8
                    self.reg_file.writeReg8(z,(self.reg_file.readReg8(z) >> 1) & 0xFF)

                    #Copia o carry para bit 7
                    self.reg_file.writeReg8(z,(self.reg_file.readReg8(z) | (self.reg_file.getFlagBit("C") << 7)))

                    #Verifica o flag Zero
                    if self.reg_file.readReg8(z) == 0:
                        self.reg_file.setFlagBit("Z")
                
                    #Atulaiza o contador de programa
                    self.reg_file.PC += 1

                    #Atualiza o clock
                    self.clkElapsed = 8

            elif y == 2:
                
                if z == 6:

                    #Grava uma cópia do bit Carry do flag
                    c_temp = self.reg_file.getFlagBit("C")

                    #Limpa o carry
                    self.reg_file.clrFlagBit("C")
                    
                    #Verifica o bit de overflow
                    if (self.mem[self.reg_file.HL]& 0x80): self.reg_file.setFlagBit("C")

                    #Executa RL (HL)
                    self.mem[self.reg_file.HL] = (self.mem[self.reg_file.HL] << 1) & 0xFF

                    #Copia o carry para bit 0
                    self.mem[self.reg_file.HL] |= c_temp

                    #Verifica o flag Zero
                    if self.mem[self.reg_file.HL] == 0:
                        self.reg_file.setFlagBit("Z")

                    #Atulaiza o contador de programa
                    self.reg_file.PC += 2
                
                    #Atualiza o clock
                    self.clkElapsed = 16

                
                else:

                    #Grava uma cópia do bit Carry do flag
                    c_temp = self.reg_file.getFlagBit("C")

                    #Limpa o carry
                    self.reg_file.clrFlagBit("C")

                    #Verifica o bit de overflow
                    if (self.reg_file.readReg8(z) & 0x80): self.reg_file.setFlagBit("C")

                    #Executa RL r8
                    self.reg_file.writeReg8(z, (self.reg_file.readReg8(z) << 1) & 0xFF)

                    #Copia o carry para bit 0
                    self.reg_file.writeReg8(z, (self.reg_file.readReg8(z) | c_temp))

                    #Verifica o flag Zero
                    if self.reg_file.readReg8(z) == 0:
                        self.reg_file.setFlagBit("Z")

                    #Atulaiza o contador de programa
                    self.reg_file.PC += 2
                
                    #Atualiza o clock
                    self.clkElapsed = 8
                    


            elif y == 3:
                
                if z == 6:

                    #Grava uma cópia do bit Carry do flag
                    c_temp = self.reg_file.getFlagBit("C")

                    #Limpa o carry
                    self.reg_file.clrFlagBit("C")
                    
                    #Verifica o bit de overflow
                    if (self.mem[self.reg_file.HL]& 0x01): self.reg_file.setFlagBit("C")

                    #Executa #RR (HL)
                    self.mem[self.reg_file.HL] = (self.mem[self.reg_file.HL] >> 1) & 0xFF

                    #Copia o carry para bit 7
                    self.mem[self.reg_file.HL] |= (c_temp << 7)

                    #Verifica o flag Zero
                    if self.mem[self.reg_file.HL] == 0:
                        self.reg_file.setFlagBit("Z")
                
                    #Atualiza o clock
                    self.clkElapsed = 16

                
                else:

                    #Grava uma cópia do bit Carry do flag
                    c_temp = self.reg_file.getFlagBit("C")

                    #Limpa o carry
                    self.reg_file.clrFlagBit("C")

                    #Verifica o bit de overflow
                    if (self.reg_file.readReg8(z) & 0x01): self.reg_file.setFlagBit("C")

                    #Executa #RR r8
                    self.reg_file.writeReg8(z, (self.reg_file.readReg8(z) >> 1) & 0xFF)

                    #Copia o carry para bit 7
                    self.reg_file.writeReg8(z, (self.reg_file.readReg8(z) | (c_temp << 7)))

                    #Verifica o flag Zero
                    if self.reg_file.readReg8(z) == 0:
                        self.reg_file.setFlagBit("Z")

                    #Atulaiza o contador de programa
                    self.reg_file.PC += 2
                
                    #Atualiza o clock
                    self.clkElapsed = 8

            elif y == 4:
                
                if z == 6:

                    #Limpa o carry
                    self.reg_file.clrFlagBit("C")
                    
                    #Verifica o bit de overflow
                    if (self.mem[self.reg_file.HL]& 0x80): self.reg_file.setFlagBit("C")

                    #Executa SLA (HL)
                    self.mem[self.reg_file.HL] = (self.mem[self.reg_file.HL] << 1) & 0xFF

                    #Verifica o flag Zero
                    if self.mem[self.reg_file.HL] == 0:
                        self.reg_file.setFlagBit("Z")

                    #Atulaiza o contador de programa
                    self.reg_file.PC += 2
                
                    #Atualiza o clock
                    self.clkElapsed = 16

                
                else:

                    #Limpa o carry
                    self.reg_file.clrFlagBit("C")

                    #Verifica o bit de overflow
                    if (self.reg_file.readReg8(z) & 0x80): self.reg_file.setFlagBit("C")

                    #Executa SLA r8
                    self.reg_file.writeReg8(z, (self.reg_file.readReg8(z) << 1) & 0xFF)

                    #Verifica o flag Zero
                    if self.reg_file.readReg8(z) == 0:
                        self.reg_file.setFlagBit("Z")

                    #Atulaiza o contador de programa
                    self.reg_file.PC += 2
                
                    #Atualiza o clock
                    self.clkElapsed = 8

            elif y == 5:
                
                if z == 6:

                    #Limpa o carry
                    self.reg_file.clrFlagBit("C")
                    
                    #Verifica o bit de overflow
                    if (self.mem[self.reg_file.HL]& 0x01): self.reg_file.setFlagBit("C")

                    #Executa SRA (HL)
                    self.mem[self.reg_file.HL] = (self.mem[self.reg_file.HL] >> 1) & 0xFF

                    #Copia o bit 6 para bit 7
                    self.mem[self.reg_file.HL] |= ((self.mem[self.reg_file.HL] << 1) & 0x80)

                    #Verifica o flag Zero
                    if self.mem[self.reg_file.HL] == 0:
                        self.reg_file.setFlagBit("Z")

                    #Atulaiza o contador de programa
                    self.reg_file.PC += 2
                                    
                    #Atualiza o clock
                    self.clkElapsed = 16

                
                else:

                    #Limpa o carry
                    self.reg_file.clrFlagBit("C")

                    #Verifica o bit de overflow
                    if (self.reg_file.readReg8(z) & 0x01): self.reg_file.setFlagBit("C")

                    #Executa #SRA r8
                    self.reg_file.writeReg8(z, (self.reg_file.readReg8(z) >> 1) & 0xFF)

                    #Copia o bit 6 para bit 7
                    self.reg_file.writeReg8(z, (self.reg_file.readReg8(z) | ((self.reg_file.readReg8(z) << 1) & 0x80)))
                    
                    #Verifica o flag Zero
                    if self.reg_file.readReg8(z) == 0:
                        self.reg_file.setFlagBit("Z")

                    #Atulaiza o contador de programa
                    self.reg_file.PC += 2
                                    
                    #Atualiza o clock
                    self.clkElapsed = 8

            elif y == 6:
                
                #limpa os flags
                self.reg_file.Flags = 0


                if z == 6:
                  
                    #Variavel temporia para bits altos
                    temp_h = ((self.mem[self.reg_file.HL] & 0x0F) << 4) 

                    #Variavel temporia para bits baixo
                    temp_l = ((self.mem[self.reg_file.HL] & 0xF0) >> 4) 
    
                    #SWAP (HL)
                    self.mem[self.reg_file.HL] = (temp_h | temp_l)

                    #Verifica o flag Zero
                    if self.mem[self.reg_file.HL] == 0:
                        self.reg_file.setFlagBit("Z")

                    #Atulaiza o contador de programa
                    self.reg_file.PC += 2
                                                
                    #Atualiza o clock
                    self.clkElapsed = 8
                
                else:
                  
                    #Variavel temporia para bits altos
                    temp_h = ((self.reg_file.readReg8(z) & 0x0F) << 4) 

                    #Variavel temporia para bits baixo
                    temp_l = ((self.reg_file.readReg8(z) & 0xF0) >> 4) 
                    
                    #SWAP r8
                    self.reg_file.writeReg8(z,(temp_h | temp_l))

                    #Verifica o flag Zero
                    if self.reg_file.readReg8(z) == 0:
                        self.reg_file.setFlagBit("Z")

                    #Atulaiza o contador de programa
                    self.reg_file.PC += 2
                
                    #Atualiza o clock
                    self.clkElapsed = 8
            else:
                
                if z == 6:

                    #Limpa o carry
                    self.reg_file.clrFlagBit("C")
                    
                    #Verifica o bit de overflow
                    if (self.mem[self.reg_file.HL]& 0x01): self.reg_file.setFlagBit("C")

                    #Executa SRL (HL)
                    self.mem[self.reg_file.HL] = (self.mem[self.reg_file.HL] >> 1) & 0xFF

                    #Verifica o flag Zero
                    if self.mem[self.reg_file.HL] == 0:
                        self.reg_file.setFlagBit("Z")

                    #Atulaiza o contador de programa
                    self.reg_file.PC += 2
                
                    #Atualiza o clock
                    self.clkElapsed = 16

                
                else:

                    #Limpa o carry
                    self.reg_file.clrFlagBit("C")

                    #Verifica o bit de overflow
                    if (self.reg_file.readReg8(z) & 0x01): self.reg_file.setFlagBit("C")

                    #Executa SRL r8
                    self.reg_file.writeReg8(z, (self.reg_file.readReg8(z) >> 1) & 0xFF)

                    #Verifica o flag Zero
                    if self.reg_file.readReg8(z) == 0:
                        self.reg_file.setFlagBit("Z")

                    #Atulaiza o contador de programa
                    self.reg_file.PC += 2
                
                    #Atualiza o clock
                    self.clkElapsed = 8

        elif x == 1:
            
            #Limpa bits do flag
            self.reg_file.setFlagBit("H")
            self.reg_file.clrFlagBit("N")
            self.reg_file.clrFlagBit("Z")
                
            if z == 6:

                #Executa BIT b, (HL)
                if ((self.mem[self.reg_file.HL] & (1 << y)) >> y) == 0:
                    self.reg_file.setFlagBit("Z")
                
                #Atulaiza o contador de programa
                self.reg_file.PC += 2
                
                #Atualiza o clock
                self.clkElapsed = 16


                
            else:

                #Executa BIT b, r8
                if ((int(self.reg_file.readReg8(z)) & (1 << y)) >> y) == 0:
                    self.reg_file.setFlagBit("Z")
                
                #Atulaiza o contador de programa
                self.reg_file.PC += 2

                #Atualiza o clock
                self.clkElapsed = 8


        elif x == 2:
            
            if z == 6:

                #Executa RES b, (HL)
                self.mem[self.reg_file.HL] = (self.mem[self.reg_file.HL] & ((~(1 << y)) & 0xFF))

                #Atulaiza o contador de programa
                self.reg_file.PC += 2
                
                #Atualiza o clock
                self.clkElapsed = 16
                
            else:

                #Executa RES b, r8
                self.reg_file.clrRegBit(y,z)

                #Atulaiza o contador de programa
                self.reg_file.PC += 2
                
                #Atualiza o clock
                self.clkElapsed = 8
            
        elif x == 3:
            
            if z == 6:

                #Executa SET b, (HL)
                self.mem[self.reg_file.HL] =  ((self.mem[self.reg_file.HL] |(1 << y)) & 0xFF)

                #Atulaiza o contador de programa
                self.reg_file.PC += 2
                
                #Atualiza o clock
                self.clkElapsed = 16

                
            else:

                #Executa SET b, r8
                self.reg_file.setRegBit(y,z)

                #Atulaiza o contador de programa
                self.reg_file.PC += 2
                
                #Atualiza o clock
                self.clkElapsed = 8
            


    #Subgrupos de instruções

    #Subgrupos dentro do grupo 0
    def execG0S0(self,opcode):
        #varivel temporária para indentificar o subgrupo da instrução
        y = (opcode[0] & 0x38) >> 3

        #Verifica qual instrução executar
        if y == 0:
            #Executa NOP

            #Atulaiza o contador de programa
            self.reg_file.PC += 1

            #Atualiza o clock
            self.clkElapsed = 4

        elif y == 1:
            #Executa LD (d16), SP
            self.mem[opcode[1]] = (self.reg_file.SP & 0x00FF)
            self.mem[opcode[2]] = (self.reg_file.SP & 0xFF00)/256

            #Atulaiza o contador de programa
            self.reg_file.PC += 3

            #Atualiza o clock
            self.clkElapsed = 20

        elif y == 2:
            #Executa STOP
            self.cpuState = CpuState.STOP

            #Atulaiza o contador de programa
            self.reg_file.PC += 2

            #Atualiza o clock
            self.clkElapsed = 4
            
        elif y == 3:
            #Calcula o end. relativo
            addr = opcode[1] - 256 if opcode[1] > 127 else opcode[1]

            #Executa JR r8
            self.reg_file.PC += addr

            #Atulaiza o contador de programa
            self.reg_file.PC += 2

            #Atualiza o clock
            self.clkElapsed = 12

        elif y == 4:

            if self.reg_file.getFlagBit("Z") == 0:
                #Calcula o end. relativo
                addr = opcode[1] - 256 if opcode[1] > 127 else opcode[1]
                #Executa JR NZ,s8
                self.reg_file.PC += addr

                #Atualiza o clock
                self.clkElapsed = 12
            
            else:
                #Não ocorreu o salto

                #Atualiza o clock
                self.clkElapsed = 8
            
            #Atulaiza o contador de programa
            self.reg_file.PC += 2

        elif y == 5:

            if self.reg_file.getFlagBit("Z"):
                #Calcula o end. relativo
                addr = opcode[1] - 256 if opcode[1] > 127 else opcode[1]
                #Executa JR Z,s8
                self.reg_file.PC += addr

                #Atualiza o clock
                self.clkElapsed = 12
            
            else:
                #Não ocorreu o salto

                #Atualiza o clock
                self.clkElapsed = 8
            
            #Atulaiza o contador de programa
            self.reg_file.PC += 2
            
        elif y == 6:

            if self.reg_file.getFlagBit("C") == 0:
                #Calcula o end. relativo
                addr = opcode[1] - 256 if opcode[1] > 127 else opcode[1]
                #Executa JR NC,s8
                self.reg_file.PC += addr

                #Atualiza o clock
                self.clkElapsed = 12
            
            else:
                #Não ocorreu o salto

                #Atualiza o clock
                self.clkElapsed = 8
            
            #Atulaiza o contador de programa
            self.reg_file.PC += 2
            
        else:

            if self.reg_file.getFlagBit("C"):
                #Calcula o end. relativo
                addr = opcode[1] - 256 if opcode[1] > 127 else opcode[1]
                #Executa JR C,s8
                self.reg_file.PC += addr

                #Atualiza o clock
                self.clkElapsed = 12
            
            else:
                #Não ocorreu o salto

                #Atualiza o clock
                self.clkElapsed = 8
            
            #Atulaiza o contador de programa
            self.reg_file.PC += 2
            

    def execG0S1(self,opcode):
        #varivel temporária para indentificar o subgrupo da instrução
        q = (opcode[0] & 0x08) >> 3

        #varivel temporária para indentificar o subgrupo da instrução
        p = (opcode[0] & 0x30) >> 4

        #Seleciona a instrução
        if q == 0:
            
            if p == 0:
                #Executa LD BC,d16
                self.reg_file.C = opcode[1]
                self.reg_file.B = opcode[2]

                #Atulaiza o contador de programa
                self.reg_file.PC += 3

                #Atualiza o clock
                self.clkElapsed = 12

            elif p == 1:
                #Executa LD DE,d16
                self.reg_file.E = opcode[1]
                self.reg_file.D = opcode[2]

                #Atulaiza o contador de programa
                self.reg_file.PC += 3

                #Atualiza o clock
                self.clkElapsed = 12

            elif p == 2:
                #Executa LD HL,d16
                self.reg_file.L = opcode[1]
                self.reg_file.H = opcode[2]

                #Atulaiza o contador de programa
                self.reg_file.PC += 3

                #Atualiza o clock
                self.clkElapsed = 12

            else:
                #Executa LD SP,d16
                self.reg_file.SP = opcode[1] | (opcode[2] << 8)

                #Atulaiza o contador de programa
                self.reg_file.PC += 3

                #Atualiza o clock
                self.clkElapsed = 12

        else:
            
            #Limpa bit do Flag
            self.reg_file.clrFlagBit("N")
            self.reg_file.clrFlagBit("C")
            self.reg_file.clrFlagBit("H")

            if p == 0:
                                   
                #Verifica o half carry
                if ((self.reg_file.L + self.reg_file.C) & 0x100) == 0x100:
                    self.reg_file.setFlagBit("H")

                #Instrução: ADD HL,BC
                self.reg_file.HL += self.reg_file.BC
                           
                #Verifica se houve overflow
                if self.reg_file.HL > 65535:
                    #Faz o overflow em 16 bits
                    self.reg_file.HL -= 65536
                    #Seta o carry
                    self.reg_file.setFlagBit("C")
                
                #Atulaiza o contador de programa
                self.reg_file.PC += 1

                #Atualiza o clock
                self.clkElapsed = 8
                            
            elif p == 1:
                                   
                #Verifica o half carry
                if ((self.reg_file.L + self.reg_file.E) & 0x100) == 0x100:
                    self.reg_file.setFlagBit("H")

                #Instrução: ADD HL,DE
                self.reg_file.HL += self.reg_file.DE
               
                #Verifica se houve overflow
                if self.reg_file.HL > 65535:
                    #Faz o overflow em 16 bits
                    self.reg_file.HL -= 65536
                    #Seta o carry
                    self.reg_file.setFlagBit("C")

                #Atulaiza o contador de programa
                self.reg_file.PC += 1
                
                #Atualiza o clock
                self.clkElapsed = 8

            elif p == 2:
                                   
                #Verifica o half carry
                if ((self.reg_file.L + self.reg_file.L) & 0x100) == 0x100:
                    self.reg_file.setFlagBit("H")

                #Instrução: ADD HL,HL
                self.reg_file.HL += self.reg_file.HL
               
                #Verifica se houve overflow
                if self.reg_file.HL > 65535:
                    #Faz o overflow em 16 bits
                    self.reg_file.HL -= 65536
                    #Seta o carry
                    self.reg_file.setFlagBit("C")

                #Atulaiza o contador de programa
                self.reg_file.PC += 1

                #Atualiza o clock
                self.clkElapsed = 8
                
            else:
                                   
                #Verifica o half carry
                if ((self.reg_file.L + (self.reg_file.SP & 0x00FF)) & 0x100) == 0x100:
                    self.reg_file.setFlagBit("H")

                #Instrução: ADD HL,SP
                self.reg_file.HL += self.reg_file.SP
               
                #Verifica se houve overflow
                if self.reg_file.HL > 65535:
                    #Faz o overflow em 16 bits
                    self.reg_file.HL -= 65536
                    #Seta o carry
                    self.reg_file.setFlagBit("C")
                
                #Atulaiza o contador de programa
                self.reg_file.PC += 1
                
                #Atualiza o clock
                self.clkElapsed = 8


    def execG0S2(self,opcode):
        #varivel temporária para indentificar o subgrupo da instrução
        q = (opcode[0] & 0x08) >> 3

        #Seleciona a instrução
        if q == 0:
            #varivel temporária para indentificar o subgrupo da instrução
            p = (opcode[0] & 0x30) >> 4
  
            #Seleciona a instrução
            if p == 0:
                #Executa LD (BC), A
                self.mem[self.reg_file.BC] = self.reg_file.A

                #Atulaiza o contador de programa
                self.reg_file.PC += 1

                #Atualiza o clock
                self.clkElapsed = 8
            
            elif p == 1:
                #Executa LD (DE), A
                self.mem[self.reg_file.DE] = self.reg_file.A

                #Atulaiza o contador de programa
                self.reg_file.PC += 1

                #Atualiza o clock
                self.clkElapsed = 8
            
            elif p == 2:
                #Executa LD (HL+), A
                self.mem[self.reg_file.HL] = self.reg_file.A
                
                #Incrementa HL
                self.reg_file.HL += 1
               
                #Verifica se houve overflow
                if self.reg_file.HL > 65535:
                    #Faz o overflow em 16 bits
                    self.reg_file.HL -= 65536

                #Atulaiza o contador de programa
                self.reg_file.PC += 1
                
                #Atualiza o clock
                self.clkElapsed = 8
            else:
                #Executa LD (HL-), A
                self.mem[self.reg_file.HL] = self.reg_file.A
                
                #Incrementa HL
                self.reg_file.HL -= 1
               
                #Verifica se houve overflow
                if self.reg_file.HL < 0:
                    #Faz o overflow em 16 bits
                    self.reg_file.HL += 65536

                #Atulaiza o contador de programa
                self.reg_file.PC += 1
                
                #Atualiza o clock
                self.clkElapsed = 8
        else:
            #varivel temporária para indentificar o subgrupo da instrução
            p = (opcode[0] & 0x30) >> 4
  
            #Seleciona a instrução
            if p == 0:
                #Executa LD A,(BC)
                self.reg_file.A = self.mem[self.reg_file.BC]

                #Atulaiza o contador de programa
                self.reg_file.PC += 1

                #Atualiza o clock
                self.clkElapsed = 8
            
            elif p == 1:
                #Executa LD A,(DE)
                self.reg_file.A = self.mem[self.reg_file.DE]

                #Atulaiza o contador de programa
                self.reg_file.PC += 1

                #Atualiza o clock
                self.clkElapsed = 8
            
            elif p == 2:
                #Executa LD A,(HL+)
                self.reg_file.A = self.mem[self.reg_file.HL]
                
                #Incrementa HL
                self.reg_file.HL += 1
               
                #Verifica se houve overflow
                if self.reg_file.HL > 65535:
                    #Faz o overflow em 16 bits
                    self.reg_file.HL -= 65536

                #Atulaiza o contador de programa
                self.reg_file.PC += 1

                #Atualiza o clock
                self.clkElapsed = 8

            else:
                #Executa LD A,(HL-)
                self.reg_file.A = self.mem[self.reg_file.HL]
                
                #Decrementa HL
                self.reg_file.HL -= 1
               
                #Verifica se houve overflow
                if self.reg_file.HL < 0:
                    #Faz o overflow em 16 bits
                    self.reg_file.HL += 65536

                #Atulaiza o contador de programa
                self.reg_file.PC += 1
                
                #Atualiza o clock
                self.clkElapsed = 8

    def execG0S3(self,opcode):
        #varivel temporária para indentificar o subgrupo da instrução
        q = (opcode & 0x08) >> 3

        #Seleciona a instrução
        if q == 0:
            #varivel temporária para indentificar o subgrupo da instrução
            p = (opcode[0] & 0x30) >> 4

            if p == 0:    
                #Instrução: INC BC
                self.reg_file.BC += 1
               
                #Verifica se houve overflow
                if self.reg_file.BC > 65536:
                    #Faz o overflow em 16 bits
                    self.reg_file.BC -= 65536

                #Atulaiza o contador de programa
                self.reg_file.PC += 1
                
                #Atualiza o clock
                self.clkElapsed = 8

            elif p == 1:
                #Instrução: INC DE
                self.reg_file.DE += 1
               
                #Verifica se houve overflow
                if self.reg_file.DE > 65536:
                    #Faz o overflow em 16 bits
                    self.reg_file.DE -= 65536

                #Atulaiza o contador de programa
                self.reg_file.PC += 1
                
                #Atualiza o clock
                self.clkElapsed = 8
            
            elif p == 2:
                #nstrução: INC HL
                self.reg_file.HL += 1
               
                #Verifica se houve overflow
                if self.reg_file.HL > 65536:
                    #Faz o overflow em 16 bits
                    self.reg_file.HL -= 65536

                #Atulaiza o contador de programa
                self.reg_file.PC += 1 
                
                #Atualiza o clock
                self.clkElapsed = 8
            
            else:
                #nstrução: INC SP
                self.reg_file.SP += 1
               
                #Verifica se houve overflow
                if self.reg_file.SP > 65536:
                    #Faz o overflow em 16 bits
                    self.reg_file.SP -= 65536

                #Atulaiza o contador de programa
                self.reg_file.PC += 1
                
                #Atualiza o clock
                self.clkElapsed = 8
           
        else:
            #varivel temporária para indentificar o subgrupo da instrução
            p = (opcode[0] & 0x30) >> 4

            if p == 0:    
                #Instrução: DEC BC
                self.reg_file.BC -= 1
               
                #Verifica se houve overflow
                if self.reg_file.BC < 0:
                    #Faz o overflow em 16 bits
                    self.reg_file.BC += 65536

                #Atulaiza o contador de programa
                self.reg_file.PC += 1
                
                #Atualiza o clock
                self.clkElapsed = 8

            elif p == 1:
                #Instrução: DEC DE
                self.reg_file.DE -= 1
               
                #Verifica se houve overflow
                if self.reg_file.DE < 0:
                    #Faz o overflow em 16 bits
                    self.reg_file.DE += 65536

                #Atulaiza o contador de programa
                self.reg_file.PC += 1

                #Atualiza o clock
                self.clkElapsed = 8
            
            elif p == 2:
                #nstrução: DEC HL
                self.reg_file.HL -= 1
               
                #Verifica se houve overflow
                if self.reg_file.HL < 0:
                    #Faz o overflow em 16 bits
                    self.reg_file.HL += 65536

                #Atulaiza o contador de programa
                self.reg_file.PC += 1

                #Atualiza o clock
                self.clkElapsed = 8

            else:
                #nstrução: DEC SP
                self.reg_file.SP -= 1
               
                #Verifica se houve overflow
                if self.reg_file.SP < 0:
                    #Faz o overflow em 16 bits
                    self.reg_file.SP += 65536

                #Atulaiza o contador de programa
                self.reg_file.PC += 1
                
                #Atualiza o clock
                self.clkElapsed = 8       


    def execG0S7(self,opcode):
        
        if opcode == 0x07:
            #Limpa o Flags
            self.reg_file.Flags = 0

            #Verifica o bit de overflow
            if (self.reg_file.A & 0x80): self.reg_file.setFlagBit("C")

            #Executa RLCA
            self.reg_file.A = (self.reg_file.A << 1) & 0xFF

            #Copia o carry para bit 0
            self.reg_file.A |= self.reg_file.getFlagBit("C")

            #Atulaiza o contador de programa
            self.reg_file.PC += 1

            #Atualiza o clock
            self.clkElapsed = 4

        elif opcode == 0x0F:
            #Limpa o Flags
            self.reg_file.Flags = 0

            #Verifica o bit de overflow
            if (self.reg_file.A & 0x01): self.reg_file.setFlagBit("C")

            #Executa RRCA
            self.reg_file.A = (self.reg_file.A >> 1) & 0xFF

            #Copia o carry para bit 7
            self.reg_file.A |= (self.reg_file.getFlagBit("C") << 7)

            #Atulaiza o contador de programa
            self.reg_file.PC += 1

            #Atualiza o clock
            self.clkElapsed = 4
            
        elif opcode == 0x17:

            #Grava uma cópia do bit Carry do flag
            c_temp = self.reg_file.getFlagBit("C")

            #Limpa os Flags
            self.reg_file.Flags = 0

            #Verifica o bit de overflow
            if (self.reg_file.A & 0x80): self.reg_file.setFlagBit("C")

            #Executa RLA
            self.reg_file.A = (self.reg_file.A << 1) & 0xFF

            #Copia o carry para bit 0
            self.reg_file.A |= c_temp

            #Atulaiza o contador de programa
            self.reg_file.PC += 1

            #Atualiza o clock
            self.clkElapsed = 8
            
        elif opcode == 0x1F:

            #Grava uma cópia do bit Carry do flag
            c_temp = self.reg_file.getFlagBit("C")

            #Limpa os Flags
            self.reg_file.Flags = 0

            #Verifica o bit de overflow
            if (self.reg_file.A & 0x01): self.reg_file.setFlagBit("C")

            #Executa RRA
            self.reg_file.A = (self.reg_file.A >> 1) & 0xFF

            #Copia o carry para bit 7
            self.reg_file.A |= (c_temp << 7)

            #Atulaiza o contador de programa
            self.reg_file.PC += 1

            #Atualiza o clock
            self.clkElapsed = 4
            
        elif opcode == 0x27:

            #Executa DAA
            
            #divide o registro em parte alta e baixa
            al = self.reg_file.A & 0x0F
            ah = (self.reg_file.A & 0xF0)/16

            #Guarda o valor antigo das flags C e H
            c_old = self.reg_file.getFlagBit("C")
            h_old = self.reg_file.getFlagBit("H")

            #limpa os flags
            self.reg_file.clrFlagBit("C")
            self.reg_file.clrFlagBit("H")
            self.reg_file.clrFlagBit("Z")

            #Verifica a operação anterior
            if self.reg_file.getFlagBit("N"):
                
                #Verifica a parte baixa
                if (h_old or al > 9):
                    self.reg_file.A += 0x06

                #Verifica a parte alta
                if (c_old or ah > 9 or (ah == 9 and al > 9)):
                    self.reg_file.A += 0x60
                    self.reg_file.setFlagBit("C")
            
            else:

                #Verifica a parte baixa                                   
                if (h_old and al > 5 ):
                    self.reg_file.A = ((self.reg_file.A - 0x06) & 0xFF)
                
                #Verifica a parte alta
                if c_old and (ah > 6 or (h_old and ah > 5)):
                    self.reg_file.A = ((self.reg_file.A - 0x60) & 0xFF)
                    self.reg_file.setFlagBit("C")
                
            if self.reg_file.A == 0:
                self.reg_file.setFlagBit("H")
            
            #Atulaiza o contador de programa
            self.reg_file.PC += 1
        
            #Atualiza o clock
            self.clkElapsed = 4
                
              
        elif opcode == 0x2F:
 
            #Seta os flags
            self.reg_file.setFlagBit("N")
            self.reg_file.setFlagBit("H")

            #Executa CPL
            self.reg_file.A = ((~self.reg_file.A) & 0xFF)

            #Atulaiza o contador de programa
            self.reg_file.PC += 1

            #Atualiza o clock
            self.clkElapsed = 4
                
        elif opcode == 0x37:
            #Executa SCF
            self.reg_file.setFlagBit("C")
            self.reg_file.clrFlagBit("H")
            self.reg_file.clrFlagBit("N")

            #Atulaiza o contador de programa
            self.reg_file.PC += 1

            #Atualiza o clock
            self.clkElapsed = 4

        elif opcode == 0x3F:
            #Executa CCF
            self.reg_file.clrFlagBit("H")
            self.reg_file.clrFlagBit("N")

            if self.reg_file.getFlagBit("C"):
                self.reg_file.clrFlagBit("C")
            else:
                self.reg_file.setFlagBit("C")
            
            #Atulaiza o contador de programa
            self.reg_file.PC += 1
            
            #Atualiza o clock
            self.clkElapsed = 4

    #Subgrupos dentro do grupo 3
    def execG3S0(self,opcode):
        
        #varivel temporária para indentificar o subgrupo da instrução
        y = (opcode[0] & 0x38) >> 3

        #Verifica qual instrução executar
        if y  == 7:

            #Limpa os flags
            self.reg_file.Flags = 0x00

            #Calcula o end. relativo
            e = opcode[1] - 256 if opcode[1] > 127 else opcode[1]

            #Verifica o half carry
            if ((self.reg_file.SP + e) & 0x100) == 0x100:
                self.reg_file.setFlagBit("H")

            #Executa LD HL, SP+ d
            self.reg_file.HL = self.reg_file.SP + e
                            
            #Verifica se houve overflow
            if self.reg_file.HL > 65535:
                #Faz o overflow em 16 bits
                self.reg_file.HL -= 65536
                #Seta o carry
                self.reg_file.setFlagBit("C")
            
            #Atulaiza o contador de programa
            self.reg_file.PC += 2
            
            #Atualiza o clock
            self.clkElapsed = 12

        elif y == 6:

            #Executa LD A, (0xFF00 + n)
            self.reg_file.A =  self.mem[((opcode[1] + 0xFF00) & 0xFFFF)]

            #Atulaiza o contador de programa
            self.reg_file.PC += 2

            #Atualiza o clock
            self.clkElapsed = 12

        elif y == 5:

            #Limpa os flags
            self.reg_file.Flags = 0x00

            #Verifica o half carry
            if ((self.reg_file.SP + opcode[1]) & 0x100) == 0x100:
                self.reg_file.setFlagBit("H")

            #Executa ADD SP, d
            self.reg_file.SP +=  opcode[1]

            #Verifica se houve overflow
            if self.reg_file.SP > 65535:
                #Faz o overflow em 16 bits
                self.reg_file.SP -= 65536
                #Seta o carry
                self.reg_file.setFlagBit("C")

            #Atulaiza o contador de programa
            self.reg_file.PC += 2

            #Atualiza o clock
            self.clkElapsed = 16

        elif y == 4:

            #Executa LD (0xFF00 + nn), A
            self.mem[((0xFF00 + opcode[1]) & 0xFFFF)] = self.reg_file.A

            #Atulaiza o contador de programa
            self.reg_file.PC += 2

            #Atualiza o clock
            self.clkElapsed = 12

        elif y == 3:
            #Executa RET C
            if self.reg_file.getFlagBit("C"):
                self.reg_file.PC = (((self.mem[self.reg_file.SP] << 8) | self.mem[self.reg_file.SP]) & 0xFFFF)
                self.reg_file.SP += 2
                
                #Atualiza o clock
                self.clkElapsed = 20

            else:
                #Não retorna da Subrotina

                #Atualiza o clock
                self.clkElapsed = 8

                #Atulaiza o contador de programa
                self.reg_file.PC += 1

        elif y == 2:
            #Executa RET NC
            if self.reg_file.getFlagBit("C") == 0:
                self.reg_file.PC = (((self.mem[self.reg_file.SP] << 8) | self.mem[self.reg_file.SP]) & 0xFFFF)
                self.reg_file.SP += 2

                #Atualiza o clock
                self.clkElapsed = 20
            else:
                #Não retorna da Subrotina

                #Atualiza o clock
                self.clkElapsed = 8

                #Atulaiza o contador de programa
                self.reg_file.PC += 1

        elif y == 1:
            #Executa RET Z
            if self.reg_file.getFlagBit("Z"):
                self.reg_file.PC = (((self.mem[self.reg_file.SP] << 8) | self.mem[self.reg_file.SP]) & 0xFFFF)
                self.reg_file.SP += 2

                #Atualiza o clock
                self.clkElapsed = 20
            else:
                #Não retorna da Subrotina

                #Atualiza o clock
                self.clkElapsed = 8

                #Atulaiza o contador de programa
                self.reg_file.PC += 1

        else:
            #Executa RET NZ
            if self.reg_file.getFlagBit("Z") == 0:
                self.reg_file.PC = (((self.mem[self.reg_file.SP] << 8) | self.mem[self.reg_file.SP]) & 0xFFFF)
                self.reg_file.SP += 2

                #Atualiza o clock
                self.clkElapsed = 20
            else:
                #Não retorna da Subrotina

                #Atualiza o clock
                self.clkElapsed = 8

                #Atulaiza o contador de programa
                self.reg_file.PC += 1


    def execG3S1(self,opcode):
        
        #varivel temporária para indentificar o subgrupo da instrução
        q = (opcode & 0x08) >> 3

        #varivel temporária para indentificar o subgrupo da instrução
        p = (opcode & 0x30) >> 4

        #Seleciona a instrução
        if q == 0:
            
            #Seleciona a instrução
            if p == 0:
                #Executa POP BC
                self.reg_file.C = self.mem[self.reg_file.SP]
                self.reg_file.B = self.mem[(self.reg_file.SP + 1)]
               
                #Incrementa a pilha
                self.reg_file.SP += 2

                #Atulaiza o contador de programa
                self.reg_file.PC += 1

                #Atualiza o clock
                self.clkElapsed = 12


            elif p == 1:
                #Executa POP DE
                self.reg_file.D = self.mem[self.reg_file.SP]
                self.reg_file.E = self.mem[(self.reg_file.SP + 1)]
               
                #Incrementa a pilha
                self.reg_file.SP += 2

                #Atulaiza o contador de programa
                self.reg_file.PC += 1

                #Atualiza o clock
                self.clkElapsed = 12

            elif p == 2:
                #Executa POP HL
                self.reg_file.L = self.mem[self.reg_file.SP]
                self.reg_file.H = self.mem[(self.reg_file.SP + 1)]
               
                #Incrementa a pilha
                self.reg_file.SP += 2

                #Atulaiza o contador de programa
                self.reg_file.PC += 1

                #Atualiza o clock
                self.clkElapsed = 12

            else:
                #Executa POP AF
                self.reg_file.F = (self.mem[self.reg_file.SP] & 0xF0)
                self.reg_file.A = self.mem[(self.reg_file.SP + 1)]
               
                #Incrementa a pilha
                self.reg_file.SP += 2

                #Atulaiza o contador de programa
                self.reg_file.PC += 1

                #Atualiza o clock
                self.clkElapsed = 12

        else:
 
            #Seleciona a instrução
            if p == 0:

                #Executa RET
                self.reg_file.PC = (((self.mem[self.reg_file.SP] << 8 ) | self.mem[self.reg_file.SP]) & 0xFFFF)
                self.reg_file.SP += 2

                #Atualiza o clock
                self.clkElapsed = 16

            elif p == 1:

                #Executa RETI
                self.reg_file.PC = (((self.mem[self.reg_file.SP] << 8) | self.mem[self.reg_file.SP]) & 0xFFFF)
                self.reg_file.SP += 2

                #Atualiza o clock
                self.clkElapsed = 16

            elif p == 2:
                
                #Executa JP HL
                self.reg_file.PC = self.reg_file.HL

                #Atualiza o clock
                self.clkElapsed = 4

            else:
                #Executa LD SP, HL
                self.reg_file.SP = self.reg_file.HL

                #Atulaiza o contador de programa
                self.reg_file.PC += 1

                #Atualiza o clock
                self.clkElapsed = 8


    def execG3S2(self,opcode):
        #varivel temporária para indentificar o tipo de instrução
        y = (opcode[0] & 0x38) >> 3

        #Verifica qual instrução executar
        if y  == 7:

            #Executa LD A, (nn)
            self.reg_file.A = self.mem[((opcode[2] << 8 ) | self.mem[opcode[1]] & 0xFFFF)]

            #Atulaiza o contador de programa
            self.reg_file.PC += 3

            #Atualiza o clock
            self.clkElapsed = 16

        elif y == 6:

            #Executa LD A, (0xFF00+C)
            self.reg_file.A = self.mem[(0xFF00 + self.reg_file.C)]

            #Atulaiza o contador de programa
            self.reg_file.PC += 2

            #Atualiza o clock
            self.clkElapsed = 8
  
        elif y == 5:

            #Executa LD (nn), A
            self.mem[(((opcode[2] << 8) | opcode[1]) & 0xFFFF)] = self.reg_file.A

            #Atulaiza o contador de programa
            self.reg_file.PC += 3
            
            #Atualiza o clock
            self.clkElapsed = 16

        elif y == 4:

            #Executa LD (0xFF00+C), A
            self.mem[(0xFF00 + self.reg_file.C)] = self.reg_file.A

            #Atulaiza o contador de programa
            self.reg_file.PC += 1

            #Atualiza o clock
            self.clkElapsed = 8

        elif y == 3:

            #Executa JP C,a16
            if self.reg_file.getFlagBit("C"):
                self.reg_file.PC = (((opcode[2] << 8) | opcode[1]) & 0xFFFF)
                
                #Atualiza o clock
                self.clkElapsed = 16
            
            else:
                #Não efetua o salto

                #Atualiza o clock
                self.clkElapsed = 12

                #Atulaiza o contador de programa
                self.reg_file.PC += 3

        elif y == 2:

            #Executa JP NC,a16
            if self.reg_file.getFlagBit("C") == 0:
                self.reg_file.PC = (((opcode[2] << 8) | opcode[1]) & 0xFFFF)

                #Atualiza o clock
                self.clkElapsed = 16
            
            else:
                #Não efetua o salto

                #Atualiza o clock
                self.clkElapsed = 12

                #Atulaiza o contador de programa
                self.reg_file.PC += 3

        elif y == 1:

            #Executa JP Z,a16
            if self.reg_file.getFlagBit("Z"):
                self.reg_file.PC = (((opcode[2] << 8) | opcode[1]) & 0xFFFF)

                #Atualiza o clock
                self.clkElapsed = 16
            
            else:
                #Não efetua o salto

                #Atualiza o clock
                self.clkElapsed = 12
                
                #Atulaiza o contador de programa
                self.reg_file.PC += 3

        else:

            #Executa JP NZ,a16
            if self.reg_file.getFlagBit("Z") == 0:
                self.reg_file.PC = (((opcode[2] << 8) | opcode[1]) & 0xFFFF)

                #Atualiza o clock
                self.clkElapsed = 16
            
            else:
                #Não efetua o salto

                #Atualiza o clock
                self.clkElapsed = 12
                
                #Atulaiza o contador de programa
                self.reg_file.PC += 3


    def execG3S3(self,opcode):
        #varivel temporária para indentificar o tipo de instrução
        y = (opcode & 0x38) >> 3

        #Verifica qual instrução executar
        if y  == 7:

            #Executa EI
            self.IE = 1

            #Atulaiza o contador de programa
            self.reg_file.PC += 1

            #Atualiza o clock
            self.clkElapsed = 12
            
        elif y == 6:

            #Executa DI
            self.IE = 0

            #Atulaiza o contador de programa
            self.reg_file.PC += 1

            #Atualiza o clock
            self.clkElapsed = 12

        elif y == 0:

            #Executa JP nn
            self.reg_file.PC = (((opcode[2] << 8) | opcode[1]) & 0xFFFF)

            #Atualiza o clock
            self.clkElapsed = 16


    def execG3S4(self,opcode):
        #varivel temporária para indentificar o tipo de instrução
        y = (opcode[0] & 0x38) >> 3

        #Verifica qual instrução executar
        if y == 0:

            #Atulaiza o contador de programa
            self.reg_file.PC += 3

            #CALL NZ,a16
            if self.reg_file.getFlagBit("Z") == 0:
                self.mem[(self.reg_file.SP - 1)] = ((self.reg_file.PC & 0xFF00) >> 8)
                self.mem[(self.reg_file.SP - 2)] = (self.reg_file.PC & 0xFF)
                self.reg_file.SP -= 2
                self.reg_file.PC = (((opcode[2] << 8) | opcode[1]) & 0xFFFF)

                #Atualiza o clock
                self.clkElapsed = 24
            
            else:
                #Não efetua o chamada de subrotina

                #Atualiza o clock
                self.clkElapsed = 12
                

        elif y == 1:

            #Atulaiza o contador de programa
            self.reg_file.PC += 3

            #CALL Z,a16
            if self.reg_file.getFlagBit("Z"):
                self.mem[(self.reg_file.SP - 1)] = ((self.reg_file.PC & 0xFF00) >> 8)
                self.mem[(self.reg_file.SP - 2)] = (self.reg_file.PC & 0xFF)
                self.reg_file.SP -= 2
                self.reg_file.PC = (((opcode[2] << 8) | opcode[1]) & 0xFFFF)

                #Atualiza o clock
                self.clkElapsed = 24
            
            else:
                #Não efetua o chamada de subrotina

                #Atualiza o clock
                self.clkElapsed = 12

        elif y == 2:

            #Atulaiza o contador de programa
            self.reg_file.PC += 3

            #CALL NC,a16
            if self.reg_file.getFlagBit("C") == 0:
                self.mem[(self.reg_file.SP - 1)] = ((self.reg_file.PC & 0xFF00) >> 8)
                self.mem[(self.reg_file.SP - 2)] = (self.reg_file.PC & 0xFF)
                self.reg_file.SP -= 2
                self.reg_file.PC = (((opcode[2] << 8) | opcode[1]) & 0xFFFF)

                #Atualiza o clock
                self.clkElapsed = 24
           
            else:
                #Não efetua o chamada de subrotina

                #Atualiza o clock
                self.clkElapsed = 12


        elif y == 3:

            #Atulaiza o contador de programa
            self.reg_file.PC += 3

            #CALL C,a16
            if self.reg_file.getFlagBit("C"):
                self.mem[(self.reg_file.SP - 1)] = ((self.reg_file.PC & 0xFF00) >> 8)
                self.mem[(self.reg_file.SP - 2)] = (self.reg_file.PC & 0xFF)
                self.reg_file.SP -= 2
                self.reg_file.PC = (((opcode[2] << 8) | opcode[1]) & 0xFFFF)

                #Atualiza o clock
                self.clkElapsed = 24
            
            else:
                #Não efetua o chamada de subrotina

                #Atualiza o clock
                self.clkElapsed = 12

    def execG3S5(self,opcode):
        #varivel temporária para indentificar o subgrupo da instrução
        q = (opcode[0] & 0x08) >> 3
        #varivel temporária para indentificar o subgrupo da instrução
        p = (opcode[0] & 0x30) >> 4

        #Seleciona a instrução
        if q == 0:
            
            #Seleciona a instrução
            if p == 0:
                #Executa PUSH BC
                self.mem[(self.reg_file.SP - 1)] = ((self.reg_file.BC & 0xFF00) >> 8)
                self.mem[(self.reg_file.SP - 2)] = (self.reg_file.BC & 0xFF)
                self.reg_file.SP -= 2

                #Atulaiza o contador de programa
                self.reg_file.PC += 1

                #Atualiza o clock
                self.clkElapsed = 16

            elif p == 1:
                #Executa PUSH DE
                self.mem[(self.reg_file.SP - 1)] = ((self.reg_file.DE & 0xFF00) >> 8)
                self.mem[(self.reg_file.SP - 2)] = (self.reg_file.DE & 0xFF)
                self.reg_file.SP -= 2

                #Atualiza o clock
                self.clkElapsed = 16

            elif p == 2:
                #Executa PUSH HL
                self.mem[(self.reg_file.SP - 1)] = ((self.reg_file.HL & 0xFF00) >> 8)
                self.mem[(self.reg_file.SP - 2)] = (self.reg_file.HL & 0xFF)
                self.reg_file.SP -= 2

                #Atulaiza o contador de programa
                self.reg_file.PC += 1

                #Atualiza o clock
                self.clkElapsed = 16

            elif p == 3:
                #Executa PUSH AF
                self.mem[(self.reg_file.SP - 1)] = ((self.reg_file.AF & 0xFF00) >> 8)
                self.mem[(self.reg_file.SP - 2)] = (self.reg_file.AF & 0xFF)
                self.reg_file.SP -= 2

                #Atulaiza o contador de programa
                self.reg_file.PC += 1

                #Atualiza o clock
                self.clkElapsed = 16

        else:
            
            #Atulaiza o contador de programa
            self.reg_file.PC += 3

            #Seleciona a instrução
            if p == 0:
                #Executa CALL nn
                self.mem[(self.reg_file.SP - 1)] = ((self.reg_file.PC & 0xFF00) >> 8)
                self.mem[(self.reg_file.SP - 2)] = (self.reg_file.PC & 0xFF)
                self.reg_file.SP -= 2
                self.reg_file.PC = (((self.mem[opcode[2]] << 8) | self.mem[opcode[1]]) & 0xFFFF)

                #Atualiza o clock
                self.clkElapsed = 24


    def execG3S6(self,opcode):

        if opcode[0] == 0xC6:
            #Executa ADD A,d8

            #Limpa os flags
            self.reg_file.Flags = 0

            #Verifica o half carry
            if (((self.reg_file.A & 0xf) + (opcode[1] & 0xf)) & 0x10) == 0x10:
                self.reg_file.setFlagBit("H")

            #Instrução: ADD A,d8
            self.reg_file.A += opcode[1]

            
            #Verifica se houve overflow
            if self.reg_file.A > 255:
                #Faz o overflow em 8 bits
                self.reg_file.A -= 256
                #Seta o carry
                self.reg_file.setFlagBit("C")

            #Verifica se o resulatdo foi zero
            if self.reg_file.A == 0:
                self.reg_file.setFlagBit("Z")

            #Atulaiza o contador de programa
            self.reg_file.PC += 2

            #Atualiza o clock
            self.clkElapsed = 8


        elif opcode[0] == 0xCE:
            #Executa ADC A,d8

            #Reseta os flags
            self.reg_file.clrFlagBit("Z")
            self.reg_file.clrFlagBit("H")
            self.reg_file.clrFlagBit("N") 

            #Verifica o half carry
            if ((((self.reg_file.A + self.reg_file.getFlagBit("C")) & 0xf) + (opcode[1] & 0xf)) & 0x10) == 0x10:
                self.reg_file.setFlagBit("H")

            #Instrução: ADC A,d8
                self.reg_file.A += (opcode[1] + self.reg_file.getFlagBit("C"))

            
            #Verifica se houve overflow
            if self.reg_file.A > 255:
                #Faz o overflow em 8 bits
                self.reg_file.A -= 256
                #Seta o carry
                self.reg_file.setFlagBit("C")
            else:
                self.reg_file.clrFlagBit("C") 

            #Verifica se o resulatdo foi zero
            if self.reg_file.A == 0:
                self.reg_file.setFlagBit("Z")


            #Atulaiza o contador de programa
            self.reg_file.PC += 2
            
            #Atualiza o clock
            self.clkElapsed = 8
                
        elif opcode[0] == 0xD6:
            #Executa SUB A, d8

            #Limpa os Flags
            self.reg_file.Flags = 0

            #Verifica o half carry
            if (((self.reg_file.A & 0xf) - (opcode[1] & 0xf)) < 0):
                 self.reg_file.setFlagBit("H")

            #Instrução: SUB A, d8
            self.reg_file.A -= opcode[1]

            
            #Verifica se houve borrow
            if self.reg_file.A < 0:
                #Faz o overflow em 8 bits
                self.reg_file.A += 256
                #Seta o carry
                self.reg_file.setFlagBit("C")

            #Verifica se o resulatdo foi zero
            if self.reg_file.A == 0:
                self.reg_file.setFlagBit("Z")

            #Atulaiza o contador de programa
            self.reg_file.PC += 2

            #Atualiza o clock
            self.clkElapsed = 8


        elif opcode[0] == 0xDE:
            #Executa SBC A,d8

            #Reseta os flags
            self.reg_file.clrFlagBit("Z")
            self.reg_file.clrFlagBit("H")
            self.reg_file.setFlagBit("N")

            #Verifica o half carry
            if ((((self.reg_file.A - self.reg_file.getFlagBit("C") ) & 0xf) - (opcode[1] & 0xf)) < 0):
                self.reg_file.setFlagBit("H")

            #Instrução: SBC A,r8  Opcode 0x98 ~ 0x9F
            self.reg_file.A -= (opcode[1] + self.reg_file.getFlagBit("C"))

            
            #Verifica se houve overflow
            if self.reg_file.A < 0:
                #Faz o overflow em 8 bits
                self.reg_file.A += 256
                #Seta o carry
                self.reg_file.setFlagBit("C")
            else:
                self.reg_file.clrFlagBit("C") 

            #Verifica se o resulatdo foi zero
            if self.reg_file.A == 0:
                self.reg_file.setFlagBit("Z")

            #Atulaiza o contador de programa
            self.reg_file.PC += 1

            #Atualiza o clock
            self.clkElapsed = 8

        elif opcode[0] == 0xE6:
            #Executa AND A,d8

            #Reseta os flags
            self.reg_file.clrFlagBit("Z")
            self.reg_file.setFlagBit("H")
            self.reg_file.clrFlagBit("N")
            self.reg_file.clrFlagBit("C")             

            #Instrução: AND A,d8
            self.reg_file.A &= opcode[1]

            #Verifica se o resulatdo foi zero
            if self.reg_file.A == 0:
                self.reg_file.setFlagBit("Z")

            #Atulaiza o contador de programa
            self.reg_file.PC += 1
            
            #Atualiza o clock
            self.clkElapsed = 8
            
        elif opcode[0] == 0xEE:
            #Executa XOR A,d8
        
            #Reseta os flags
            self.reg_file.Flags = 0             

            #Instrução: XOR A,d8
            self.reg_file.A ^= opcode[1]

            #Verifica se o resulatdo foi zero
            if self.reg_file.A == 0:
                self.reg_file.setFlagBit("Z")

            #Atulaiza o contador de programa
            self.reg_file.PC += 1

            #Atualiza o clock
            self.clkElapsed = 8

        elif opcode[0] == 0xF6:
            #Executa OR A,d8
            
            #Reseta os flags
            self.reg_file.Flags == 0             

            #Instrução: OR A,r8  Opcode 0xB0 ~ 0xB7
            self.reg_file.A |= opcode[1]

            
            #Verifica se o resulatdo foi zero
            if self.reg_file.A == 0:
                self.reg_file.setFlagBit("Z")


            #Atulaiza o contador de programa
            self.reg_file.PC += 1

            #Atualiza o clock
            self.clkElapsed = 8
        
        elif opcode[0] == 0xFE:
            #Executa  CP A,d8
        
            #Reseta os flags
            self.reg_file.clrFlagBit("Z")
            self.reg_file.clrFlagBit("C")
            self.reg_file.clrFlagBit("H")
            self.reg_file.setFlagBit("N")  


            #Verifica o half carry
            if (((self.reg_file.A & 0xf) - (opcode[1] & 0xf)) < 0):
                self.reg_file.setFlagBit("H")

            #Instrução: CP A,d8
            temp = (self.reg_file.A - opcode[1])
            
            #Verifica se houve borrow
            if temp < 0:
                #Faz o overflow em 8 bits
                temp = (self.reg_file.A + 256)
                #Seta o carry
                self.reg_file.setFlagBit("C")

            #Verifica se o resulatdo foi zero
            if temp == 0:
                self.reg_file.setFlagBit("Z")

            #Atulaiza o contador de programa
            self.reg_file.PC += 1

            #Atualiza o clock
            self.clkElapsed = 8
           
   
    def ula(self,op,reg):
        #Seleciona a operação
        if op == 0:
            #Operação ADD

            #Reseta os flags
            self.reg_file.Flags = 0

            if reg == 6:
                
                #Verifica o half carry
                if ((self.reg_file.A & 0xf) + (self.mem[self.reg_file.HL] & 0xf) & 0x10) == 0x10:
                    self.reg_file.setFlagBit("H")

                #Instrução: ADD A,(HL)  Opcode 0x86
                self.reg_file.A += self.mem[self.reg_file.HL]

                #Atulaiza o contador de programa
                self.reg_file.PC += 1

                #Atualiza o clock
                self.clkElapsed = 8
               
            else:

                #Verifica o half carry
                if (((self.reg_file.A & 0xf) + (self.reg_file.readReg8(reg) & 0xf)) & 0x10) == 0x10:
                    self.reg_file.setFlagBit("H")

                #Instrução: ADD A,r8  Opcode 0x80 ~ 0x87
                self.reg_file.A += self.reg_file.readReg8(reg)

                #Atulaiza o contador de programa
                self.reg_file.PC += 1
                
                #Atualiza o clock
                self.clkElapsed = 4

            
            #Verifica se houve overflow
            if self.reg_file.A > 255:
                #Faz o overflow em 8 bits
                self.reg_file.A -= 256
                #Seta o carry
                self.reg_file.setFlagBit("C")

            #Verifica se o resulatdo foi zero
            if self.reg_file.A == 0:
                self.reg_file.setFlagBit("Z")
                         
        elif op == 1:
            #Operação ADC

            #Reseta os flags
            self.reg_file.clrFlagBit("Z")
            self.reg_file.clrFlagBit("H")
            self.reg_file.clrFlagBit("N")            

            if reg == 6:
                
                #Verifica o half carry
                if (((self.reg_file.A + self.reg_file.getFlagBit("C")) & 0xf) + (self.mem[self.reg_file.HL] & 0xf) & 0x10) == 0x10:
                    self.reg_file.setFlagBit("H")

                #Instrução: ADC A,(HL)  Opcode 0x8E
                self.reg_file.A += (self.mem[self.reg_file.HL] + self.reg_file.getFlagBit("C"))

                #Atulaiza o contador de programa
                self.reg_file.PC += 1
                
                #Atualiza o clock
                self.clkElapsed = 8
               
            else:

                #Verifica o half carry
                if ((((self.reg_file.A + self.reg_file.getFlagBit("C")) & 0xf) + (self.reg_file.readReg8(reg) & 0xf)) & 0x10) == 0x10:
                    self.reg_file.setFlagBit("H")

                #Instrução: ADC A,r8  Opcode 0x88 ~ 0x8F
                self.reg_file.A += (self.reg_file.readReg8(reg) + self.reg_file.getFlagBit("C"))

                #Atulaiza o contador de programa
                self.reg_file.PC += 1
                
                #Atualiza o clock
                self.clkElapsed = 4

            
            #Verifica se houve overflow
            if self.reg_file.A > 255:
                #Faz o overflow em 8 bits
                self.reg_file.A -= 256
                #Seta o carry
                self.reg_file.setFlagBit("C")
            else:
                self.reg_file.clrFlagBit("C") 

            #Verifica se o resulatdo foi zero
            if self.reg_file.A == 0:
                self.reg_file.setFlagBit("Z")
    
           
        elif op == 2:
        #Operação SUB

            #Reseta os flags
            self.reg_file.clrFlagBit("Z")
            self.reg_file.clrFlagBit("C")
            self.reg_file.clrFlagBit("H")
            self.reg_file.setFlagBit("N")  

            if reg == 6:
                
                #Verifica o half carry
                if (((self.reg_file.A & 0xf) - (self.mem[self.reg_file.HL] & 0xf)) < 0):
                    self.reg_file.setFlagBit("H")

                #Instrução: SUB A,(HL)  Opcode 0x96
                self.reg_file.A -= self.mem[self.reg_file.HL]

                #Atulaiza o contador de programa
                self.reg_file.PC += 1
                
                #Atualiza o clock
                self.clkElapsed = 8
               
            else:

                #Verifica o half carry
                if (((self.reg_file.A & 0xf) - (self.reg_file.readReg8(reg) & 0xf)) < 0):
                    self.reg_file.setFlagBit("H")

                #Instrução: SUB A,r8  Opcode 0x90 ~ 0x97
                self.reg_file.A -= self.reg_file.readReg8(reg)

                #Atulaiza o contador de programa
                self.reg_file.PC += 1
                
                #Atualiza o clock
                self.clkElapsed = 4

            
            #Verifica se houve borrow
            if self.reg_file.A < 0:
                #Faz o overflow em 8 bits
                self.reg_file.A += 256
                #Seta o carry
                self.reg_file.setFlagBit("C")

            #Verifica se o resulatdo foi zero
            if self.reg_file.A == 0:
                self.reg_file.setFlagBit("Z")
            
        elif op == 3:
        #Operação SBC

            #Reseta os flags
            self.reg_file.clrFlagBit("Z")
            self.reg_file.clrFlagBit("H")
            self.reg_file.setFlagBit("N")            

            if reg == 6:
                
                #Verifica o half carry
                if (((self.reg_file.A - self.reg_file.getFlagBit("C")) & 0xf) - (self.mem[self.reg_file.HL] & 0xf) < 0):
                    self.reg_file.setFlagBit("H")

                #Instrução: SBC A,(HL)  Opcode 0x9E
                self.reg_file.A -= (self.mem[self.reg_file.HL] + self.reg_file.getFlagBit("C"))

                #Atulaiza o contador de programa
                self.reg_file.PC += 1
                
                #Atualiza o clock
                self.clkElapsed = 8
               
            else:

                #Verifica o half carry
                if ((((self.reg_file.A - self.reg_file.getFlagBit("C") ) & 0xf) - (self.reg_file.readReg8(reg) & 0xf)) < 0):
                    self.reg_file.setFlagBit("H")

                #Instrução: SBC A,r8  Opcode 0x98 ~ 0x9F
                self.reg_file.A -= (self.reg_file.readReg8(reg) + self.reg_file.getFlagBit("C"))

                #Atulaiza o contador de programa
                self.reg_file.PC += 1
                
                #Atualiza o clock
                self.clkElapsed = 4

            
            #Verifica se houve overflow
            if self.reg_file.A < 0:
                #Faz o overflow em 8 bits
                self.reg_file.A += 256
                #Seta o carry
                self.reg_file.setFlagBit("C")
            else:
                self.reg_file.clrFlagBit("C") 

            #Verifica se o resulatdo foi zero
            if self.reg_file.A == 0:
                self.reg_file.setFlagBit("Z")
            
        elif op == 4:
        #Operação AND

            #Reseta os flags
            self.reg_file.clrFlagBit("Z")
            self.reg_file.setFlagBit("H")
            self.reg_file.clrFlagBit("N")
            self.reg_file.clrFlagBit("C")             

            if reg == 6:
                #Instrução: AND A,(HL)  Opcode 0xA6
                self.reg_file.A &= self.mem[self.reg_file.HL]

                #Atulaiza o contador de programa
                self.reg_file.PC += 1
                
                #Atualiza o clock
                self.clkElapsed = 8
               
            else:
                #Instrução: AND A,r8  Opcode 0xA0 ~ 0xA7
                self.reg_file.A &= self.reg_file.readReg8(reg)

                #Atulaiza o contador de programa
                self.reg_file.PC += 1
                
                #Atualiza o clock
                self.clkElapsed = 4

            
            #Verifica se o resulatdo foi zero
            if self.reg_file.A == 0:
                self.reg_file.setFlagBit("Z")
 
        elif op == 5:
        #Operação XOR
        
            #Reseta os flags
            self.reg_file.Flags = 0             

            if reg == 6:
                #Instrução: XOR A,(HL)  Opcode 0xAE
                self.reg_file.A ^= self.mem[self.reg_file.HL]

                #Atulaiza o contador de programa
                self.reg_file.PC += 1
                
                #Atualiza o clock
                self.clkElapsed = 8
               
            else:
                #Instrução: XOR A,r8  Opcode 0xA8 ~ 0xAF
                self.reg_file.A ^= self.reg_file.readReg8(reg)

                #Atulaiza o contador de programa
                self.reg_file.PC += 1
                
                #Atualiza o clock
                self.clkElapsed = 6

            
            #Verifica se o resulatdo foi zero
            if self.reg_file.A == 0:
                self.reg_file.setFlagBit("Z")
            
 
        elif op == 6:
        #Operação OR
        
            #Reseta os flags
            self.reg_file.Flags == 0             

            if reg == 6:              
                #Instrução: OR A,(HL)  Opcode 0xB6
                self.reg_file.A |= self.mem[self.reg_file.HL]

                #Atulaiza o contador de programa
                self.reg_file.PC += 1
                
                #Atualiza o clock
                self.clkElapsed = 8
               
            else:
                #Instrução: OR A,r8  Opcode 0xB0 ~ 0xB7
                self.reg_file.A |= self.reg_file.readReg8(reg)

                #Atulaiza o contador de programa
                self.reg_file.PC += 1
                
                #Atualiza o clock
                self.clkElapsed = 4

            
            #Verifica se o resulatdo foi zero
            if self.reg_file.A == 0:
                self.reg_file.setFlagBit("Z")
        

        else:
        #Operação CP

            #Reseta os flags
            self.reg_file.clrFlagBit("Z")
            self.reg_file.clrFlagBit("C")
            self.reg_file.clrFlagBit("H")
            self.reg_file.setFlagBit("N")  

            if reg == 6:
                
                #Verifica o half carry
                if ((self.reg_file.A & 0xf) - (self.mem[self.reg_file.HL] & 0xf) < 0):
                    self.reg_file.setFlagBit("H")

                #Instrução: CP A,(HL)  Opcode 0xBE
                temp = (self.reg_file.A - self.mem[self.reg_file.HL])

                #Atulaiza o contador de programa
                self.reg_file.PC += 1
                
                #Atualiza o clock
                self.clkElapsed = 8
               
            else:

                #Verifica o half carry
                if (((self.reg_file.A & 0xf) - (self.reg_file.readReg8(reg) & 0xf)) < 0):
                    self.reg_file.setFlagBit("H")

                #Instrução: CP A,r8  Opcode 0xB8 ~ 0xBF
                temp = (self.reg_file.A - self.reg_file.readReg8(reg))

                #Atulaiza o contador de programa
                self.reg_file.PC += 1
                
                #Atualiza o clock
                self.clkElapsed = 4

            
            #Verifica se houve borrow
            if temp < 0:
                #Faz o overflow em 8 bits
                temp = (self.reg_file.A + 256)
                #Seta o carry
                self.reg_file.setFlagBit("C")

            #Verifica se o resulatdo foi zero
            if temp == 0:
                self.reg_file.setFlagBit("Z")
       


        