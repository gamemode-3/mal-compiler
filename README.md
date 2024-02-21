# MAL compiler
Python tool for compiling MAL-adjacent programs to the binary representation

- You need to edit the text file to input programs, it isn't a command line tool.
- No guarantee that it works perfectly.
- Remember to update both INPUT and  PROGRAM_START (which is the IJVM bytecode or where the microprogram starts).
- In binary operators with H and a B bus, H always has to be on the right. MAR = LV + H would work, MAR = H + LV would not.
- Every line starts with the address. The address format is the most significant bit aka branch bit followed by the line index: 0 1 is the first line. if for any reason it continues with mbs =  1, the second line is 1 2.
- This line format is also used in goto and conditional jumps, prefixed by the command index. Going to bipush2 would be 0x10 0 2. The literal binary address can also be used here (eg. 0b100011101)
- Condition notation is ifeq <address> and iflt <address>. ifeq reads the zero flag, iflt reads the negative flag.

Created according to [Structured Computer Architechture, 6th Ed. by Andrew S. Tanenbaum](https://csc-knu.github.io/sys-prog/books/Andrew%20S.%20Tanenbaum%20-%20Structured%20Computer%20Organization.pdf) for my [Mic-1 implementation in Digital](https://github.com/gamemode-3/Digital-Mic-1)
