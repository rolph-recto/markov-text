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

		#get the next chunk from the next n words
		#where n = chunk_size
		next_chunk = " ".join(word_list[i+1:i+chunk_size+1])

		#word was not previously parsed
		#create new element in map
		if not word in markov_map:
			markov_map[word] = {}

		#next chunk was not previous parsed
		#create new element in map
		if not next_chunk in markov_map[word]:
			markov_map[word][next_chunk] = 1
		else:
			markov_map[word][next_chunk] += 1

	#now calculate the frequency of each chunk
	#which is important for to calculate the
	#probability to each next_word to be picked
	for word, chunk_info in markov_map.iteritems():
		frequency = 0

		for next_chunk, num in chunk_info.iteritems():
			frequency += num
		
		markov_map[word]["__frequency__"] = frequency

	return markov_map

def generate_text(max_chunks, markov_map, words_per_line):
	"""generate text sequence of a specified length using a given Markov map"""

	chunk_list = []

	#pick a random word to start with
	#make sure the word is capitalized
	#to (somewhat) ensure the text begins
	#with the beginning of a sentence
	#this assumes that at least one word
	#in the text is capitalized
	word = "word"
	while not word[0].isupper():
		word = random.choice(markov_map.keys())
		
	chunk_list.append(word)

	num_chunks = 1
	while num_chunks < max_chunks:
		next_chunks = markov_map[word]
		
		#add up chunk values until it hits a threshold
		#then add the current chunk into the generated chunk list
		#this allows chunk with high values to have a higher
		#probability of being chosen
		val = 0
		threshold = int(round(random.random() * next_chunks["__frequency__"]))

		#shuffle the chunk list to ensure randomness
		shuffled_chunk_list = next_chunks.keys()
		random.shuffle(shuffled_chunk_list)

		for next_chunk in shuffled_chunk_list:
			#make sure we're not trying to choose '__frequency__'!
			if not next_chunk == "__frequency__":
				val += next_chunks[next_chunk]
				#if the chunk value passes the treshold, select the word
				if val >= threshold:
					break
		
		chunk_list.append(next_chunk)

		#if next_chunk is the last chunk, it is not in the markov map
		#find a random word to replace it instead
		if not next_chunk in markov_map:
			word = random.choice(markov_map.keys())
		else:
			#the next word should the first word of the chunk
			word = next_chunk.split()[0]

		num_chunks += 1

	#convert chunk list into a list of single words
	word_list = " ".join(chunk_list).split()
	text = ""
	
	#split output into lines
	if words_per_line > 0:
		for i, word in enumerate(word_list):
			text += word + " "
			if (i+1) % words_per_line == 0:
				text += "\n"
	#keep output in one line
	else:
		text = " ".join(word_list)
		
	return text

def ends_in_punctuation(text):
	return '.' in text or '?' in text or '!' in text
	
def end_sentence(text):
	"""ensures that the generated text ends in a sentence"""

	#if there is punctuation in the generated text
	#that denotes a sentence, make sure the text
	#ends in a complete sentence, not a fragment
	if ends_in_punctuation(text):
		#find the last instance of the punctuation '.', '?' or '!'
		last_index = 0
		for punctuation in ['.', '?', '!']:
			punc_index = text.rfind(punctuation)
			if last_index < punc_index:
				last_index = punc_index
		
		return text[:last_index+1]
	#if there is no sentence punctuation, return the whole text
	else:
		return text
	
def strip_enclosures(text):
	"""removes parenthesis and quote-marks from the text to prevent mismatched/open enclosures"""
	
	for bad_char in ['\"', '[', ']', '(', ')']:
		text = text.replace(bad_char, '')
	
	return text
		
def cleanup(text):
	"""add decorators to this function to clean up the generated text"""
	
	text = end_sentence(text)
	text = strip_enclosures(text)
	
	return text
	
def main(filename, num_words, chunk_size, words_per_line):
	#file must exist!
	if os.path.exists(filename):
		#num_words has to be at least 1
		if num_words > 0:
			markov_map = create_markov_map(filename, chunk_size)
			generated_text = generate_text(num_words, markov_map, words_per_line)
			
			#clean up the generated text
			generated_text = cleanup(generated_text)
			
			print len(generated_text)
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
			words_per_line = int(sys.argv[3])
			chunk_size = int(sys.argv[4])
			main(sys.argv[1], num_words, chunk_size, words_per_line)
		except ValueError:
			print "Error: Not a number."

	elif len(sys.argv) == 1:
		print "Usage: markov.py filename num_words words_per_line chunk_size "

	else:
		print "Error: Must have two arguments."
	


