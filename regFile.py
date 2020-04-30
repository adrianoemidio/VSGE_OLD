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

class RegisterFile:

    def __init__(self):
        self._A = 0
        self._B = 0
        self._C = 0
        self._D = 0
        self._E = 0
        self._H = 0
        self._L = 0
        self._Flags = 0
        self.SP = 0
        self.PC = 0
        self._AF = 0
        self._BC = 0
        self._DE = 0
        self._HL = 0
    
    #Escreve um dado no registro de 8 bits
    def writeReg8(self,reg,data):
        if reg == 7:
            self.A = data
        elif reg == 0:
            self.B = data
        elif reg == 1:
            self.C = data
        elif reg == 2:
            self.D = data
        elif reg == 3:
            self.E = data
        elif reg == 4:
            self.H = data
        elif reg == 5:
            self.L = data

    @property
    def A(self):
        return self._A

    @A.setter
    def A(self,data):
        self._A = data
        self._AF = ((data*256) | (self._AF & 0x00FF))

    @property
    def B(self):
        return self._B

    @B.setter
    def B(self,data):
        self._B = data
        self._BC = ((data*256) | (self._BC & 0x00FF))

    @property
    def C(self):
        return self._C

    @C.setter
    def C(self,data):
        self._C = data
        self._BC = (data | (self._BC & 0xFF00))
   

    @property
    def D(self):
        return self._D

    @D.setter
    def D(self,data):
        self._D = data
        self._DE = ((data*256) | (self._DE & 0x00FF))

    @property
    def E(self):
        return self._E

    @E.setter
    def E(self,data):
        self._E = data
        self._DE = (data | (self._DE & 0xFF00))
   

    @property
    def H(self):
        return self._H

    @H.setter
    def H(self,data):
        self._H = data
        self._HL = ((data*256) | (self._HL & 0x00FF))

    @property
    def L(self):
        return self._L

    @L.setter
    def L(self,data):
        self._L = data
        self._HL = (data | (self._HL & 0xFF00))
    
    @property
    def Flags(self):
        return self._Flags

    @Flags.setter
    def Flags(self,data):
        self._Flags = data
        self._AF = (data | (self._AF & 0xFF00))

    @property
    def HL(self):
        return self._HL

    @HL.setter
    def HL(self,data):
        self._HL = data
        self._H = (data & 0xFF00)/256
        self._L = (data & 0x00FF)

    @property
    def AF(self):
        return self._AF

    @AF.setter
    def AF(self,data):
        self._AF = data
        self._A = (data & 0xFF00)/256
        self._Flags = (data & 0x00FF)
    
    @property
    def BC(self):
        return self._BC

    @BC.setter
    def BC(self,data):
        self._BC = data
        self._B = (data & 0xFF00)/256
        self._C = (data & 0x00FF)

    @property
    def DE(self):
        return self._DE

    @DE.setter
    def DE(self,data):
        self._DE = data
        self._D = (data & 0xFF00)/256
        self._E = (data & 0x00FF)

    @HL.setter
    def HL(self,data):
        self._HL = data
        self._H = (data & 0xFF00)/256
        self._L = (data & 0x00FF)
         

    #Lê o dado de um registro de 8 bits
    def readReg8(self,reg):
        
        if reg == 7:
            return self.A
        elif reg == 0:
            return self.B
        elif reg == 1:
            return self.C
        elif reg == 2:
            return self.D
        elif reg == 3:
            return self.E
        elif reg == 4:
            return self.H
        elif reg == 5:
            return self.L
       
    
    def setFlagBit(self,bit):

        if bit == "C" or bit == 4:
            self.Flags |= 0x10
        elif bit == "H" or bit == 5:
            self.Flags |= 0x20
        elif bit == "N" or bit == 6:
            self.Flags |= 0x40
        elif bit == "Z" or bit == 7:
            self.Flags |= 0x80

    def clrFlagBit(self,bit):

        if bit == "C" or bit == 4:
            self.Flags &= (~0x10)
        elif bit == "H" or bit == 5:
            self.Flags &= (~0x20)
        elif bit == "N" or bit == 6:
            self.Flags &= (~0x40)
        elif bit == "Z" or bit == 7:
            self.Flags &= (~0x80)
    
    def getFlagBit(self,bit):

        if bit == "C" or bit == 4:
            return (self.Flags & 0x10) >> 4
        elif bit == "H" or bit == 5:
            return (self.Flags & 0x20) >> 5
        elif bit == "N" or bit == 6:
            return (self.Flags & 0x40) >> 6
        elif bit == "Z" or bit == 7:
            return (self.Flags & 0x80) >> 7

    def setRegBit(self,bit,reg):
        
        if reg == 7:
            self.A = ((self.A |(1 << bit)) & 0xFF)
        elif reg == 0:
            self.B = ((self.B |(1 << bit)) & 0xFF)
        elif reg == 1:
            self.C = ((self.C |(1 << bit)) & 0xFF)
        elif reg == 2:
            self.D = ((self.D |(1 << bit)) & 0xFF)
        elif reg == 3:
            self.E = ((self.E |(1 << bit)) & 0xFF)
        elif reg == 4:
            self.H = ((self.H |(1 << bit)) & 0xFF)
        elif reg == 5:
            self.L = ((self.L |(1 << bit)) & 0xFF)
        


    def clrRegBit(self,bit,reg):
        
        if reg == 7:
            self.A = ((self.A & (~(1 << bit)) & 0xFF))
        elif reg == 0:
            self.B = ((self.B & (~(1 << bit)) & 0xFF))
        elif reg == 1:
            self.C = ((self.C & (~(1 << bit)) & 0xFF))
        elif reg == 2:
            self.D = ((self.D & (~(1 << bit)) & 0xFF))
        elif reg == 3:
            self.E = ((self.E & (~(1 << bit)) & 0xFF))
        elif reg == 4:
            self.H = ((self.H & (~(1 << bit)) & 0xFF))
        elif reg == 5:
            self.L = ((self.L & (~(1 << bit)) & 0xFF))