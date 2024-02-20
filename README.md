# mal-compiler
Python tool for compiling MAL programs to the binary representation

- You need to edit the text file to input programs, it isn't a command line tool.
- No guarantee that it works perfectly.
- Remember to update both INPUT and  PROGRAM_START (which is the IJVM bytecode or where the microprogram starts).
- In binary operators with H and a B bus, H always has to be on the right. MAR = LV + H would work, MAR = H + LV would not.