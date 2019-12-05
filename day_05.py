"""
--- Day 5: Sunny with a Chance of Asteroids ---
You're starting to sweat as the ship makes its way toward Mercury. The Elves suggest that you get the air conditioner
working by upgrading your ship computer to support the Thermal Environment Supervision Terminal.

The Thermal Environment Supervision Terminal (TEST) starts by running a diagnostic program (your puzzle input).
The TEST diagnostic program will run on your existing Intcode computer after a few modifications:

First, you'll need to add two new instructions:

Opcode 3 takes a single integer as input and saves it to the position given by its only parameter. For example, the
instruction 3,50 would take an input value and store it at address 50.
Opcode 4 outputs the value of its only parameter. For example, the instruction 4,50 would output the value at address 50.
Programs that use these instructions will come with documentation that explains what should be connected to the input
and output. The program 3,0,4,0,99 outputs whatever it gets as input, then halts.

Second, you'll need to add support for parameter modes:

Each parameter of an instruction is handled based on its parameter mode. Right now, your ship computer already
understands parameter mode 0, position mode, which causes the parameter to be interpreted as a position - if the
parameter is 50, its value is the value stored at address 50 in memory. Until now, all parameters have been in
position mode.

Now, your ship computer will also need to handle parameters in mode 1, immediate mode. In immediate mode, a parameter
is interpreted as a value - if the parameter is 50, its value is simply 50.

Parameter modes are stored in the same value as the instruction's opcode. The opcode is a two-digit number based only
on the ones and tens digit of the value, that is, the opcode is the rightmost two digits of the first value in an
instruction. Parameter modes are single digits, one per parameter, read right-to-left from the opcode: the first
parameter's mode is in the hundreds digit, the second parameter's mode is in the thousands digit, the third parameter's
mode is in the ten-thousands digit, and so on. Any missing modes are 0.

For example, consider the program 1002,4,3,4,33.

The first instruction, 1002,4,3,4, is a multiply instruction - the rightmost two digits of the first value, 02, indicate
opcode 2, multiplication. Then, going right to left, the parameter modes are 0 (hundreds digit), 1 (thousands digit),
and 0 (ten-thousands digit, not present and therefore zero):

ABCDE
 1002

DE - two-digit opcode,      02 == opcode 2
 C - mode of 1st parameter,  0 == position mode
 B - mode of 2nd parameter,  1 == immediate mode
 A - mode of 3rd parameter,  0 == position mode,
                                  omitted due to being a leading zero
This instruction multiplies its first two parameters. The first parameter, 4 in position mode, works like it did
before - its value is the value stored at address 4 (33). The second parameter, 3 in immediate mode, simply has value 3.
The result of this operation, 33 * 3 = 99, is written according to the third parameter, 4 in position mode, which also
works like it did before - 99 is written to address 4.

Parameters that an instruction writes to will never be in immediate mode.

Finally, some notes:

It is important to remember that the instruction pointer should increase by the number of values in the instruction
after the instruction finishes. Because of the new instructions, this amount is no longer always 4.

Integers can be negative: 1101,100,-1,4,0 is a valid program (find 100 + -1, store the result in position 4).
The TEST diagnostic program will start by requesting from the user the ID of the system to test by running an input
instruction - provide it 1, the ID for the ship's air conditioner unit.

It will then perform a series of diagnostic tests confirming that various parts of the Intcode computer, like parameter
modes, function correctly. For each test, it will run an output instruction indicating how far the result of the test
was from the expected value, where 0 means the test was successful. Non-zero outputs mean that a function is not working
correctly; check the instructions that were run before the output instruction to see which one failed.

Finally, the program will output a diagnostic code and immediately halt. This final output isn't an error; an output
followed immediately by a halt means the program finished. If all outputs were zero except the diagnostic code, the
diagnostic program ran successfully.
"""

import os.path


