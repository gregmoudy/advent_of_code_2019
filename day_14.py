import os.path
import math

file_path = os.path.splitext( __file__ )[ 0 ] + '_input.txt'
with open( file_path, 'r' ) as f:
	lines = f.read( ).splitlines( )


#======================================================================

KEY_OUTPUT_NUM = 'output_num'
KEY_INPUT_CHEMS = 'input_chems'

FORMULAS = { }

for line in lines:
	i, o, = line.split( '=>' )

	o = o.lstrip( ' ' )
	o = o.split( ' ' )
	o = ( int( o[ 0 ] ), o[ 1 ] )

	i = i.rstrip( ' ' )
	i = i.split( ',' )
	i = [ x.lstrip( ' ' ) for x in i ]
	i = [ x.split( ' ' ) for x in i ]
	i = [ ( y, int( x ) ) for x, y in i ]

	input_chems = { }
	for c, n in i:
		input_chems[ c ] = n

	formula_data = { KEY_OUTPUT_NUM : o[ 0 ], KEY_INPUT_CHEMS : input_chems }
	FORMULAS[ o[ 1 ] ] = formula_data


#======================================================================

ORE = 'ORE'
FUEL = 'FUEL'

CHEM_SUPPLY = { }

def create_chem( chem_code, qty = 1, ore_required = 0 ):
	global CHEM_SUPPLY

	formula_data = FORMULAS.get( chem_code )

	# Go through the input chemicals needs to produce the chemical and produce them if we don't have them already in our supply.
	input_chems = formula_data[ KEY_INPUT_CHEMS ]
	for input_chem_code, input_chem_num_required in input_chems.items( ):
		input_chem_num_required = input_chem_num_required * qty

		# Track ore required, can not be produced.
		if input_chem_code == ORE:
			ore_required += input_chem_num_required
			continue

		# Get the current supply of the input chem.
		input_chem_current_supply = CHEM_SUPPLY.get( input_chem_code, 0 )

		# If we don't have enough, then produce how much we need.
		while CHEM_SUPPLY.get( input_chem_code, 0 ) < input_chem_num_required:
			ore_required = create_chem( input_chem_code, qty = qty, ore_required = ore_required )

		# Remove the require amount from our chem supply.
		input_chem_current_supply = CHEM_SUPPLY.get( input_chem_code, 0 )
		new_supply_count = input_chem_current_supply - input_chem_num_required
		CHEM_SUPPLY[ input_chem_code ] = new_supply_count

	# Record how much of the chemical was produced.
	num_produced = formula_data[ KEY_OUTPUT_NUM ] * qty
	current_supply = CHEM_SUPPLY.get( chem_code, 0 )
	new_supply = current_supply + num_produced
	CHEM_SUPPLY[ chem_code ] = new_supply

	return ore_required



def ore_required_to_make_fuel( qty = 1 ):
	#global CHEM_SUPPLY
	#CHEM_SUPPLY = { }
	ore = create_chem( FUEL, qty = qty )
	return ore


#======================================================================


if __name__ == '__main__':
	# Part 1
	# Given the list of reactions in your puzzle input, what is the minimum amount of ORE required to produce exactly 1 FUEL?
	CHEM_SUPPLY = { }
	ore_required = create_chem( FUEL )
	print( 'Ore Required: {0}'.format( ore_required ) ) # 870051

	# Part 2
	# Given 1 trillion ORE, what is the maximum amount of FUEL you can produce?
	CHEM_SUPPLY = { }
	fuel_count = 0
	ore_supply = 1000000000000 # One trillion

	while ore_supply > 0:
		ore_required = create_chem( FUEL )
		ore_supply -= ore_required
		if ore_supply >= 0:
			fuel_count += 1

	print( 'One Trillion Ore Fuel Count: {0}'.format( fuel_count ) ) # 1863741 # THIS IS SLOWWWW


	#CHEM_SUPPLY = { }
	#oreForOne = ore_required_to_make_fuel( )
	#ORE_STORAGE = 1000000000000
	#part2 = math.ceil( ORE_STORAGE / oreForOne )
	#while True:
		#checkFuel = ore_required_to_make_fuel(part2)
		#if checkFuel <= ORE_STORAGE:
			#sizingCheck = ( ( ORE_STORAGE - checkFuel ) / oreForOne )
			#if sizingCheck > 10000:
				#part2 += 10000

			#elif sizingCheck > 1000:
				#part2 += 1000

			#elif sizingCheck > 100:
				#part2 += 100

			#elif sizingCheck > 10:
				#part2 += 10

			#else:
				#part2 += 1;

		#else:
			#part2 -= 1
			#break

	#print( checkFuel )
