#!/usr/bin/env python||python
# VMTranslator for the HACK language
# Project 7 of Nand2Tetris
# FunkeCoder23
# v0.0.1

import os
import sys

class Translator():
    def __init__(self):
        self.stripped = []
        self.parse_arguments()
        with open(self.filename, 'r') as file:
            self.vmcode = file.readlines()
        self.stripper()


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
        # NOLABELS ='n'.join(self.nolabels)
        # BYTECODE = '\n'.join(self.bytecode)
        return (
            f"{self.filename}\n"
            f"VMCODE:\n{VMCODE}\n\n"
            f"STRIPPED:\n{STRIP}\n\n"
            # f"NOLABELS:\n{NOLABELS}\n\n"
            # f"BYTECODE:\n{BYTECODE}\n\n"
            # f"SYMBOLS:\n{SYMBOLS}\n\n"
            # f"LABELS:\n{LABELS}\n\n"
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


VMT = Translator() 
print(repr(VMT))