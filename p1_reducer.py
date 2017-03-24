#!/usr/bin/python
import sys
import os
import re
import time

word_keys = {}
stop_words = {}

class Reducer():
    # Read in (key, value) pairs from stdin (stdout of mapper)
    def readin_pairs(self):
        global word_count
        word_count = 0
        for input in sys.stdin:
            # Breaks up input into list of words
            input = input.strip()
            word, count = input.split('\t', 1)
            word_count = word_count + 1
            self.add_to_dict(word)

    # Determines which dictionary to add to: stop words dictionary or word keys dictionary
    def add_to_dict(self, key):
        value = 1
        # If word is a stop word, increment its occurrence in dictionary
        if key in stop_words.keys():
            #print "stop word encountered: {0}".format(key)
            value = stop_words.get(key)
            value = int(value) + 1
            stop_words[key] = value
        else:
            # If word is a legit word key, increment its occurrence in dictionary
            if key in word_keys.keys():
                value = word_keys.get(key)
                value = int(value) + 1
                # If the key becomes a stop word, add it to stop words dictionary
                if (self.stop_word((key, value))):
                    stop_words[key] = value
                else:
                    word_keys[key] = value
            else:
                word_keys[key] = value

    # Determines if word is stop word or not based on an occurrence of greater than 200
    def stop_word(self, (word, count)):
        if (count > 200):
            #print "New stop word found: {0}".format(word)
            word_keys.pop(word, None)
            return True
        else:
            return False

# Print out dictionary of word keys
def print_wk():
    print "\n|------------------------- Word Keys -------------------------|\n"
    for key, value in word_keys.items():
        print '%s\t%s' % (key, value)

# Print out dictionary of stop words
def print_sw():
    print "\n|------------------------- Stop words -------------------------|\n"
    for key, value in stop_words.items():
        print '%s\t%s' % (key, value)

if __name__ == "__main__":
    reducer = Reducer()
    start = time.time()
    reducer.readin_pairs()
    stop = time.time() - start
    print_wk()
    #print_sw()
    #sys.stderr.write("Total word count: " + str(word_count) + " (" + str(round(stop, 2)) + " secs) " + '\n')
