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
	print_pop

	# test if !
	DUP
	[LIT]
	33
	end

	# jump back to main
	[LIT]
	0
	[IF]
	exit

read:
	[LIT]
	[NOP] # TODO

add:
	[LIT]
	0x4

subtract:
	[LIT]
	0x7

multiply:
	[NOP]  # TODO

divide:
	[NOP]  # TODO

print_pop: # TODO
	[NOP]

print_all: # TODO
	[NOP]

exit:
	.
