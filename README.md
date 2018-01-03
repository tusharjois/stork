# stork

`stork` is a combination of a virtual stack machine, an instruction set for the stack machine, and an assembler to bridge the two, all written in Python. It is derived from Philip Koopman's book, "Stack Computers: the new wave" first published in 1989.

## Usage

```
```

## Reference

### Virtual Stack Machine

### Instruction Set

The stack machine implements the instructions set forth by Koopman, found here, as well as a few extensions.

```
 Instr-   Opcode    Data Stack
 uction   (hex)  input   -> output   Function
 !        01     N1 ADDR ->            Store N1 at location ADDR in
                                     program memory

 +        02     N1 N2   -> N3         Add N1 and N2, giving sum N3

 -        03     N1 N2   -> N3         Subtract N2 from N1, giving
                                     difference N3

 *        04     N1 N2   -> HI LO      Multiply N1 and N2, giving
                                     the result N3. The HI bits of 
                                     N3 are pushed first, and the 
                                     LO bits are pushed next.

 /        05     N1 N2   -> HI LO      Divide N2 by N1, giving
                                     the result N3. The HI bits of 
                                     N3 are pushed first, and the 
                                     LO bits are pushed next.

 >R       06     N1      ->            Push N1 onto the return stack

 @        07     ADDR    -> N1         Fetch the value at location
                                     ADDR in program memory,
                                     returning N1

 AND      08     N1 N2   -> N3         Perform a bitwise AND on N1 and
                                     N2, giving result N3

 DROP     09     N1      ->            Drop N1 from the stack

 DUP      0A     N1      -> N1 N1      Duplicate N1, returning a
                                     second copy of it on the stack

 OR       0B     N1 N2   -> N3         Perform a bitwise OR on N1 and
                                     N2, giving result N3

 OVER     0C     N1 N2   -> N1 N2 N1   Push a copy of the second
                                     element on the stack, N1, onto
                                     the top of the stack

 R>       0D             -> N1         Pop the top element of the
                                     return stack, and push it onto
                                     the data stack as N1

 SHR      0E     N1 N2   -> N3         Perform a right shift of N2
                                     by N1 bits, giving result N3

 SHL      0F     N1 N2   -> N3         Perform a left shift of N2
                                     by N1 bits, giving result N3

 SWAP     10     N1 N2   -> N2 N1      Swap the order of the top two
                                     stack elements

 XOR      11     N1  N2  -> N3         Perform a bitwise eXclusive OR
                                     on N1 and N2, giving result N3

 [IF]     12     N1      ->            If N1 is false (value is 0)
                                     perform a branch to the address
                                     in the next program cell,
                                     otherwise continue

 [CALL]   13             ->            Perform a subroutine call to
                                     the address in the next program
                                     cell

 [EXIT]   14             ->            Perform a subroutine return

 [LIT]    15             -> N1         Treat the value in the next
                                     program cell as an integer
                                     constant, and push it onto the
                                     stack as N1
```

### Assembler

Before the compiler runs, the preprocessor indexes labels to replace them in code with addresses. Labels are of the format `identifier:`, where `identifier` is any set of ASCII letters and numbers that do not correspond to an instruction. Note that identifiers must start with a letter. It also parses `include` directives and appends those files to the end of the program. The assembler converts instruction source files into binary files readable by the Virtual Stack Machine. Newlines (`"\n"`) delineate between instructions in source files. Tabs (`"\t"`) and spaces (`" "`) can be used for formatting. Comments are indicated by `%`; the assembler ignores everything after a `%` up to the next newline.

Example source files are included in the `examples/` directory of the repository.



