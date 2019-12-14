import os.path

file_path = os.path.splitext( __file__ )[ 0 ] + '_input.txt'
with open( file_path, 'r' ) as f:
	lines = f.read( ).splitlines( )

	formulas = [ ]

	for line in lines:
		i, o, = line.split( '=>' )

		o = o.lstrip( ' ' )
		o = o.split( ' ' )
		o = ( int( o[ 0 ] ), o[ 1 ] )

		i = i.rstrip( ' ' )
		i = i.split( ',' )
		i = [ x.lstrip( ' ' ) for x in i ]
		i = [ x.split( ' ' ) for x in i ]
		i = [ ( int( x ), y ) for x, y in i ]

		formulas.append( ( i, o ) )

	# formulas ( [ (input num, input code) ], (output num, output code ) ),

	print( 'break' )

#======================================================================


#======================================================================


if __name__ == '__main__':
	print( 'break' )
