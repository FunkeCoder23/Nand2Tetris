#!/usr/bin/env python3||python
# CodeWriter for the HACK language
# Project 7 of Nand2Tetris
# FunkeCoder23
# v0.0.1


import os
from posixpath import split

CMDS = {
    # Arithmetic funcs
    "add": "C_ARITHMETIC",
    "sub": "C_ARITHMETIC",
    "and": "C_ARITHMETIC",
    "or": "C_ARITHMETIC",
    "not": "C_ARITHMETIC",
    "neg": "C_ARITHMETIC",
    "eq": "C_ARITHMETIC",
    "gt": "C_ARITHMETIC",
    "lt": "C_ARITHMETIC",
    # Stack funcs
    "push": "C_PUSH",
    "pop": "C_POP",
    # C_LABEL,
    # C_GOTO,
    # C_IF,
    # C_FUNCTION,
    # C_RETURN,
    # C_CALL
}

MATHS = {
    "add": "M+D",
    "sub": "M-D",
    "and": "M&D",
    "or": "M|D",
}
SEGMENTS = {
    "local": "LCL",
    "argument": "ARG",
    "this": "THIS",
    "that": "THAT",
}

JUMPS = {
    "eq": "JEQ",
    "lt": "JLT",
    "gt": "JGT",
}
STATIC = {}


