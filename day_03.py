import os.path


if __name__ == '__main__':
	file_path = os.path.splitext( __file__ )[ 0 ] + '_input.txt'
	with open( file_path, 'r' ) as f:
		lines = f.readlines( )

	"""
	--- Day 3: Crossed Wires ---
	The gravity assist was successful, and you're well on your way to the Venus refuelling station. During the rush back
	on Earth, the fuel management system wasn't completely installed, so that's next on the priority list.

	Opening the front panel reveals a jumble of wires. Specifically, two wires are connected to a central port and extend
	outward on a grid. You trace the path each wire takes as it leaves the central port,
	one wire per line of text (your puzzle input).

	The wires twist and turn, but the two wires occasionally cross paths. To fix the circuit, you need to find the
	intersection point closest to the central port. Because the wires are on a grid, use the Manhattan distance for
	this measurement. While the wires do technically cross right at the central port where they both start, this point
	does not count, nor does a wire count as crossing with itself.

	For example, if the first wire's path is R8,U5,L5,D3, then starting from the central port (o),
	it goes right 8, up 5, left 5, and finally down 3:

	...........
	...........
	...........
	....+----+.
	....|....|.
	....|....|.
	....|....|.
	.........|.
	.o-------+.
	...........
	Then, if the second wire's path is U7,R6,D4,L4, it goes up 7, right 6, down 4, and left 4:

	...........
	.+-----+...
	.|.....|...
	.|..+--X-+.
	.|..|..|.|.
	.|.-X--+.|.
	.|..|....|.
	.|.......|.
	.o-------+.
	...........
	These wires cross at two locations (marked X),
	but the lower-left one is closer to the central port: its distance is 3 + 3 = 6.

	Here are a few more examples:

	R75,D30,R83,U83,L12,D49,R71,U7,L72
	U62,R66,U55,R34,D71,R55,D58,R83 = distance 159
	R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51
	U98,R91,D20,R16,D67,R40,U7,R15,U6,R7 = distance 135
	"""

	wire_path_1 = lines[ 0 ].split( ',' )
	wire_path_2 = lines[ 1 ].split( ',' )

	DIR_LEFT 	= 'L'
	DIR_RIGHT 	= 'R'
	DIR_UP 		= 'U'
	DIR_DOWN 	= 'D'


	def get_wire_points( wire_path ):
		x = 0
		y = 0

		wire_points = [ ]
		#wire_points.append( ( x, y ) )

		for i in wire_path:
			direction = i[ 0 ]
			distance = int( i[ 1: ] )

			if direction == DIR_LEFT:
				for i in range( distance ):
					x -= 1
					wire_points.append( ( x, y ) )

			elif direction == DIR_RIGHT:
				for i in range( distance ):
					x += 1
					wire_points.append( ( x, y ) )

			elif direction == DIR_UP:
				for i in range( distance ):
					y += 1
					wire_points.append( ( x, y ) )

			elif direction == DIR_DOWN:
				for i in range( distance ):
					y -= 1
					wire_points.append( ( x, y ) )

		return wire_points


	wire_points_1 = get_wire_points( wire_path_1 )
	wire_points_2 = get_wire_points( wire_path_2 )

	shared_points = set( wire_points_1 ) & set( wire_points_2 )
	shared_points_distances = { }

	for point in shared_points:
		distance = abs( point[ 0 ] ) + abs( point[ 1 ] )
		shared_points_distances[ point ] = distance

	shared_points_sorted_by_distance = sorted( list( shared_points_distances.keys( ) ), key = lambda x: shared_points_distances[ x ] )

	closests_intersection = shared_points_sorted_by_distance[ 0 ]
	distance_of_closests_intersection = abs( closests_intersection[ 0 ] ) + abs( closests_intersection[ 1 ] ) # 293

	# What is the Manhattan distance from the central port to the closest intersection?
	print( 'The Manhattan distance from the central port to the closest intersection: {0}'.format( distance_of_closests_intersection ) )


	"""
	--- Part Two ---
	It turns out that this circuit is very timing-sensitive; you actually need to minimize the signal delay.

	To do this, calculate the number of steps each wire takes to reach each intersection; choose the intersection where
	the sum of both wires' steps is lowest. If a wire visits a position on the grid multiple times, use the steps value
	from the first time it visits that position when calculating the total value of a specific intersection.

	The number of steps a wire takes is the total number of grid squares the wire has entered to get to that location,
	including the intersection being considered. Again consider the example from above:

	...........
	.+-----+...
	.|.....|...
	.|..+--X-+.
	.|..|..|.|.
	.|.-X--+.|.
	.|..|....|.
	.|.......|.
	.o-------+.
	...........
	In the above example, the intersection closest to the central port is reached after 8+5+5+2 = 20 steps by the first
	wire and 7+6+4+3 = 20 steps by the second wire for a total of 20+20 = 40 steps.

	However, the top-right intersection is better: the first wire takes only 8+5+2 = 15 and the second wire takes only
	7+6+2 = 15, a total of 15+15 = 30 steps.

	Here are the best steps for the extra examples from above:

	R75,D30,R83,U83,L12,D49,R71,U7,L72
	U62,R66,U55,R34,D71,R55,D58,R83 = 610 steps
	R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51
	U98,R91,D20,R16,D67,R40,U7,R15,U6,R7 = 410 steps
	"""

	insection_combined_steps = { }

	for point in shared_points:
		wire_insection_steps_1 = wire_points_1.index( point ) + 1
		wire_insection_steps_2 = wire_points_2.index( point ) + 1
		insection_combined_steps[ point ] = wire_insection_steps_1 + wire_insection_steps_2

	insection_combined_steps_sorted = list( insection_combined_steps.values( ) )
	insection_combined_steps_sorted.sort( )
	fewest_combined_steps_to_an_intersection = insection_combined_steps_sorted[ 0 ] # 27306

	# What is the fewest combined steps the wires must take to reach an intersection?
	print( 'The fewest combined steps the wires must take to reach an intersection: {0}'.format( fewest_combined_steps_to_an_intersection ) )
