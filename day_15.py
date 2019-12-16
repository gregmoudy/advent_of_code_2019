import os.path

file_path = os.path.splitext( __file__ )[ 0 ] + '_input.txt'
with open( file_path, 'r' ) as f:
	lines = f.readlines( )
	int_strs = lines[ 0 ].split( ',' )
	INPUT_DATA = [ int( x ) for x in int_strs ]

#======================================================================


class Intcode_Computer:
	def __init__( self ):
		self.data = list( INPUT_DATA )
		self.data.extend( [ 0 ] * 10000 )
		self.idx = 0
		self.relative_base = 0
		self.inputs = [ ]
		self.output = None
		self.done = False

		self.user_input_callback_func = None


	def translate_instruction( self, instruction ):
		instruction_str = str( instruction )

		while len( instruction_str ) < 5:
			instruction_str = '0' + instruction_str

		opcode = int( instruction_str[ 3: ] )
		mode1 = int( instruction_str[ 2 ] )
		mode2 = int( instruction_str[ 1 ] )
		mode3 = int( instruction_str[ 0 ] ) # This should always be 0?

		return opcode, mode1, mode2, mode3


	def get_param( self, param_num, mode ):
		PARAM_MODE_POSITION 	= 0 # Value is an index position. A value of 50 returns the value at index 50.
		PARAM_MODE_IMMEDIATE = 1 # Value is a value. A value of 50 is returned as 50.
		PARAM_MODE_RELATIVE 	= 2 # Position value that is combined with a relative base position.

		if mode == PARAM_MODE_POSITION:
			return self.data[ self.idx + param_num ]

		elif mode == PARAM_MODE_IMMEDIATE:
			return self.idx + param_num

		elif mode == PARAM_MODE_RELATIVE:
			return self.relative_base + self.data[ self.idx + param_num ]

		raise ValueError


	def get_params(self, mode1, mode2 = None, mode3 = None):
		param1 = self.get_param( 1, mode1 )
		param2 = None
		param3 = None

		if mode2 is not None:
			param2 = self.get_param( 2, mode2 )

		if mode3 is not None:
			param3 = self.get_param( 3, mode3 )

		if param3 is not None:
			return param1, param2, param3

		if param2 is not None:
			return param1, param2

		return param1


	def compute( self ):
		OPCODE_ADD 			= 1 # Add position 2 to 3 and copy to position set in position 4.
		OPCODE_MULTIPLY	= 2 # Multiply position 2 to 3 and copy to position set in position 4.

		OPCODE_INPUT 		= 3 # Takes a single integer as input and saves it to the position given by its only parameter.
		OPCODE_OUTPUT 		= 4 # Outputs the value of its only parameter.

		OPCODE_JUMP_TRUE 	= 5 # If the first param is not a 0, the index becomes the second param value.
		OPCODE_JUMP_FALSE = 6 # If the first param is 0, the index  comes the second param value.

		OPCODE_LESS_THAN 	= 7 # If the first param is less than the second param, 1 gets stored at the target, otherwise 0.
		OPCODE_EQUALS 		= 8 # If the first param is equel to the second param, 1 gets stored at the target, otherwise 0.

		OPCODE_RB_OFFSET 	= 9 # Adjusts the relative base by the value of its only parameter.

		OPCODE_HALT 		= 99 # HALT

		while True:
			opcode, mode1, mode2, mode3 = self.translate_instruction( self.data[ self.idx ] )

			if opcode == OPCODE_ADD:
				param1, param2, param3 = self.get_params( mode1, mode2, mode3 )
				self.data[ param3 ] = self.data[ param1 ] + self.data[ param2 ]
				self.idx += 4

			elif opcode == OPCODE_MULTIPLY:
				param1, param2, param3 = self.get_params( mode1, mode2, mode3 )
				self.data[ param3 ] = self.data[ param1 ] * self.data[ param2 ]
				self.idx += 4

			elif opcode == OPCODE_INPUT:
				param1 = self.get_params( mode1 )

				if self.user_input_callback_func is not None:
					input_val = self.user_input_callback_func( )

				else:
					input_val = self.inputs.pop( 0 )

				self.data[ param1 ] = input_val
				self.idx += 2

			elif opcode == OPCODE_OUTPUT:
				param1 = self.get_params( mode1 )
				self.output = self.data[ param1 ]
				self.idx += 2
				return self.output

			elif opcode == OPCODE_JUMP_TRUE:
				param1, param2 = self.get_params( mode1, mode2 )
				self.idx = self.data[ param2 ] if self.data[ param1 ] != 0 else self.idx + 3

			elif opcode == OPCODE_JUMP_FALSE:
				param1, param2 = self.get_params( mode1, mode2 )
				self.idx = self.data[ param2 ] if self.data[ param1 ] == 0 else self.idx + 3

			elif opcode == OPCODE_LESS_THAN:
				param1, param2, param3 = self.get_params( mode1, mode2, mode3 )
				self.data[ param3 ] = 1 if self.data[ param1 ] < self.data[ param2 ] else 0
				self.idx += 4

			elif opcode == OPCODE_EQUALS:
				param1, param2, param3 = self.get_params( mode1, mode2, mode3 )
				self.data[ param3 ] = 1 if self.data[ param1 ] == self.data[ param2 ] else 0
				self.idx += 4

			elif opcode == OPCODE_RB_OFFSET:
				param1 = self.get_params( mode1 )
				self.relative_base += self.data[ param1 ]
				self.idx += 2

			elif opcode == OPCODE_HALT:
				self.done = True
				return self.output


