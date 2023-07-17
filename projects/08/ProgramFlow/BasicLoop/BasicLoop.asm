
@0
D = A
@SP
A = M
M = D
@SP
M = M+1

@1
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

(LOOP_START)
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

@1
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
@LOOP_START
D; JNE

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
