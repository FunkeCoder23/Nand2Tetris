# Assembler for the HACK language
# Project 6 of Nand2Tetris
# FunkeCoder23
# v0.0.1

import os
import sys

REGISTERS = {
    "R0": 0,
    "R1": 1,
    "R2": 2,
    "R3": 3,
    "R4": 4,
    "R5": 5,
    "R6": 6,
    "R7": 7,
    "R8": 8,
    "R9": 9,
    "R10": 10,
    "R11": 11,
    "R12": 12,
    "R13": 13,
    "R14": 14,
    "R15": 15,
    "SP": 0,
    "LCL": 1,
    "ARG": 2,
    "THIS": 3,
    "THAT": 4,
    "SCREEN": 16384,
    "KBD": 24576,
}

DEST = {
    "A": 4,
    "D": 2,
    "M": 1,
}

SYMBOLS = {}
LABELS = {}


class Assembler():
    def __init__(self):

        self.stripped = []
        self.bytecode = []

        self.parse_arguments()
        with open(self.filename, 'r') as file:
            self.asm = file.readlines()

        self.assemble()
        # self.write_file()

    def write_file(self):
        filename = os.path.splitext(self.filename)
        fileout=(filename[0] + '.hack')
        with open(fileout,'w') as fout:
            fout.write('\n'.join(self.bytecode))

    def __repr__(self):
        '''
        Print the ASM (original) representation of the file provided
        '''
        ASM = ''.join(self.asm)
        STRIP = '\n'.join(self.stripped)
        BYTECODE = '\n'.join(self.bytecode)
        return (
            f"{self.filename}\n"
            # f"ASM:\n{ASM}\n\n"
            f"STRIPPED:\n{STRIP}\n\n"
            f"BYTECODE:\n{BYTECODE}\n\n"
            f"SYMBOLS:\n{SYMBOLS}\n\n"
            f"LABELS:\n{LABELS}\n\n"
        )

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
        self.label()
        self.symbolize()
        self.translate()

    def symbolize(self):
        """
        Converts ASM to it's base symbols
        Removes comments and whitespace
        """
        # Check every line
        for line in self.asm:
            # Check for comments and remove
            comment = line.rfind("//")
            line = line[:comment]
            # Remove whitespace
            line = line.strip()
            # Remove empty lines after stripping
            if len(line) == 0:
                continue
            # Store whatever is left
            self.stripped.append(line)

    def label(self):
        linenum = 0
        for line in self.stripped:
            # Check for label
            if line[0] == '(':
                print("GOT HERE")
                label = line[1:-1]
                self.sym2int(label, linenum)
            self.stripped.remove(line)
            linenum += 1

    def translate(self):
        for line in self.stripped:
            # Check for A type instruction
            if line[0] == '@':
                bytecode = '0'
                A = line[1:]
                val = self.sym2int(A)
                bytecode += (f"{val:015b}")
                self.bytecode.append(bytecode)
                continue
            # Handle C type instructions
            # comp mandatory, dest,jump optional
            bytecode = '111'

    # def dest2int(self,dest):

    def sym2int(self, sym, linenum=None):
        '''
        Converts @sym to integer

        - if @sym == {R0, R1, R2, ...} returns 0,1,2,...
        - if @sym == {SCREEN, KBD, ...} returns 16384, 24576, etc
        - if @sym is user created return its value
        - else add @sym to SYMBOLS list and return its value
        '''
        # See if constant val
        try:
            symint = int(sym)
        except:
            pass
        else:
            return symint
        # Check in Registers
        if sym in REGISTERS:
            return REGISTERS[sym]
        # Check in Symbols
        if sym in SYMBOLS:
            return SYMBOLS[sym]
        # Check in Labels
        if sym in LABELS:
            return LABELS[sym]
        # if linenum passed, add to val
        if linenum is not None:
            LABELS.update({sym: linenum})
            return LABELS[sym]
        else:
            addr = len(SYMBOLS)+16  # RAM address
            SYMBOLS.update({sym: addr})
            return SYMBOLS[sym]


Assy = Assembler()
print(repr(Assy))
# print(STACK)
