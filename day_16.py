import os.path

file_path = os.path.splitext( __file__ )[ 0 ] + '_input.txt'
with open( file_path, 'r' ) as f:
	lines = f.read( ).splitlines( )
	nums = [ int( x ) for x in lines[ 0 ] ]

	print('break')

#======================================================================


#======================================================================


if __name__ == '__main__':
	print( 'break' )
