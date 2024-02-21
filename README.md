# mal-compiler
Python tool for compiling MAL programs to the binary representation

- You need to edit the text file to input programs, it isn't a command line tool.
- No guarantee that it works perfectly.
- Remember to update both INPUT and  PROGRAM_START (which is the IJVM bytecode or where the microprogram starts).
- In binary operators with H and a B bus, H always has to be on the right. MAR = LV + H would work, MAR = H + LV would not.

Created according to Structured Computer Architechture, 6th Ed. by Andrew S. Tanenbaum^[[4]](https://csc-knu.github.io/sys-prog/books/Andrew%20S.%20Tanenbaum%20-%20Structured%20Computer%20Organization.pdf)
