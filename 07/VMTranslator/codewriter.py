#!/usr/bin/env python3||python
# CodeWriter for the HACK language
# Project 7 of Nand2Tetris
# FunkeCoder23
# v0.0.1


class CodeWriter():
    def __init__(self,filename):
        self.filename=filename
        self.asm=[]

    def WritePushPop(self, cmd, seg, index):
        """
        Writes the asm code that is the translation of the given cmd,
        where cmd is either:
        * C_PUSH
        * C_POP
        """
        pass

    def writeArithmetic(self, cmd):
        """
        Writes asm code that is the translation of the given arithmetic code
        """
        pass

    def close(self):
        with open(self.filename,'w') as f:
            for line in self.asm:
                f.write(line)
