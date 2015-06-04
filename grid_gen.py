#! /usr/bin/env python

import os,sys
from random import shuffle

if len(sys.argv) < 2:
	print "Insufficient arguments."
	sys.exit(1)

gridsize = 5
filename = sys.argv[1]
wordlist = [line.rstrip('\n').upper().split(',') for line in open(filename, 'r').readlines()]

def get_words():
	words = { 'chars': {}, 'words': [] }
	shuffle(wordlist)
	for word, meaning in wordlist:
		if len(words['words']) == 10: break
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

words = get_words()
print words['words'], len(words['words'])
