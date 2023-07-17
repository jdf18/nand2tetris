// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)
//
// This program only needs to handle arguments that satisfy
// R0 >= 0, R1 >= 0, and R0*R1 < 32768.

// Put your code here.


// i = R0
// sum = 0
// for (i != 0; i--) {
//   sum = sum + R1
// }
// R2 = sum

@R0
D = M
@i
M = D
@sum
M = 0

(LOOP)
@i
D = M
@END
D; JEQ
D = D-1
@i
M = D
@R1
D = M
@sum
D = M + D
@sum
M = D
@LOOP
0; JMP
(END)
@sum
D = M
@R2
M = D