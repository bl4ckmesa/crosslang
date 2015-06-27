#! /usr/bin/env python

import os,sys
import random
import textwrap

if len(sys.argv) < 2:
	print "Insufficient arguments."
	sys.exit(1)

gridsize = 5
wordcount = 10
filename = sys.argv[1]
wordlist = [line.rstrip('\n').upper().split(',') for line in open(filename, 'r').readlines()]

def print_cube(wordgrid):
	cube = ""
	for square in wordgrid:
		for key in square:
			if square[key] == "":
				cube += "-"
			else:
				cube += square[key]
	
	for line in textwrap.wrap(cube,gridsize):
		print line

def get_words(wordlist):
	words = { 'chars': {}, 'words': [] }
	random.shuffle(wordlist)
	for word, meaning in wordlist:
		if len(words['words']) == wordcount: break
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
def free_adjacent(wordgrid,next_letter,prev_letter = []):
	# Get grid adjacent to prev_letter
	prev_c, prev_p = prev_letter
	upleft = prev_p + gridsize - 1
	up = prev_p + gridsize
	upright = prev_p + gridsize + 1
	left = prev_p - 1
	right = prev_p + 1
	downleft = prev_p - gridsize - 1
	down = prev_p - gridsize
	downright = prev_p - gridsize + 1
	adjacent = [upleft,up,upright,left,right,downleft,down,downright]
	available = []
	for square in adjacent:
		if 0 <= square <= gridsize ** 2:
			available.append(square)

	# See if next_letter is already in a grid there
	for square in available:
		print wordgrid[square]

	# If not, pick randomly among them.

	print ""

def trace_words(_words,gridsize):
	# Try to trace all the letters of all the words a grid
	common_letters = [ 'E', 'S', 'N', 'T', 'A', 'O' ]
	grid = []
	for n in range(1, (gridsize ** 2) + 1):
		grid.append({ n: '' })
	inner_grid = []
	for square in grid:
		sq = int(square.keys()[0])
		# Add inner grid numbers
		if gridsize < sq < ((gridsize ** 2) - gridsize) and not sq % gridsize in [ 0, 1, gridsize ]:
			inner_grid.append(sq)
	prev_letter = [] # Will be letter and position in grid (i.e., [ 'a', 5 ]
	for word in _words:
		wordgrid = list(grid)
		# Go letter by letter.
		for c in word[0]:
			# Start somewhere on the grid
			if not prev_letter:
				# First time letter
				print "First word:", word
				coord = random.choice(wordgrid).keys()[0]
			else:
				# Everything else
				# coord = free_adjacent(wordgrid,c,prev_letter)
				coord = free_adjacent(wordgrid,c,prev_letter)
			prev_letter = [ c, coord ]
			wordgrid[coord - 1][coord] = c
		grid = wordgrid
		print "\n\n> %s <" % c
		print_cube(grid)
	return grid

words = get_words(wordlist)
wordgrid = trace_words(words['words'],gridsize)


print_cube(wordgrid)

for word in words['words']:
	print word[0]
