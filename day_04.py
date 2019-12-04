import os.path
import re


DOUBLES_REGEX_STRING = r'(.)\1+'


def has_double( password ):
	return re.search( DOUBLES_REGEX_STRING, str( password ) ) is not None



def increments( password ):
	password_nums = [ int( x ) for x in str( password ) ]

	previous_num = password_nums[ 0 ]
	for i in range( 1, len( password_nums ) ):
		current_num = password_nums[ i ]
		if current_num < previous_num:
			return False

		previous_num = current_num

	return True



def double_isolated( password ):
	doubles_search_pattern = re.compile( DOUBLES_REGEX_STRING )
	for match in doubles_search_pattern.finditer( str( password ) ):
		if len( match.group( ) ) == 2:
			return True

	return False



if __name__ == '__main__':
	file_path = os.path.splitext( __file__ )[ 0 ] + '_input.txt'
	with open( file_path, 'r' ) as f:
		lines = f.readlines( )

	"""
	--- Day 4: Secure Container ---
	You arrive at the Venus fuel depot only to discover it's protected by a password. The Elves had written the password
	on a sticky note, but someone threw it out.

	However, they do remember a few key facts about the password:

	It is a six-digit number.
	The value is within the range given in your puzzle input.
	Two adjacent digits are the same (like 22 in 122345).
	Going from left to right, the digits never decrease; they only ever increase or stay the same (like 111123 or 135679).
	Other than the range rule, the following are true:

	111111 meets these criteria (double 11, never decreases).
	223450 does not meet these criteria (decreasing pair of digits 50).
	123789 does not meet these criteria (no double).

	How many different passwords within the range given in your puzzle input meet these criteria?
	"""

	# Process Input
	puzzle_input = lines[ 0 ].split( '-' )
	puzzle_input = [ int( x ) for x in puzzle_input ]

	range_min = puzzle_input[ 0 ] + 1
	range_max = puzzle_input[ 1 ] - 1

	# Generate Passwords
	passwords = list( range( range_min, range_max + 1 ) )

	# Validate Passwords Part 1
	passwords_with_doubles = [ x for x in passwords if has_double( x ) ]
	valid_passwords_part_1 = [ x for x in passwords_with_doubles if increments( x ) ]

	print( 'Number of valid passwords: {0}'.format( len( valid_passwords_part_1 ) ) ) # 2090


	"""
	--- Part Two ---
	An Elf just remembered one more important detail: the two adjacent matching digits are not part of a larger group of
	matching digits.

	Given this additional criterion, but still ignoring the range rule, the following are now true:

	112233 meets these criteria because the digits never decrease and all repeated digits are exactly two digits long.
	123444 no longer meets the criteria (the repeated 44 is part of a larger group of 444).
	111122 meets the criteria (even though 1 is repeated more than twice, it still contains a double 22).

	How many different passwords within the range given in your puzzle input meet all of the criteria?
	"""

	# Validate Passwords Part 2
	valid_passwords_part_2 = [ x for x in valid_passwords_part_1 if double_isolated( x ) ]

	print( 'Number of valid passwords part 2: {0}'.format( len( valid_passwords_part_2 ) ) ) # 1419