if __name__ == '__main__':
	file_path = os.path.splitext( __file__ )[ 0 ] + '_input.txt'
	with open( file_path, 'r' ) as f:
		lines = f.readlines( )


	def compute( noun = None, verb = None, system_id = 1 ):
		OPCODE_ADD 			= 1 # Add position 2 to 3 and copy to position set in position 4.
		OPCODE_MULTIPLY	= 2 # Multiply position 2 to 3 and copy to position set in position 4.

		OPCODE_INPUT 		= 3 # Takes a single integer as input and saves it to the position given by its only parameter.
		OPCODE_OUTPUT 		= 4 # Outputs the value of its only parameter.

		OPCODE_JUMP_TRUE 	= 5 # If the first param is not a 0, the index becomes the second param value.
		OPCODE_JUMP_FALSE = 6 # If the first param is 0, the index  comes the second param value.

		OPCODE_LESS_THAN 	= 7 # If the first param is less than the second param, 1 gets stored at the target, otherwise 0.
		OPCODE_EQUALS 		= 8 # If the first param is equel to the second param, 1 gets stored at the target, otherwise 0.

		OPCODE_HALT 		= 99 # HALT

		PARAM_MODE_POSITION 	= 0 # Value is an index position. A value of 50 returns the value at index 50.
		PARAM_MODE_IMMEDIATE = 1 # Value is a value. A value of 50 is returned as 50.


		int_strs = lines[ 0 ].split( ',' )
		ints = [ int( x ) for x in int_strs ] # len( ) 129

		# PART 1
		program_input = list( ints )

		# Modify the input based on the instructions.
		if noun is not None:
			program_input[ 1 ] = noun

		if verb is not None:
			program_input[ 2 ] = verb

		index = 0
		while index <= ( len( program_input ) - 2 ):
			# Take the instruction at the current index and convert it to the opcode and param modes.
			instruction = program_input[ index ]
			instruction_str = str( instruction )

			while len( instruction_str ) < 5:
				instruction_str = '0' + instruction_str

			opcode = int( instruction_str[ 3: ] )

			mode_1 = int( instruction_str[ 2 ] )
			mode_2 = int( instruction_str[ 1 ] )
			mode_3 = int( instruction_str[ 0 ] ) # This should always be 0?

			if opcode == OPCODE_HALT:
				#print( 'OPCODE_HALT hit at index: {0}'.format( index ) )
				break

			# Param 1
			val1_index = index + 1
			if opcode != OPCODE_INPUT and mode_1 == PARAM_MODE_POSITION:
				val1_index = program_input[ index + 1 ]

			val1 = program_input[ val1_index ]


			if opcode == OPCODE_JUMP_TRUE:
				if val1 == 0:
					index += 2
					continue

			if opcode == OPCODE_JUMP_FALSE:
				if val1 != 0:
					index += 2
					continue


			# Param 2
			val2_index = index + 2
			if opcode not in [ OPCODE_OUTPUT ] and mode_2 == PARAM_MODE_POSITION:
				val2_index = program_input[ index + 2 ]

			if opcode not in [  ]:
				val2 = program_input[ val2_index ]

				# Param 3 - Always positional?
				target_index = program_input[ index + 3 ]


			# Process Opcodes
			if opcode == OPCODE_ADD:
				new_val = val1 + val2
				program_input[ target_index ] = new_val
				steps = 4

			elif opcode == OPCODE_MULTIPLY:
				new_val = val1 * val2
				program_input[ target_index ] = new_val
				steps = 4

			elif opcode == OPCODE_INPUT:
				program_input[ val1 ] = system_id
				steps = 2

			elif opcode == OPCODE_OUTPUT:
				print( 'OPCODE_OUTPUT: {0}'.format( val1 ) )
				steps = 2

			elif opcode == OPCODE_LESS_THAN:
				if val1 < val2:
					program_input[ target_index ] = 1

				else:
					program_input[ target_index ] = 0

				steps = 4

			elif opcode == OPCODE_EQUALS:
				if val1 == val2:
					program_input[ target_index ] = 1

				else:
					program_input[ target_index ] = 0

				steps = 4

			elif opcode == OPCODE_JUMP_TRUE:
				index = val2
				continue

			elif opcode == OPCODE_JUMP_FALSE:
				index = val2
				continue

			else:
				print( 'ERROR: Unknown Opcode: {0} at index {1}'.format( opcode, index ) )
				raise ValueError


			# Go to the next instructions.
			index += steps

		return program_input[ 0 ]




	# After providing 1 to the only input instruction and passing all the tests,
	# what diagnostic code does the program produce?
	# part 1 = 13210611
	#compute( )

	compute( system_id = 5 )