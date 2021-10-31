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

COMPS = {
    "0": "101010",
    "1": "111111",
    "-1": "111010",
    "D": "001100",
    "A": "110000",
    "!D": "001101",
    "!A": "110001",
    "-D": "001111",
    "-A": "110011",
    "D+1": "011111",
    "A+1": "110111",
    "D-1": "001110",
    "A-1": "110010",
    "D+A": "000010",
    "D-A": "010011",
    "A-D": "000111",
    "D&A": "000000",
    "D|A": "010101",
}

COMPSA = {
    "M": "110000",
    "!M": "110001",
    "-M": "110011",
    "M+1": "110111",
    "M-1": "110010",
    "D+M": "000010",
    "D-M": "010011",
    "M-D": "000111",
    "D&M": "000000",
    "D|M": "010101",
}

DESTS = {
    None: 0,
    "A": 4,
    "D": 2,
    "M": 1,
}

JUMPS = {
    None: "000",
    "JGT": "001",
    "JEQ": "010",
    "JGE": "011",
    "JLT": "100",
    "JNE": "101",
    "JLE": "110",
    "JMP": "111",
}

SYMBOLS = {}
LABELS = {}


class Assembler():
    def __init__(self):

        self.stripped = []
        self.nolabels = []
        self.bytecode = []

        self.parse_arguments()
        with open(self.filename, 'r') as file:
            self.asm = file.readlines()

        self.assemble()
        self.write_file()

    def write_file(self):
        filename = os.path.splitext(self.filename)
        fileout = (filename[0] + '.hack')
        with open(fileout, 'w') as fout:
            fout.write('\n'.join(self.bytecode))

    def __repr__(self):
        '''
        Print the ASM (original) representation of the file provided
        '''
        ASM = ''.join(self.asm)
        STRIP = '\n'.join(self.stripped)
        NOLABELS ='n'.join(self.nolabels)
        BYTECODE = '\n'.join(self.bytecode)
        return (
            f"{self.filename}\n"
            # f"ASM:\n{ASM}\n\n"
            f"STRIPPED:\n{STRIP}\n\n"
            f"NOLABELS:\n{NOLABELS}\n\n"
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
        self.stripper()
        self.label()
        self.translate()

    def stripper(self):
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
            print(line)
            # Check for label
            if line[0] == '(':
                label = line[1:-1]
                self.sym2int(label, linenum)
            else:
                self.nolabels.append(line)
                linenum += 1

    def comp2str(self, comp):
        if comp in COMPS:
            bytecode = '0'
            bytecode += COMPS[comp]
        elif comp in COMPSA:
            bytecode = '1'
            bytecode += COMPSA[comp]
        else:
            print(f"ERROR: Comp {comp} not found.")
            exit(1)
        return bytecode

    def jump2str(self, jump):
        if jump in JUMPS:
            bytecode = JUMPS[jump]
        else:
            print(f"ERROR: Jump {jump} not found.")
            exit(1)
        return bytecode

    def dest2str(self, dest):
        # Handle null dest
        if dest is None:
            return "000"
        destint = 0
        for d in list(dest):
            if d in DESTS:
                destint += DESTS[d]
            else:
                print(f"ERROR: Dest {d} not found.")
                exit(1)
        bytecode = f"{destint:03b}"
        return bytecode

    def Ainstr(self, line):
        bytecode = '0'
        A = line[1:]
        val = self.sym2int(A)
        bytecode += (f"{val:015b}")
        self.bytecode.append(bytecode)

    def Cinstr(self, line):
        bytecode = '111'
        dest = None
        jump = None
        # Check for =
        try:
            destsep = line.index('=')
            dest = line[:destsep]
        except:
            destsep = 1
        # Check for ;
        try:
            jumpsep = line.index(';')
            jump = line[jumpsep+1:]
        except:
            jumpsep = len(line)
        # 4 cases, in order of most likely:
        # =, ;, neither, both
        if dest is None:
            comp = line[:jumpsep]
        elif jump is None:
            comp = line[destsep+1:]
        elif dest is None and jump is None:
            comp = line
        else:
            comp = line[destsep+1:jumpsep]
        # Get bytecode for each part
        bytecode += self.comp2str(comp)
        bytecode += self.dest2str(dest)
        bytecode += self.jump2str(jump)
        self.bytecode.append(bytecode)

    def translate(self):
        for line in self.nolabels:
            # Check for A type instruction
            if line[0] == '@':
                self.Ainstr(line)
                continue
            # Handle C type instructions
            # comp mandatory, dest,jump optional
            else:
                self.Cinstr(line)
                continue

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
# print(repr(Assy))
# print(STACK)
