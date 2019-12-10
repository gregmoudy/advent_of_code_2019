import os.path
import math

file_path = os.path.splitext( __file__ )[ 0 ] + '_input.txt'
with open( file_path, 'r' ) as f:
	lines = f.read().splitlines()

#======================================================================
ASTEROID_MAP = list( lines )
X_MAX = len( ASTEROID_MAP[ 0 ] ) - 1
Y_MAX = len( ASTEROID_MAP ) - 1

OBJ_EMPTY = '.'
OBJ_ASTEROID = '#'


def location_lookup( x, y ):
	if x < 0 or x > X_MAX or y < 0 or y > Y_MAX:
		raise ValueError

	return ASTEROID_MAP[ y ][ x ]


def atan3( x, y ):
	ang = math.atan2( x, y )
	# atan2 wraps around from +pi to -pi
	# we'd rather it wrapped from 2pi to 0
	if ang < 0:
		ang += 2 * math.pi
	# atan2 goes counterclockwise
	# lets reverse that
	# 0 is a special case
	if ang != 0:
		ang = 2 * math.pi - ang

	return ang


def destroy_n_asteroids( asteroid_locations, station_location, n ):
	if n < 1 or n > len( asteroid_locations ):
		raise ValueError

	asteroid_locations = set( asteroid_locations ) # Dupe so we can modify.
	asteroid_locations.remove( station_location ) # Remove the station location.

	station_x, station_y = station_location

	# TODO: I need to walk through this math to understand it better.
	count = 0
	last_angle = -1e-100
	while count < n:
		count += 1
		nuked_x = None
		nuked_y = None
		nuked_dist = 1e99
		angle = 10
		for asteroid_x, asteroid_y in asteroid_locations:
			ang = atan3( station_x - asteroid_x, station_y - asteroid_y )
			if ang > last_angle:
				dist = ( asteroid_x - station_x ) **2 + ( asteroid_y - station_y ) **2
				if ang < angle or ( ang == angle and dist < nuked_dist ):
					nuked_x = asteroid_x
					nuked_y = asteroid_y
					nuked_dist = dist
					angle = ang

		if angle == 10:
			last_angle = -1e-100
			count -= 1
			continue

		asteroid_locations.remove( ( nuked_x, nuked_y ) )
		last_angle = angle

	return ( nuked_x, nuked_y )


def find_best_station_location( asteroid_locations ):
	detectable_asteroids_and_location = [ ]

	# Go to each asteroid location.
	for x, y in asteroid_locations:
		# Find the scan angle to each asteroid and collect a set of the unique angles.
		detected_asteroid_angles = set( )
		for asteroid_x, asteroid_y in asteroid_locations:
			angle_to_asteroid = math.atan2( asteroid_x - x, asteroid_y - y )
			detected_asteroid_angles.add( angle_to_asteroid )

		# Record the the number of scanable asteroids and the location of scan.
		detectable_asteroids = len( detected_asteroid_angles )
		detectable_asteroids_and_location.append( ( detectable_asteroids, x, y ) )

	# Get the entry with the most detectable asteroids and return the value and location.
	number_of_asteroids_detectable, station_x, station_y = max( detectable_asteroids_and_location )

	return number_of_asteroids_detectable, station_x, station_y


#======================================================================


if __name__ == '__main__':
	# Collect the locations of all the asteroids on the map.
	asteroid_locations = set( )
	for x in range( 0, X_MAX + 1 ):
		for y in range( 0, Y_MAX + 1 ):
			obj = location_lookup( x, y )
			if obj == OBJ_ASTEROID:
				asteroid_locations.add( ( x, y ) )

	# Part 1
	number_of_asteroids_detectable, station_x, station_y = find_best_station_location( asteroid_locations )
	station_location = ( station_x, station_y )

	print( 'Best location for a new monitoring station: {0}.'.format( station_location ) ) # 20, 20
	print( '{0} asteroids can be detected from this location.'.format( number_of_asteroids_detectable ) ) # 292

	# Part 2
	final_location = destroy_n_asteroids( asteroid_locations, station_location, 200 )
	final_val = ( final_location[ 0 ] * 100 ) + final_location[ 1 ]
	print( 'Location value of 200th asteroid destruction: {0}'.format( final_val ) ) # 317
