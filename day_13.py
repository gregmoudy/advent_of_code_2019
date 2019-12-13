import os.path
import time

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

TILE_EMPTY 	= 0
TILE_WALL 	= 1
TILE_BLOCK 	= 2
TILE_PADDLE = 3
TILE_BALL 	= 4

LEFT 		= -1
NEUTRAL 	= 0
RIGHT 	= 1


class Arcade:
	def __init__( self, quarters = None ):
		self.computer = Intcode_Computer( )
		self.computer.user_input_callback_func = self.get_user_input
		self.screen = { }
		self.score = 0

		if quarters:
			self.computer.data[ 0 ] = quarters


	def run( self ):
		while self.computer.done is False:
			x = self.computer.compute( )
			y = self.computer.compute( )
			output_3 = self.computer.compute( )

			if x == -1 and y == 0:
				self.score = output_3

			else:
				self.screen[ ( x, y ) ] = output_3

		self.draw_score( )


	def get_tile_count( self, tile_id ):
		return len( [ x for x in self.screen.values( ) if x == tile_id ] )


	def get_tile_pos( self, lookup_tile_id ):
		for pos in self.screen:
			tile_id = self.screen[ pos ]
			if tile_id == lookup_tile_id:
				return pos


	def draw_screen( self ):
		x_max = max( [ x[ 0 ] for x in self.screen.keys( ) ] )
		y_max = max( [ x[ 1 ] for x in self.screen.keys( ) ] )

		for y in range( y_max + 1 ):
			line = ''
			for x in range( x_max + 1 ):
				tile_id = self.screen.setdefault( ( x, y ), TILE_EMPTY )

				if tile_id == TILE_WALL:
					tile = '|'

				elif tile_id == TILE_BLOCK:
					tile = 'X'

				elif tile_id == TILE_PADDLE:
					tile = '-'

				elif tile_id == TILE_BALL:
					tile = 'o'

				else:
					tile = ' '

				line += tile

			print( line )

		self.draw_score( )


	def draw_score( self ):
		print( 'Current Score: {0}'.format( self.score ) )


	def get_user_input( self ):
		self.draw_screen( )
		#time.sleep( 0.001 )

		ball_pos = self.get_tile_pos( TILE_BALL )
		paddle_pos = self.get_tile_pos( TILE_PADDLE )

		if ball_pos[ 0 ] < paddle_pos[ 0 ]:
			joystick_val = LEFT

		elif ball_pos[ 0 ] > paddle_pos[ 0 ]:
			joystick_val = RIGHT

		else:
			joystick_val = NEUTRAL

		return joystick_val


#======================================================================


if __name__ == '__main__':

	# Part 1
	arcade = Arcade( )

	# How many block tiles are on the screen when the game exits?
	arcade.run( )
	block_count = arcade.get_tile_count( TILE_BLOCK )
	print( 'Number of block tiles: {0}'.format( block_count ) ) # 361

	# Part 2
	arcade = Arcade( quarters = 2 )

	# What is your score after the last block is broken?
	arcade.run( ) # 17590
