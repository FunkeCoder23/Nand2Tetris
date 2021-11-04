#!/usr/bin/env python||python
# VMTranslator for the HACK language
# Project 7 of Nand2Tetris
# FunkeCoder23
# v0.0.1



import os
import sys
import glob


def parse_arguments():
    '''
    Parses command line arguments into filename
    '''
    if len(sys.argv) != 2:
        print(f"""\nERROR: Missing filename. \nUsage: {sys.argv[0]} /path/to/file.asm
        """)
        exit(1)

    filename = sys.argv[1]
    if os.path.isfile(filename):
        if filename.endswith('vm'):
            print(f" {filename}")
        else:
            print(f"ERROR: File {filename} does not end in .vm")
            exit(2)
    else:
        files=glob.glob(filename + '/*.vm')
        if len(files) != 0:
            for f in files:
                print(f" {f}")
        else:
            fpath=os.path.realpath(filename)
            print(f"ERROR: No .vm files found in {fpath}")

parse_arguments()