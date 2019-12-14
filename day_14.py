import os.path

file_path = os.path.splitext( __file__ )[ 0 ] + '_input.txt'
with open( file_path, 'r' ) as f:
	lines = f.readlines( )
	print( 'break' )

#======================================================================


#======================================================================


if __name__ == '__main__':
	print( 'break' )
