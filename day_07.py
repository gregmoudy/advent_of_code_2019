import os.path


class Planet:
	def __init__( self, name ):
		self.name = name
		self.parent = None
		self.children = [ ]


	def __repr__( self ):
		return 'Planet<{0}>'.format( self.name )


	def parent_to( self, parent ):
		self.parent = parent
		self.parent.add_child( self )


	def add_child( self, child ):
		if child not in self.children:
			self.children.append( child )


	def get_indirect_parents( self ):
		indirect_parents = [ ]

		if self.parent is not None:
			parent = self.parent.parent

			while parent is not None:
				indirect_parents.append( parent )
				parent = parent.parent

		return indirect_parents



if __name__ == '__main__':
	file_path = os.path.splitext( __file__ )[ 0 ] + '_input.txt'
	with open( file_path, 'r' ) as f:
		lines = f.read( ).splitlines( )

	# Create planet orbit object data.
	orbits = lines
	planets = { }

	for orbit in orbits:
		parent_name, child_name = orbit.split( ')' )

		parent = planets.setdefault( parent_name, Planet( parent_name ) )
		child = planets.setdefault( child_name, Planet( child_name ) )
		child.parent_to( parent )


	# Part 1
	direct_orbits = 0
	indirect_orbits = 0

	for planet_name in planets:
		planet = planets[ planet_name ]

		if planet.parent is not None:
			direct_orbits += 1

		indirect_parents = planet.get_indirect_parents( )
		indirect_orbits += len( indirect_parents )

	total_orbits = direct_orbits + indirect_orbits
	print( 'Total Direct Orbits: {0}'.format( direct_orbits ) )
	print( 'Total Indirect Orbits: {0}'.format( indirect_orbits ) )
	print( 'Total Orbits: {0}'.format( total_orbits ) )


	# Part 2
	you_indirect_parents = planets[ 'YOU' ].get_indirect_parents( )
	santa_indirect_parents = planets[ 'SAN' ].get_indirect_parents( )

	for parent in you_indirect_parents:
		if parent in santa_indirect_parents:
			you_idx = you_indirect_parents.index( parent )
			you_jumps = len( you_indirect_parents[ :you_idx + 1 ] )

			san_idx = santa_indirect_parents.index( parent )
			san_jumps = len( santa_indirect_parents[ :san_idx + 1 ] )

			orbital_transfers = you_jumps + san_jumps
			break

	print( 'Orbital Transfers: {0}'.format( orbital_transfers ) )
