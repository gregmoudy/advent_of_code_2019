import os.path

#======================================================================

file_path = os.path.splitext( __file__ )[ 0 ] + '_input.txt'
with open( file_path, 'r' ) as f:
	IMAGE_DATA = f.readlines( )[ 0 ].rstrip( '\n' )

#======================================================================




if __name__ == '__main__':
	image_data = str( IMAGE_DATA )

	BLACK = '0'
	WHITE = '1'
	TRANS = '2'

	width = 25
	height = 6
	pixels_per_layer = width * height

	layers = [ image_data[ i:i+pixels_per_layer ] for i in range( 0, len( image_data ), pixels_per_layer ) ]

	# Part 1
	lowest_0_layer = layers[ 0 ]
	for layer in layers:
		if layer.count( '0' ) < lowest_0_layer.count( '0' ):
			lowest_0_layer = layer

	answer = lowest_0_layer.count( '1' ) * lowest_0_layer.count( '2' )
	print( answer ) #1088

	# Part 2
	layers_merged = ''

	for pixel_idx in range( 0, pixels_per_layer ):
		for layer in layers:
			color = layer[ pixel_idx ]
			if color in [ BLACK, WHITE ]:
				if color == BLACK:
					color = ' '

				layers_merged += color
				break

	rows = [ layers_merged[ i:i+width ] for i in range( 0, len( layers_merged ), width ) ]
	for row in rows:
		print( row ) # LGYHB
