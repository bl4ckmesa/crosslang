#! /usr/bin/env python

import os,sys
import random
import textwrap
import logging
import re
import copy
from logging import debug
from logging import info

if len(sys.argv) < 2:
	print "Insufficient arguments."
	sys.exit(1)

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

gridsize = 4
wordcount = 10
filename = sys.argv[1]
wordlist = [ re.sub(r'[^a-zA-Z,]','',line.rstrip('\n').upper()).split(',',1) for line in open(filename, 'r').readlines() ]
finallist = []

def print_cube(wordgrid):
	cube = ""
	for square in wordgrid:
		for key in square:
			if square[key] == "":
				cube += "-" + " "
			else:
				cube += square[key] + " "
	
	for line in textwrap.wrap(cube,gridsize * 2):
		print '\n', line
	print '\n'

def get_words(wordlist):
	words = { 'chars': {}, 'words': [] }
	random.shuffle(wordlist)
	for word, meaning in wordlist:
		if len(words['words']) == wordcount * 100: break
		words['words'].append([ word, meaning ])
		# Get stats for characters
		for c in word:
			# Get count for #n instances in string
			ccount = word.count(c)
			# Kick out if the next character is going to put us over the grid limit.
			if c in words['chars'].keys():
				if ccount > words['chars'][c]:
					if sum(words['chars'].values()) + ccount > gridsize ** 2:
						words['words'].pop(-1)
						break
					words['chars'][c] = ccount
			else:
				if sum(words['chars'].values()) + ccount > gridsize ** 2:
					words['words'].pop(-1)
					break
				words['chars'][c] = ccount
	return words

# Analyzes grid and returns a random adjacent square
def free_adjacent(wordgrid,next_letter,prev_letters = []):
	# Get grid adjacent to prev_letters
	if len(prev_letters) > 0:
		prev_c, prev_p = prev_letters[-1]
	else:
		# We're on a new word; just pick a random available one
		empty_squares = []
		for square in wordgrid:
			for key in square:
				if square[key] == "-" or square[key] == next_letter:
					empty_squares.append(key)
		if len(empty_squares) > 0:
			debug("Picking randomly from: %s" % str(empty_squares))
			return random.choice(empty_squares)
		else:
			debug("Couldn't find any space in: %s" % str(empty_squares))
			return None

	# Get adjacent square values
	upleft = prev_p + gridsize - 1
	up = prev_p + gridsize
	upright = prev_p + gridsize + 1
	left = prev_p - 1
	right = prev_p + 1
	downleft = prev_p - gridsize - 1
	down = prev_p - gridsize
	downright = prev_p - gridsize + 1

	# Now only use values that are valid
	# On the left side
	if prev_p % gridsize == 1:
		adjacent = [up,upright,right,down,downright]
	# On the right side
	elif prev_p % gridsize == 0:
		adjacent = [upleft,up,left,downleft,down]
	# Somewhere in the middle
	else:
		adjacent = [upleft,up,upright,left,right,downleft,down,downright]
	# Remove top or bottom if they are out of bounds
	adj = []
	debug("Adjacent: %s" % str(adjacent))
	for square in adjacent:
		# Make sure the square is valid for the grid
		if 0 <= square <= gridsize ** 2:
			adj.append(square)
	adjacent = adj

	debug("Prev_letter was: %s" % prev_letters[-1])
	debug("Adjacent: %s" % str(adjacent))
	# See if next_letter is already in a grid there; if it is, use it.
	current_grid_coords = (x[1] for x in prev_letters)
	for square in adjacent:
		for key in wordgrid[square - 1]:
			if wordgrid[key - 1][key] == next_letter:
				if key in current_grid_coords:
					debug("Grid %s has a %s but is already part of the word." % (key,next_letter))
				else:
					debug("%s was already at %s" % (next_letter, key))
					return key

	# If not, pick randomly among them.
	for square in adjacent:
		for key in wordgrid[square - 1]:
			if wordgrid[key - 1][key] == "-":
				debug("Found life in grid %s" % str(key))
				return key

	debug("Could not find a place for letter %s close to %s" % (next_letter, prev_c))
	return None


def trace_words(_words,gridsize):
	# Try to trace all the letters of all the words a grid
	grid = []
	for n in range(1, (gridsize ** 2) + 1):
		grid.append({ n: '-' })
	inner_grid = []
	for square in grid:
		sq = int(square.keys()[0])
		# Add inner grid numbers
		if gridsize < sq < ((gridsize ** 2) - gridsize) and not sq % gridsize in [ 0, 1, gridsize ]:
			inner_grid.append(sq)
	prev_letters = [] # Will be letter and position in grid (i.e., [ 'a', 5 ]
	for word in _words:
		coord = None
		retries = 0
		retries_max = 100
		while coord == None and retries < retries_max:
			skipword = False
			subword = []
			debug("\nWord: %s", str(word))
			wordgrid = copy.deepcopy(grid)
			# Go letter by letter.
			for c in word[0]:
				# Start somewhere on the grid
				if not prev_letters:
					# First time letter
					coord = free_adjacent(wordgrid,c)
				else:
					# Everything else
					coord = free_adjacent(wordgrid,c,prev_letters)
				if coord == None:
					skipword = True
					break
				prev_letters.append([ c, coord ])
				wordgrid[coord - 1][coord] = c
				debug("> %s <" % c)
				#print_cube(wordgrid)

			debug("Original cube pre %s looks like this:" % word)
			#print_cube(grid)

			if skipword:
				debug("Couldn't fit word in... Tried %s times." % retries)
				wordgrid = grid
				debug("> %s < - Failed; reverted wordgrid" % word[0])
				#print_cube(grid)
				retries += 1
				if retries == retries_max:
					debug("Couldn't fit word %s in... Tried %s times." % (word,retries))
			else:
				finallist.append(word)
				grid = wordgrid
				info("Successfully fit word %s in... Tried %s times." % (word,retries))
				debug("> %s < - Completed Successfully" % word[0])
				#print_cube(grid)
				# Break out now if the wordlist is at the right length
				if len(finallist) >= wordcount:
					return grid
			prev_letters = []
	return grid

common_letters = [ 'E', 'S', 'N', 'T', 'A', 'O' ]
words = get_words(wordlist)
wordgrid = trace_words(words['words'],gridsize)

# Fill in the last few unused squares with a random letter
# alphabet = [ 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z' ]
# Generate alphabet from word list
alphabet = ""
for word in words['words']:
	alphabet = "".join(set(word[0]+alphabet))

for square in wordgrid:
	for key in square:
		if square[key] == "-":
			square[key] = random.choice(alphabet)

print_cube(wordgrid)
for word in finallist:
	print word[1]
