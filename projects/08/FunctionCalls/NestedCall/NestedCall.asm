
(Sys.init)

@4000
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
@3
M = D

@5000
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
@4
M = D

@70818ad2
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
@Sys.main
0; JEQ
(70818ad2)

@SP
M = M-1
A = M
D = M
@6
M = D

(LOOP)
@LOOP
0; JEQ

(Sys.main)
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
@SP
A = M
M = 0
@SP
M = M+1

@4001
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
@3
M = D

@5001
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
@4
M = D

@200
D = A
@SP
A = M
M = D
@SP
M = M+1

@1
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

@40
D = A
@SP
A = M
M = D
@SP
M = M+1

@1
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

@6
D = A
@SP
A = M
M = D
@SP
M = M+1

@1
D = M
@3
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

@123
D = A
@SP
A = M
M = D
@SP
M = M+1

@9ebade83
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
@Sys.add12
0; JEQ
(9ebade83)

@SP
M = M-1
A = M
D = M
@5
M = D

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

@1
D = M
@2
A = D+A
D = M
@SP
A = M
M = D
@SP
M = M+1

@1
D = M
@3
A = D+A
D = M
@SP
A = M
M = D
@SP
M = M+1

@1
D = M
@4
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

(Sys.add12)

@4002
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
@3
M = D

@5002
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

@12
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
