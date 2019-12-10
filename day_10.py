import os.path

file_path = os.path.splitext( __file__ )[ 0 ] + '_input.txt'
with open( file_path, 'r' ) as f:
	lines = f.read().splitlines()

#======================================================================
ASTEROID_MAP = list( lines )
X_MAX = len( ASTEROID_MAP[ 0 ] ) - 1
Y_MAX = len( ASTEROID_MAP ) - 1

LOC_EMPTY = '.'
LOC_ASTEROID = '#'


def location_lookup( x, y ):
	if x < 0 or x > X_MAX or y < 0 or y > Y_MAX:
		raise ValueError

	return ASTEROID_MAP[ y ][ x ]


#======================================================================


if __name__ == '__main__':
	print( 'break' )
