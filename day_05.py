import os.path


def translate_instruction( instruction ):
	instruction_str = str( instruction )

	while len( instruction_str ) < 5:
		instruction_str = '0' + instruction_str

	opcode = int( instruction_str[ 3: ] )
	mode_1 = int( instruction_str[ 2 ] )
	mode_2 = int( instruction_str[ 1 ] )
	mode_3 = int( instruction_str[ 0 ] ) # This should always be 0?

	return opcode, mode_1, mode_2, mode_3



def get_param_val( data, index, mode ):
	PARAM_MODE_POSITION 	= 0 # Value is an index position. A value of 50 returns the value at index 50.
	PARAM_MODE_IMMEDIATE = 1 # Value is a value. A value of 50 is returned as 50.

	# Mode Position
	if mode == PARAM_MODE_POSITION:
		return data[ data[ index ] ]

	# Mode Immediate
	return data[ index ]



def get_param_vals( data, index, mode_1, mode_2 ):
	val_1 = get_param_val( data, index + 1, mode_1 )
	val_2 = get_param_val( data, index + 2, mode_2 )

	return val_1, val_2



def compute( input_data, input_val = 1 ):
	OPCODE_ADD 			= 1 # Add position 2 to 3 and copy to position set in position 4.
	OPCODE_MULTIPLY	= 2 # Multiply position 2 to 3 and copy to position set in position 4.

	OPCODE_INPUT 		= 3 # Takes a single integer as input and saves it to the position given by its only parameter.
	OPCODE_OUTPUT 		= 4 # Outputs the value of its only parameter.

	OPCODE_JUMP_TRUE 	= 5 # If the first param is not a 0, the index becomes the second param value.
	OPCODE_JUMP_FALSE = 6 # If the first param is 0, the index  comes the second param value.

	OPCODE_LESS_THAN 	= 7 # If the first param is less than the second param, 1 gets stored at the target, otherwise 0.
	OPCODE_EQUALS 		= 8 # If the first param is equel to the second param, 1 gets stored at the target, otherwise 0.

	OPCODE_HALT 		= 99 # HALT


	# Make a copy of the data so we can modify it.
	data = list( input_data )

	diagnostic_code = None

	index = 0
	while data[ index ] != OPCODE_HALT:
		opcode, mode_1, mode_2, mode_3 = translate_instruction( data[ index ] )

		if opcode == OPCODE_ADD:
			val_1, val_2 = get_param_vals( data, index, mode_1, mode_2 )
			data[ data[ index + 3 ] ] = val_1 + val_2
			index += 4

		elif opcode == OPCODE_MULTIPLY:
			val_1, val_2 = get_param_vals( data, index, mode_1, mode_2 )
			data[ data[ index + 3 ] ] = val_1 * val_2
			index += 4

		elif opcode == OPCODE_INPUT:
			data[ data[ index + 1] ] = input_val
			index += 2

		elif opcode == OPCODE_OUTPUT:
			diagnostic_code = data[ data[ index + 1 ] ]
			index += 2

		elif opcode == OPCODE_JUMP_TRUE:
			val_1, val_2 = get_param_vals( data, index, mode_1, mode_2 )
			index = val_2 if val_1 != 0 else index + 3

		elif opcode == OPCODE_JUMP_FALSE:
			val_1, val_2 = get_param_vals( data, index, mode_1, mode_2 )
			index = val_2 if val_1 == 0 else index + 3

		elif opcode == OPCODE_LESS_THAN:
			val_1, val_2 = get_param_vals( data, index, mode_1, mode_2 )
			data[ data[ index + 3 ] ] = 1 if val_1 < val_2 else 0
			index += 4

		elif opcode == OPCODE_EQUALS:
			val_1, val_2 = get_param_vals( data, index, mode_1, mode_2 )
			data[ data[ index + 3 ] ] = 1 if val_1 == val_2 else 0
			index += 4

	return diagnostic_code




if __name__ == '__main__':
	file_path = os.path.splitext( __file__ )[ 0 ] + '_input.txt'
	with open( file_path, 'r' ) as f:
		lines = f.readlines( )

		int_strs = lines[ 0 ].split( ',' )
		ints_input = [ int( x ) for x in int_strs ] # len( ) 129


	print( compute( ints_input ) ) # 13210611
	print( compute( ints_input, input_val = 5 ) ) # 584126
