# Assembler for the HACK language
# Project 6 of Nand2Tetris
# FunkeCoder23
# v0.0.1

import sys

REGISTERS = {
    "R0": 0,
    "R1":1,
    "R2":2,
    "R3":3,
    "R4":4,
    "R5":5,
    "R6":6,
    "R7":7,
    "R8":8,
    "R9":9,
    "R10":10,
    "R11":11,
    "R12":12,
    "R13":13,
    "R14":14,
    "R15":15,
    "SP":0,
    "LCL":1,
    "ARG":2,
    "THIS":3,
    "THAT":4,
    "SCREEN":16384,
    "KBD":24576,
}

DEST={
    "A":4,
    "D":2,
    "M":1,
}

STACK={}



class Assembler():
    def __init__(self):

        self.symbols=[]

        self.parse_arguments()
        with open(self.filename, 'r') as file:
            self.asm = file.readlines()
        self.assemble()

    def __repr__(self):
        '''
        Print the ASM (original) representation of the file provided
        '''
        return ''.join(self.asm)

    def __print__(self):
        '''
        Print the bytecode (conversion) of the file provided
        '''
        return ''.join(self.bytcode)

    def parse_arguments(self):
        '''
        Parses command line arguments into filename
        '''
        if len(sys.argv) != 2:
            print(f"""\nERROR: Missing filename. \nUsage: {sys.argv[0]} /path/to/file.asm
            """)
            exit(1)
        else:
            self.filename = sys.argv[1]
            print(f"Assembling {self.filename}")
    
    def assemble(self):
        self.symbolize()
        self.translate()

    def symbolize(self):
        """
        Converts ASM to it's base symbols
        Removes comments and whitespace
        """
        #Check every line
        for line in self.asm:
            # Check for comments and remove
            comment=line.rfind("//")
            line=line[:comment]
            # Remove whitespace
            line=line.strip()
            # Remove empty lines after stripping
            if len(line) == 0:
                continue
            # Store whatever is left
            self.symbols.append(line)

    def translate(self):
        for line in self.symbols:
            if line[0] == '@':
                A=line[1:]
                self.reg2int(A)

    def reg2int(self,sym):
        try:
            symint=int(sym)
        except:
            pass
        else:
            return symint
        if sym in REGISTERS:
            return REGISTERS[sym]
        elif sym in STACK:
            return STACK[sym]
        else:
            STACK.update({sym:len(STACK)+16})
            return STACK[sym]

Assy = Assembler()
print(STACK)