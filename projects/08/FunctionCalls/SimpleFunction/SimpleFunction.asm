
(SimpleFunction.test)
@SP
A = M
M = 0
@SP
M = M+1
@SP
A = M
M = 0
@SP
M = M+1

@1
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

@SP
M = M-1
A = M
M = !M
@SP
M = M+1

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
@SP
M = M-1
A = M
D = M-D
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
