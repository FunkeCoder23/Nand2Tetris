// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// init

@8192
D=A
@SCREENEND
M=D  //set SCREENEND to 8192 (256x32)

// infinite loop
(loop)
@KBD
D=M // Get KBD input
@write_black
D; JNE // if any input, jump to write_black
@write_white // else, jump to write_white
0;JMP
@loop //probably redundant as should always jump back to loop, but just in case
0;JMP // go to loop 

(write_black)
// Writes black to every pixel
// Screen is 256x512
// 32 Words per row (32*16=512)
@ITER
M=0 //init ITER to 0


(write_black_loop)
@ITER
D=M // ITER -> D
@SCREEN
A=A+D // SCREEN + ITER -> A
M=-1 // RAM[SCREEN+ITER] -> black
@ITER 
M=M+1 // 1 + ITER -> ITER
D=M
@SCREENEND
D=D-M
@loop
D;JEQ // if SCREENEND-ITER == 0 exit write black loop
@write_black_loop
0;JMP


(write_white)
// Writes black to every pixel
// Screen is 256x512
// 32 Words per row (32*16=512)
@ITER
M=0 //init ITER to 0


(write_white_loop)
@ITER
D=M // ITER -> D
@SCREEN
A=A+D // SCREEN + ITER -> A
M=0 // RAM[SCREEN+ITER] -> black

// @16
// D=A // D=16
@ITER 
M=M+1 // 1 + ITER -> ITER
D=M
@SCREENEND
D=D-M
@loop
D;JEQ // if SCREENEND-ITER == 0 exit write black loop
@write_white_loop
0;JMP
