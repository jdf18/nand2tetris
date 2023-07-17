
@2
D = M
@1
A = D+A
D = M
@SP
A = M
M = D
@SP
M = M+1

@SP
M = M-1
A = M
D = M
@4
M = D

@0
D = A
@SP
A = M
M = D
@SP
M = M+1

@4
D = M
@0
D = D+A
@13
M = D
@SP
M = M-1
A = M
D = M
@13
A = M
M = D

@1
D = A
@SP
A = M
M = D
@SP
M = M+1

@4
D = M
@1
D = D+A
@13
M = D
@SP
M = M-1
A = M
D = M
@13
A = M
M = D

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

@2
D = M
@0
D = D+A
@13
M = D
@SP
M = M-1
A = M
D = M
@13
A = M
M = D

(MAIN_LOOP_START)
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

@SP
M = M - 1
A = M
D = M
@COMPUTE_ELEMENT
D; JNE

@END_PROGRAM
0; JEQ

(COMPUTE_ELEMENT)
@4
D = M
@0
A = D+A
D = M
@SP
A = M
M = D
@SP
M = M+1

@4
D = M
@1
A = D+A
D = M
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
D = D+M
@SP
A = M
M = D
@SP
M = M+1

@4
D = M
@2
D = D+A
@13
M = D
@SP
M = M-1
A = M
D = M
@13
A = M
M = D

@4
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
D = D+M
@SP
A = M
M = D
@SP
M = M+1

@SP
M = M-1
A = M
D = M
@4
M = D

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

@2
D = M
@0
D = D+A
@13
M = D
@SP
M = M-1
A = M
D = M
@13
A = M
M = D

@MAIN_LOOP_START
0; JEQ

(END_PROGRAM)