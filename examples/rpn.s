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
	0x0004  # memory location
	[LIT]
	0x4     # desired length of input
	[LIT]
	0x4     # syscall: read input
	[SYS]

	[LIT]   # check output 
	0x0
	-
	[IF]
	end     # if the end result is unexpected
	
	[LIT]   # push result to stack
	0x0004
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
	*
	SWAP
	DROP

	[LIT]
	0
	[IF]
	main

divide:
	DROP
	/
	SWAP
	DROP
	
	[LIT]
	0
	[IF]
	main

print_pop: # TODO
	DROP
	[LIT]
	0x1     # syscall: print string
	[SYS]
	
	[LIT]
	0
	[IF]
	main

end:
	DROP
	.
