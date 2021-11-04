#!/usr/bin/env python||python
# Parser for the HACK language
# Project 7 of Nand2Tetris
# FunkeCoder23
# v0.0.1


import os
import sys

CMDS=[
    "C_ARITHMETIC",
    "C_PUSH",
    "C_POP",
    "C_LABEL",
    "C_GOTO",
    "C_IF",
    "C_FUNCTION",
    "C_RETURN",
    "C_CALL",
]

class Parser():
    def __init__(self,filename):
        self.stripped = []
        self.translated=[]
        with open(filename, 'r') as file:
            self.vmcode = file.readlines()
        self.stripper()
        print(self.stripped)

    def write_file(self):
        filename = os.path.splitext(self.filename)
        fileout = (filename[0] + '.hack')
        with open(fileout, 'w') as fout:
            fout.write('\n'.join(self.bytecode))

    def __repr__(self):
        '''
        Print the ASM (original) representation of the file provided
        '''
        VMCODE = ''.join(self.vmcode)
        STRIP = '\n'.join(self.stripped)
        TRANSLATED ='n'.join(self.translated)
        # BYTECODE = '\n'.join(self.bytecode)
        return (
            f"{self.filename}\n"
            f"VMCODE:\n{VMCODE}\n\n"
            f"STRIPPED:\n{STRIP}\n\n"
            f"TRANSLATED:\n{TRANSLATED}\n\n"
            # f"BYTECODE:\n{BYTECODE}\n\n"
            # f"SYMBOLS:\n{SYMBOLS}\n\n"
            # f"LABELS:\n{LABELS}\n\n"
        )

    def __print__(self):
        '''
        Print the bytecode (conversion) of the file provided
        '''
        return ''.join(self.bytcode)


    def stripper(self):
        """
        Removes comments and whitespace
        """
        # Check every line
        for line in self.vmcode:
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
    
    def parser(self):
        for line in self.stripped: 
            pass
