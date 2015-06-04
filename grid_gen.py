#! /usr/bin/env python

import os,sys
import random

if len(sys.argv) < 2:
	print "Insufficient arguments."
	sys.exit(1)

gridsize = 5
wordcount = 10
filename = sys.argv[1]
wordlist = [line.rstrip('\n').upper().split(',') for line in open(filename, 'r').readlines()]

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

def trace_words(_words,gridsize):
	# Try to trace all the letters of all the words a grid
	common_letters = [ 'E', 'S', 'N', 'T', 'A', 'O' ]
	grid = []
	for n in range(1, gridsize ** 2):
		grid.append({ n: '' })
	inner_grid = []
	for square in grid:
		sq = int(square.keys()[0])
		# Add inner grid numbers
		if gridsize < sq < ((gridsize ** 2) - gridsize) and not sq % gridsize in [ 0, 1, gridsize ]:
			inner_grid.append(sq)
	print inner_grid
	prev_letter = [] # Will be letter and position in grid (i.e., [ 'a', 5 ]
	for word in _words:
		wordgrid = ""
		# Go letter by letter.
		# Start in a random place 
		# Emphasize the middle 4 squares for common letters
		# Don't allow reuse of letters in the same word
		# Place next letter has to be adjacent to previous letter
		# If all words are placed and there are blank spaces, fill them with random letters
		# Don't actually press letters in for word unless the whole word will work there.
		#    Maybe try lots and lots of words until we get n = wordcount that actually work?
		for c in word:
			# Start somewhere on the grid
			if not prev_letter:
				# First time letter
				pass
			else:
				# Everything else
				pass
			pass
	return wordgrid

words = get_words(wordlist)
wordgrid = trace_words(words['words'],gridsize)

print words['words'], len(words['words'])
print wordgrid
