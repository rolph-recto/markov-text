#markov.py
#Markov text generator

import sys
import os.path
import random

def create_markov_map(filename, chunk_size):
	"""build a Markov map of a text"""

	markov_map = {}	

	#build word list
	with open(filename) as f:
		data = f.read(-1)
		word_list = data.split()

	#iterate through the word list
	#we're going to ignore the last word because
	#the Markov chain calculation relies on the
	#word having a word after it, so the last word
	#doesn't count in the calculation 
	for i in range(len(word_list) - chunk_size):
		word = word_list[i]
		#get the next word from list of next words
		#where the list has a size of chunk_size
		next_word = " ".join(word_list[i+1:i+chunk_size+1])

		#word was not previously parsed
		#create new element in map
		if not word in markov_map:
			markov_map[word] = {}

		#next word was not previous parsed
		#create new element in map
		if not next_word in markov_map[word]:
			markov_map[word][next_word] = 1
		else:
			markov_map[word][next_word] += 1

	#now calculate the frequency of each word
	#which is important for to calculate the
	#probability to each next_word to be picked
	for word, word_info in markov_map.iteritems():
		frequency = 0

		for next_word, num in word_info.iteritems():
			frequency += num
		
		markov_map[word]["__frequency__"] = frequency

	return markov_map


def generate_text(max_words, markov_map):
	"""generate text sequence of a specified length using a given Markov map"""

	word_list = []

	#pick a random word to start with
	word = random.choice(markov_map.keys())
	word_list.append(word)

	num_words = 1
	while num_words < max_words:
		next_words = markov_map[word]
		
		#add up word values until it hits a threshold
		#then add the current word into the generated word list
		#this allows words with high values to have a higher
		#probability of being chosen
		val = 0
		threshold = int(round(random.random() * next_words["__frequency__"]))

		#shuffle the word list to ensure randomness
		shuffled_word_list = next_words.keys()
		random.shuffle(shuffled_word_list)

		for next_word in shuffled_word_list:
			#make sure we're not trying to choose '__frequency__'!
			if not next_word == "__frequency__":
				val += next_words[next_word]
				#if the word value passes the treshold, select the word
				if val >= threshold:
					break
		
		word_list.append(next_word)

		#if next_word is the last word, it is not in the markov map
		#find a random word to replace it instead
		if not next_word in markov_map:
			word = random.choice(markov_map.keys())
		else:
			#the next word should the first word of the chunk
			word = next_word.split()[0]

		num_words += 1

	return " ".join(word_list)


def main(filename, num_words, chunk_size):
	#file must exist!
	if os.path.exists(filename):
		#num_words has to be at least 1
		if num_words > 0:
			araby_markov_map = create_markov_map(filename, chunk_size)
			generated_text = generate_text(num_words, araby_markov_map)
			print generated_text

		else:
			print "Error: num_words must be greater than 0."

	else:
		print "Error: filename '{0}' does not exist!".format(filename)

if __name__ == "__main__":
	#check for the right number of arguments
	if len(sys.argv) >= 4:
		try:
			num_words = int(sys.argv[2])
			chunk_size = int(sys.argv[3])
			main(sys.argv[1], num_words, chunk_size)
		except ValueError:
			print "Error: Not a number."

	elif len(sys.argv) == 1:
		print "Usage: markov.py filename num_words"

	else:
		print "Error: Must have two arguments."
	


