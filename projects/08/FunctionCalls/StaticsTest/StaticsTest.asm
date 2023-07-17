@256
D = A
@SP
M = D

@72ffbe85
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
(72ffbe85)

(Class1.set)

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
@16
M = D

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
@17
M = D

@0
D = A
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

(Class1.get)

@16
D = M
@SP
A = M
M = D
@SP
M = M+1

@17
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

(Class2.set)

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
@18
M = D

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
@19
M = D

@0
D = A
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

(Class2.get)

@18
D = M
@SP
A = M
M = D
@SP
M = M+1

@19
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

(Sys.init)

@6
D = A
@SP
A = M
M = D
@SP
M = M+1

@8
D = A
@SP
A = M
M = D
@SP
M = M+1

@4ab0bb50
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
@7
D = D-A
@ARG
M = D
@SP
D = M
@LCL
M = D
@Class1.set
0; JEQ
(4ab0bb50)

@SP
M = M-1
A = M
D = M
@5
M = D

@23
D = A
@SP
A = M
M = D
@SP
M = M+1

@15
D = A
@SP
A = M
M = D
@SP
M = M+1

@e20bc4c5
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
@7
D = D-A
@ARG
M = D
@SP
D = M
@LCL
M = D
@Class2.set
0; JEQ
(e20bc4c5)

@SP
M = M-1
A = M
D = M
@5
M = D

@b5b02c6b
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
@Class1.get
0; JEQ
(b5b02c6b)

@93dd56c0
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
@Class2.get
0; JEQ
(93dd56c0)

(WHILE)
@WHILE
0; JEQ
