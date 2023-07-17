@256
D = A
@SP
M = D

@c501b340
D = A
@SP
A = M
M = D
@SP
M = M+1
@LCL
D = M
@SP
A = M
M = D
@SP
M = M+1
@ARG
D = M
@SP
A = M
M = D
@SP
M = M+1
@THIS
D = M
@SP
A = M
M = D
@SP
M = M+1
@THAT
D = M
@SP
A = M
M = D
@SP
M = M+1
@SP
D = M
@5
D = D-A
@ARG
M = D
@SP
D = M
@LCL
M = D
@Sys.init
0; JEQ
(c501b340)

(Main.fibonacci)

@2
D = M
@0
A = D+A
D = M
@SP
A = M
M = D
@SP
M = M+1

@2
D = A
@SP
A = M
M = D
@SP
M = M+1

@SP
M = M-1
A = M
D = M
@SP
M = M-1
A = M
D = M-D
@SP
A = M
M = -1
@da04b7a1
D; JLT
@SP
A = M
M = 0
(da04b7a1)
@SP
M = M+1

@SP
M = M - 1
A = M
D = M
@IF_TRUE
D; JNE

@IF_FALSE
0; JEQ

(IF_TRUE)
@2
D = M
@0
A = D+A
D = M
@SP
A = M
M = D
@SP
M = M+1

@LCL
D = M
@14
M = D
@5
A = D-A
D = M
@15
M = D
@SP
M = M-1
A = M
D = M
@ARG
A=M
M = D
D = A+1
@SP
M = D
@14
A = M-1
D = M
@THAT
M = D
@14
D = M
@2
A = D-A
D = M
@THIS
M = D
@14
D = M
@3
A = D-A
D = M
@ARG
M = D
@14
D = M
@4
A = D-A
D = M
@LCL
M = D
@15
A = M
0; JEQ

(IF_FALSE)
@2
D = M
@0
A = D+A
D = M
@SP
A = M
M = D
@SP
M = M+1

@2
D = A
@SP
A = M
M = D
@SP
M = M+1

@SP
M = M-1
A = M
D = M
@SP
M = M-1
A = M
D = M-D
@SP
A = M
M = D
@SP
M = M+1

@4f449f76
D = A
@SP
A = M
M = D
@SP
M = M+1
@LCL
D = M
@SP
A = M
M = D
@SP
M = M+1
@ARG
D = M
@SP
A = M
M = D
@SP
M = M+1
@THIS
D = M
@SP
A = M
M = D
@SP
M = M+1
@THAT
D = M
@SP
A = M
M = D
@SP
M = M+1
@SP
D = M
@6
D = D-A
@ARG
M = D
@SP
D = M
@LCL
M = D
@Main.fibonacci
0; JEQ
(4f449f76)

@2
D = M
@0
A = D+A
D = M
@SP
A = M
M = D
@SP
M = M+1

@1
D = A
@SP
A = M
M = D
@SP
M = M+1

@SP
M = M-1
A = M
D = M
@SP
M = M-1
A = M
D = M-D
@SP
A = M
M = D
@SP
M = M+1

@9ec054bc
D = A
@SP
A = M
M = D
@SP
M = M+1
@LCL
D = M
@SP
A = M
M = D
@SP
M = M+1
@ARG
D = M
@SP
A = M
M = D
@SP
M = M+1
@THIS
D = M
@SP
A = M
M = D
@SP
M = M+1
@THAT
D = M
@SP
A = M
M = D
@SP
M = M+1
@SP
D = M
@6
D = D-A
@ARG
M = D
@SP
D = M
@LCL
M = D
@Main.fibonacci
0; JEQ
(9ec054bc)

@SP
M = M-1
A = M
D = M
@SP
M = M-1
A = M
D = D+M
@SP
A = M
M = D
@SP
M = M+1

@LCL
D = M
@14
M = D
@5
A = D-A
D = M
@15
M = D
@SP
M = M-1
A = M
D = M
@ARG
A=M
M = D
D = A+1
@SP
M = D
@14
A = M-1
D = M
@THAT
M = D
@14
D = M
@2
A = D-A
D = M
@THIS
M = D
@14
D = M
@3
A = D-A
D = M
@ARG
M = D
@14
D = M
@4
A = D-A
D = M
@LCL
M = D
@15
A = M
0; JEQ

(Sys.init)

@4
D = A
@SP
A = M
M = D
@SP
M = M+1

@59ecac97
D = A
@SP
A = M
M = D
@SP
M = M+1
@LCL
D = M
@SP
A = M
M = D
@SP
M = M+1
@ARG
D = M
@SP
A = M
M = D
@SP
M = M+1
@THIS
D = M
@SP
A = M
M = D
@SP
M = M+1
@THAT
D = M
@SP
A = M
M = D
@SP
M = M+1
@SP
D = M
@6
D = D-A
@ARG
M = D
@SP
D = M
@LCL
M = D
@Main.fibonacci
0; JEQ
(59ecac97)

(WHILE)
@WHILE
0; JEQ
