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
	DROP
	+
	
	[LIT]
	0
	[IF]
	main

subtract:
	DROP
	-

	[LIT]
	0
	[IF]
	main

multiply:
	DROP
	[NOP]  # TODO

divide:
	DROP
	[NOP]  # TODO

print_pop: # TODO
	DROP
	[CALL]
	print_one
	DROP
	[CALL]
	print_return
	
	[LIT]
	0
	[IF]
	main

print_one:
	# convert top to char
	[LIT]
	48
	+

	# store in memory
	[LIT]
	0x0000 
	!

	# store space in memory
	[LIT]
	32
	[LIT]
	0x0001
	!
	
	[LIT]
	0x0000  # memory location
	[LIT]
	0x2     # desired length of input
	[LIT]
	0x2     # syscall: print string

	[SYS]

	DROP
	
	[EXIT]

print_return:
	# store newline in memory
	[LIT]
	10
	[LIT]
	0x0000
	!
	
	[LIT]
	0x0000  # memory location
	[LIT]
	0x1     # desired length of input
	[LIT]
	0x2     # syscall: print string
	
	[SYS]

	DROP

	[EXIT]


print_all: # TODO
	DROP
	[NOP]

end:
	DROP
	.
