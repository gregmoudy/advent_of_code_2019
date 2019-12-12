import os.path
import math

file_path = os.path.splitext( __file__ )[ 0 ] + '_input.txt'
with open( file_path, 'r' ) as f:
	lines = f.read( ).splitlines( )


def translate_input( line ):
	remove = '<> =xyz'
	for c in remove:
		line = line.replace( c, '' )

	strs = line.split( ',' )
	pos = [ int( x ) for x in strs ]

	return pos

#======================================================================

POS_LEN = 3

class Moon:
	def __init__( self, pos ):
		self.pos = pos
		self.vel = [ 0, 0, 0 ]


	def update_position( self ):
		# Apply the velocity as an offset to the position to get the new position.
		for i in range( POS_LEN ):
			self.pos[ i ] += self.vel[ i ]


	def get_total_energy(self):
		potential_energy = sum( map( abs, self.pos ) )
		kinetic_energy = sum( map( abs, self.vel ) )
		total_energy = potential_energy * kinetic_energy

		return total_energy


#======================================================================

def create_moons( ):
	moons = [ ]
	for line in lines:
		pos = translate_input( line )
		moon = Moon( pos )
		moons.append( moon )

	return moons



def simulate_motion( moons ):
	# Update the velocity of every moon by applying gravity.
	for moon in moons:
		other_moons = list( moons )
		other_moons.pop( moons.index( moon ) )

		for other_moon in other_moons:
			new_vel = [ ]
			for pos_axis, other_pos_axis, vel_axis in zip( moon.pos, other_moon.pos, moon.vel ):

				if pos_axis < other_pos_axis:
					vel_offset = 1

				elif pos_axis > other_pos_axis:
					vel_offset = -1

				else:
					vel_offset = 0

				new_vel.append( vel_axis + vel_offset )

			moon.vel = new_vel


	# Update the position of every moon by applying velocity.
	for moon in moons:
		moon.update_position( )



def calculate_system_energy( moons ):
	moon_energies = [ ]
	for moon in moons:
		total_energy = moon.get_total_energy( )
		moon_energies.append( total_energy )

	system_energy = sum( moon_energies )

	return system_energy



def lcm( a, b ):
	return int( abs( a * b ) / math.gcd( a, b ) )



def get_axis_vals( moons ):
	axis_vals = [ [ m.pos[ i ] for m in moons ] for i in range( POS_LEN ) ]
	return axis_vals


#======================================================================


if __name__ == '__main__':
	#moons = [
		#{ POS : [ -1, 0, 2 ], VEL : [ 0, 0, 0 ] },
		#{ POS : [ 2, -10, -7 ], VEL : [ 0, 0, 0 ] },
		#{ POS : [ 4, -8, 8 ], VEL : [ 0, 0, 0 ] },
		#{ POS : [ 3, 5, -1 ], VEL : [ 0, 0, 0 ] },
	#]

	# Part 1
	# What is the total energy in the system after simulating the moons given in your scan for 1000 steps?
	moons = create_moons( )

	for steps in range( 0, 1000 ):
		simulate_motion( moons )

	# Calculate total energy in the system.
	system_energy = calculate_system_energy( moons )
	print( system_energy ) # 8362


	# Part 2 # 478373365921244
	# TOO SLOW
	#moons = create_moons( )

	#moons_snapshots = [ ]
	#moons_snapshots.append( str( moons ) )

	#step = 0
	#while True:
		#simulate_motion( moons )
		#step += 1

		#moons_snapshot = str( moons )
		#if moons_snapshot in moons_snapshots:
			#print( 'Steps: {0}'.format( step ) )
			#break

		#moons_snapshots.append( moons_snapshot )


	# TODO: Break down why this works.
	moons = create_moons( )
	initial_axis_vals = get_axis_vals( moons )

	res = [ 0, 0, 0 ]
	steps = 1
	while not all( res ):
		simulate_motion( moons )
		current_axis_vals = get_axis_vals( moons )
		steps += 1

		for i in range( POS_LEN ):
			if current_axis_vals[ i ] == initial_axis_vals[ i ] and not res[ i ]:
				res[ i ] = steps

	val = int( lcm( lcm( res[ 0 ], res[ 1 ] ), res[ 2 ] ) )
	print( val )
