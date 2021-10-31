# Assembler for the HACK language
# Project 6 of Nand2Tetris
# FunkeCoder23
# v0.0.1

import sys


class Assembler():
    def __init__(self):
        self.parse_arguments()
        with open(self.filename, 'r') as file:
            self.asm = file.readlines()

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
        if len(sys.argv) != 2:
            print(f"""\nERROR: Missing filename. \nUsage: {sys.argv[0]} /path/to/file.asm
            """)
            exit(1)
        else:
            self.filename = sys.argv[1]
            print(f"Assembling {self.filename}")


asm = Assembler()
print(repr(asm))
