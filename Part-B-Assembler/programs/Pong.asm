// EDUCATIONAL SMOKE TEST ONLY — NOT the official Nand2Tetris Pong.asm.
// Use the official course Pong.asm for the required comparison.
@KBD
D=M
@PRESSED
D;JGT
@0
D=A
@SCREEN
M=D
@LOOP
0;JMP
(PRESSED)
@SCREEN
M=-1
(LOOP)
@LOOP
0;JMP
