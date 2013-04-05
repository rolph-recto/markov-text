markov-text
===========

Simple Markov text generator written in Python 2.7.

Command line usage:
python markov.py filename num_words words_per_line chunk_size

-filename: file to read text from
-num_chunks: number of chunks to generate
-words_per_line: number of words in betwen line breaks (set to -1 to have no line breaks)
-chunk_size: number of words per chunk

This is a pretty fast script; I've tried it with Ulysses as the source text (~250,000 words) and it finished in 1 or 2 seconds. It's a nice simple toy to play around with.

For best results, set chunk_size to around 2 to 4. If you want to make random esoteric poetry, words_per_line is your friend. (Though you'll still have to break you own stanzas -- a feature in the future, maybe?)