#======================================================================

NORTH = 1
SOUTH = 1
WEST 	= 3
EAST 	= 4

MAP_DROID 	= 'D'
MAP_EMPTY 	= '.'
MAP_WALL 	= '#'
MAP_O2 		= 'O'


#Accept a movement command via an input instruction.
#Send the movement command to the repair droid.
#Wait for the repair droid to finish the movement operation.
#Report on the status of the repair droid via an output instruction.

class Repair_Droid:
	def __init__( self ):
		self.computer = Intcode_Computer( )
		self.computer.user_input_callback_func = self.get_movement_input

		self.position = ( 0, 0 )

		self.planned_movement = NORTH
		self.direction = ( 0, 1 )

		self.map_data = { self.position : MAP_EMPTY }


	@property
	def planned_position( self ):
		return ( self.position[ 0 ] + self.direction[ 0 ], self.position[ 1 ] + self.direction[ 1 ] )


	def move_north( self ):
		self.planned_movement = NORTH
		self.direction = ( 0, 1 )


	def move_south( self ):
		self.planned_movement = SOUTH
		self.direction = ( 0, -1 )


	def move_west( self ):
		self.planned_movement = WEST
		self.direction = ( -1, 0 )


	def move_east( self ):
		self.planned_movement = EAST
		self.direction = ( 0, 1 )


	def get_movement_input( self ):
		return self.planned_movement


	def process_output( self, status ):
		STATUS_WALL_HIT 		= 0 # Position not changed.
		STATUS_MOVED 			= 1
		STATUS_MOVED_AT_O2 	= 2

		if status == STATUS_WALL_HIT:
			self.map_data[ self.planned_position ] = MAP_WALL
			self.move_east( )

		elif status == STATUS_MOVED:
			self.map_data[ self.planned_position ] = MAP_EMPTY
			self.position = self.planned_position

		elif status == STATUS_MOVED_AT_O2:
			self.map_data[ self.planned_position ] = MAP_O2
			self.computer.done = True

			# TODO: PRINT MAP???
			return


	def run( self ):
		while self.computer.done is False:
			output = self.computer.compute( )
			self.process_output( output )


#======================================================================


if __name__ == '__main__':
	droid = Repair_Droid( )
	droid.run( )
