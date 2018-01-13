main:
	# get input
	[CALL]
	read

	# test if +
	DUP
	[LIT]
	43
	-
	[IF]
	add
	
	# test if - 
	DUP
	[LIT]
	45
	-
	[IF]
	subtract
	
	# test if *
	DUP
	[LIT]
	42
	-
	[IF]
	multiply

	# test if /
	DUP
	[LIT]
	47
	-
	[IF]
	divide

	# test if ?
	DUP
	[LIT]
	63
	-
	[IF]
	print_all

	# test if ^
	DUP
	[LIT]
	94
	-
	[IF]
	print_pop

	# test if !
	DUP
	[LIT]
	33
	-
	[IF]
	end

	# if it's not a command, it should stay on the stack
	# convert character to integer
	[LIT]
	48
	-

	# jump back to main
	[LIT]
	0
	[IF]
	main

read:
	[LIT]
	0x0001  # memory location
	[LIT]
	0x1     # desired length of input
	[LIT]
	0x3     # syscall: read input
	[SYS]

	[LIT]   # check output 
	0x0
	-
	[IF]
	end     # if the end result is unexpected
	
	[LIT]   # push result to stack
	0x0001
	@

	[EXIT]

add:
	[LIT]
	0x4
	
	[LIT]
	0
	[IF]
	main

subtract:
	[LIT]
	0x7
	
	[LIT]
	0
	[IF]
	main

multiply:
	[NOP]  # TODO

divide:
	[NOP]  # TODO

print_pop: # TODO
	[NOP]

print_all: # TODO
	[NOP]

end:
	.
