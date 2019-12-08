import os.path
import itertools


#======================================================================

file_path = os.path.splitext( __file__ )[ 0 ] + '_input.txt'
with open( file_path, 'r' ) as f:
	lines = f.readlines( )
	int_strs = lines[ 0 ].split( ',' )
	INPUT_DATA = [ int( x ) for x in int_strs ]

#======================================================================


class Intcode_Computer:
	def __init__( self ):
		self.data = list( INPUT_DATA )
		self.index = 0
		self.inputs = [ ]
		self.output = None
		self.done = False


	@ staticmethod
	def translate_instruction( instruction ):
		instruction_str = str( instruction )

		while len( instruction_str ) < 5:
			instruction_str = '0' + instruction_str

		opcode = int( instruction_str[ 3: ] )
		mode_1 = int( instruction_str[ 2 ] )
		mode_2 = int( instruction_str[ 1 ] )
		mode_3 = int( instruction_str[ 0 ] ) # This should always be 0?

		return opcode, mode_1, mode_2, mode_3


	@staticmethod
	def get_param_val( data, index, mode ):
		PARAM_MODE_POSITION 	= 0 # Value is an index position. A value of 50 returns the value at index 50.
		PARAM_MODE_IMMEDIATE = 1 # Value is a value. A value of 50 is returned as 50.

		# Mode Position
		if mode == PARAM_MODE_POSITION:
			return data[ data[ index ] ]

		# Mode Immediate
		return data[ index ]


	def get_param_vals( self, data, index, mode_1, mode_2 ):
		val_1 = self.get_param_val( data, index + 1, mode_1 )
		val_2 = self.get_param_val( data, index + 2, mode_2 )

		return val_1, val_2


	def compute( self ):
		OPCODE_ADD 			= 1 # Add position 2 to 3 and copy to position set in position 4.
		OPCODE_MULTIPLY	= 2 # Multiply position 2 to 3 and copy to position set in position 4.

		OPCODE_INPUT 		= 3 # Takes a single integer as input and saves it to the position given by its only parameter.
		OPCODE_OUTPUT 		= 4 # Outputs the value of its only parameter.

		OPCODE_JUMP_TRUE 	= 5 # If the first param is not a 0, the index becomes the second param value.
		OPCODE_JUMP_FALSE = 6 # If the first param is 0, the index  comes the second param value.

		OPCODE_LESS_THAN 	= 7 # If the first param is less than the second param, 1 gets stored at the target, otherwise 0.
		OPCODE_EQUALS 		= 8 # If the first param is equel to the second param, 1 gets stored at the target, otherwise 0.

		OPCODE_HALT 		= 99 # HALT

		while True:
			opcode, mode_1, mode_2, mode_3 = self.translate_instruction( self.data[ self.index ] )

			if opcode == OPCODE_ADD:
				val_1, val_2 = self.get_param_vals( self.data, self.index, mode_1, mode_2 )
				self.data[ self.data[ self.index + 3 ] ] = val_1 + val_2
				self.index += 4

			elif opcode == OPCODE_MULTIPLY:
				val_1, val_2 = self.get_param_vals( self.data, self.index, mode_1, mode_2 )
				self.data[ self.data[ self.index + 3 ] ] = val_1 * val_2
				self.index += 4

			elif opcode == OPCODE_INPUT:
				self.data[ self.data[ self.index + 1] ] = self.inputs.pop( 0 )
				self.index += 2

			elif opcode == OPCODE_OUTPUT:
				self.output = self.data[ self.data[ self.index + 1 ] ]
				self.index += 2
				return self.output

			elif opcode == OPCODE_JUMP_TRUE:
				val_1, val_2 = self.get_param_vals( self.data, self.index, mode_1, mode_2 )
				self.index = val_2 if val_1 != 0 else self.index + 3

			elif opcode == OPCODE_JUMP_FALSE:
				val_1, val_2 = self.get_param_vals( self.data, self.index, mode_1, mode_2 )
				self.index = val_2 if val_1 == 0 else self.index + 3

			elif opcode == OPCODE_LESS_THAN:
				val_1, val_2 = self.get_param_vals( self.data, self.index, mode_1, mode_2 )
				self.data[ self.data[ self.index + 3 ] ] = 1 if val_1 < val_2 else 0
				self.index += 4

			elif opcode == OPCODE_EQUALS:
				val_1, val_2 = self.get_param_vals( self.data, self.index, mode_1, mode_2 )
				self.data[ self.data[ self.index + 3 ] ] = 1 if val_1 == val_2 else 0
				self.index += 4

			elif opcode == OPCODE_HALT:
				self.done = True
				return self.output


#======================================================================


def calc_max_thruster_signal( amp_phase_min, amp_phase_max, feedback_loop = False ):
	thruster_signals = [ ]

	for amp_phases in itertools.permutations( range( amp_phase_min, amp_phase_max + 1 ) ):
		computers = [ ]
		for amp_phase in amp_phases:
			computer = Intcode_Computer( )
			computer.inputs.append( amp_phase )
			computers.append( computer )

		output = 0
		while computers[ -1 ].done == False:
			for computer in computers:
				computer.inputs.append( output )
				output = computer.compute( )

			if not feedback_loop:
				break

		thruster_signals.append( output )

	return max( thruster_signals )



if __name__ == '__main__':
	# Part 1
	max_thruster_signal = calc_max_thruster_signal( 0, 4 )
	print( max_thruster_signal ) # 46248

	# Part 2
	max_thruster_signal = calc_max_thruster_signal( 5, 9, feedback_loop = True )
	print( max_thruster_signal ) # 54163586
