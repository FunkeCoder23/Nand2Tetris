#!/usr/bin/env python||python
# VMTranslator for the HACK language
# Project 7 of Nand2Tetris
# FunkeCoder23
# v0.0.1



import os
import sys
import glob

from codewriter import CodeWriter
from codeparser import Parser

class Translator():
    def __init__(self):
        self.parse_arguments()
        if os.path.isfile(self.filename):
            print("is file")
            writefile=os.path.splitext(self.filename)[0]+'.asm'  
        else:
            dir=self.filename.split('\\')[-1]
            if dir=="":
                dir=self.filename.split('\\')[-2]
            writefile=self.filename+'\\'+dir+'.asm'
        print(writefile)
        # CodeWriter(writefile)

    def parse_arguments(self):
        '''
        Parses command line arguments into filename
        '''
        if len(sys.argv) != 2:
            print(f"""\nERROR: Missing filename. \nUsage: {sys.argv[0]} /path/to/folder\n       {sys.argv[0]} /path/to/file.vm
            """)
            exit(1)

        filename = sys.argv[1]
        self.filename=filename
        if os.path.isfile(filename):
            if filename.endswith('vm'):
                Parser(filename)
            else:
                print(f"ERROR: File {filename} does not end in .vm")
                exit(2)
        else:
            files=glob.glob(filename + '/*.vm')
            if len(files) != 0:
                for f in files:
                    Parser(f)
            else:
                fpath=os.path.realpath(filename)
                print(f"ERROR: No .vm files found in {fpath}")

Translator()