class CodeWriter():
    def __init__(self, filename, stripped):
        self.jumps = 0
        self.filename = os.path.splitext(filename)[0]
        self.name = os.path.basename(self.filename)
        print(self.name)
        self.stripped = stripped
        self.asm = []
        self.translate()
        self.write_file()
        print(repr(self))

    def __repr__(self):
        return f"""
        {self.name}
        
        {self.asm}

        {STATIC}
        """

    def write_file(self):
        fileout = (self.filename + '.asm')
        with open(fileout, 'w') as fout:
            fout.write('\n'.join(self.asm))

    def translate(self):
        for line in self.stripped:
            args = line.split(" ")
            cmd = args[0]
            if CMDS[cmd] == "C_ARITHMETIC":
                self.writeArithmetic(args)
            if CMDS[cmd] == "C_PUSH" or CMDS[cmd] == "C_POP":
                self.WritePushPop(args)

    def WritePushPop(self, args):
        """
        Writes the asm code that is the translation of the given cmd,
        where cmd is either:
        * C_PUSH
        * C_POP
        """
        self.asm.append(f"//{' '.join(args)}")

        cmd = args[0]
        seg = args[1]
        index = int(args[2])

        if seg in SEGMENTS:
            seg = SEGMENTS[seg]
            if cmd == "pop":
                # ADDR = LCL + i
                self.asm.append(f"@{seg}")   # A = LCL
                self.asm.append("D=M")       # D = *LCL
                self.asm.append(f"@{index}")  # A = i
                self.asm.append("D=A+D")     # D = (LCL+i)
                self.asm.append("@R13")      # A = R13
                self.asm.append("M=D")       # *R13 = LCL+i
                # SP--
                self.asm.append("@SP")       # A = SP
                self.asm.append("AM=M-1")    # SP--
                # *ADDR=*SP
                self.asm.append("D=M")       # D = *SP
                self.asm.append("@R13")      # A = R13
                self.asm.append("A=M")       # A = LCL+1
                self.asm.append("M=D")       # *(LCL+1) = *SP
            if cmd == "push":
                # ADDR = LCL + i
                self.asm.append(f"@{seg}")      # A = LCL
                self.asm.append("D=M")       # D = *LCL
                self.asm.append(f"@{index}")  # A = i
                self.asm.append("A=A+D")     # A = (LCL+i)
                self.asm.append("D=M")       # D = *(LCL+i)
                # *SP = *addr
                self.asm.append("@SP")       # A = SP
                self.asm.append("A=M")       # A = *SP
                self.asm.append("M=D")       # *SP = *(LCL+i)
                # SP ++
                self.asm.append("@SP")       # A = SP
                self.asm.append("M=M+1")     # SP++

        elif seg == "constant":
            if cmd == "push":
                self.asm.append(f'@{index}')  # i
                self.asm.append("D=A")        # D = i
                self.asm.append("@SP")        # A = SP
                self.asm.append("A=M")        # A = *SP
                self.asm.append("M=D")        # *SP = index
                self.asm.append("@SP")        # A = SP
                self.asm.append("M=M+1")      # *SP++
            if cmd == "pop":
                self.asm.append("@SP")        # A = SP
                self.asm.append("AM=M-1")      # *SP--
                self.asm.append("D=M")        # D = *SP

        elif seg == "static":
            addr = f"{self.name}.{index}"
            if cmd == "pop":
                # ADDR = LCL + i
                self.asm.append(f"@{addr}")   # A = s
                self.asm.append("D=A")       # D = s
                # self.asm.append(f"@{index}")  # A = i
                # self.asm.append("D=A+D")     # D = (s+i)
                self.asm.append("@R13")      # A = R13
                self.asm.append("M=D")       # *R13 = s+i
                # SP--
                self.asm.append("@SP")       # A = SP
                self.asm.append("AM=M-1")    # SP--
                # *ADDR=*SP
                self.asm.append("D=M")       # D = *SP
                self.asm.append("@R13")      # A = R13
                self.asm.append("A=M")       # A = LCL+1
                self.asm.append("M=D")       # *(LCL+1) = *SP
            if cmd == "push":
                # ADDR = LCL + i
                self.asm.append(f"@{addr}")      # A = static
                self.asm.append("D=M")       # A = *static
                # self.asm.append(f"@{index}")  # A = i
                # self.asm.append("A=A+D")     # A = (static+i)
                # self.asm.append("D=M")       # D = *(static+i)
                # *SP = *addr
                self.asm.append("@SP")       # A = SP
                self.asm.append("A=M")       # A = *SP
                self.asm.append("M=D")       # *SP = *(LCL+i)
                # SP ++
                self.asm.append("@SP")       # A = SP
                self.asm.append("M=M+1")     # SP++

        elif seg == "temp":
            if index > 7 or index < 0:
                print(f"OOB {args}")
            idx = index + 5  # temp i -> i + 5
            if cmd == "push":
                self.asm.append(f'@{idx}')  # i
                self.asm.append("D=M")        # D = i
                self.asm.append("@SP")        # A = SP
                self.asm.append("A=M")        # A = *SP
                self.asm.append("M=D")        # *SP = index
                self.asm.append("@SP")        # A = SP
                self.asm.append("M=M+1")      # *SP++
            if cmd == "pop":
                self.asm.append("@SP")        # A = SP
                self.asm.append("AM=M-1")      # *SP--
                self.asm.append("D=M")        # D = *SP
                self.asm.append(f'@{idx}')  # i
                self.asm.append("M=D")        # *SP = index

        elif seg == "pointer":
            if index > 1 or index < 0:
                print(f"OOB {args}")
            idx = index + 3  # pointer i -> i + 3
            if cmd == "push":
                self.asm.append(f'@{idx}')  # i
                self.asm.append("D=M")        # D = i
                self.asm.append("@SP")        # A = SP
                self.asm.append("A=M")        # A = *SP
                self.asm.append("M=D")        # *SP = index
                self.asm.append("@SP")        # A = SP
                self.asm.append("M=M+1")      # *SP++
            if cmd == "pop":
                self.asm.append("@SP")        # A = SP
                self.asm.append("AM=M-1")      # *SP--
                self.asm.append("D=M")        # D = *SP
                self.asm.append(f'@{idx}')  # i
                self.asm.append("M=D")        # *SP = index
        else:
            print(f"Unhandled PUSH/POP: {cmd} {seg} {index}")
            exit(1)
        self.asm.append("")

    def writeArithmetic(self, args):
        """
        Writes asm code that is the translation of the given arithmetic code
        """
        cmd = args[0]
        if cmd == "not" or cmd == "neg":
            self.asm.append(f"//{' '.join(args)}")
            self.asm.append("@SP")    # A = SP
            self.asm.append("A=M-1")  # SP--
            if cmd == "not":
                self.asm.append("M=!M")
                self.asm.append("")
                return
            if cmd == "neg":
                self.asm.append("M=-M")
                self.asm.append("")
                return
        
        self.asm.append("@SP")    # A = SP
        self.asm.append("AM=M-1")  # SP--
        self.asm.append("D=M")    # D = y
        if cmd in MATHS:
            cmd=MATHS[cmd]
            self.asm.append("A=A-1")  # SP--
            self.asm.append(f"M={cmd}")  # SP = x + y
        
        elif cmd in JUMPS:
            cmd = JUMPS[cmd]
            self.asm.append("@SP")
            self.asm.append("AM=M-1")  # SP--
            self.asm.append("D=M-D")  # D = x - y
            self.asm.append(f"@j{self.jumps}_true")  # @j#_true
            self.asm.append(f"D;{cmd}")  # jump if D = 0
            # False case
            self.asm.append("@SP")
            self.asm.append("A=M")
            self.asm.append("M=0")
            self.asm.append(f"@j{self.jumps}_end")  # @j#_end
            self.asm.append("0;JMP")
            # True case
            self.asm.append(f"(j{self.jumps}_true)")
            self.asm.append("@SP")
            self.asm.append("A=M")
            self.asm.append("M=-1")
            self.asm.append(f"(j{self.jumps}_end)")
            self.asm.append("@SP")        # A = SP
            self.asm.append("M=M+1")      # *SP++
            self.jumps += 1
        else:
            print(f"Unhandled Arithmetic: {cmd}")
            exit(1)
        self.asm.append("")

    def close(self):
        with open(self.filename, 'w') as f:
            for line in self.asm:
                f.write(line)
