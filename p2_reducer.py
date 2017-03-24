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
            word, fname, line_num = input.split('\t', 2)
            #print word, fname, line_num
            word_count = word_count + 1
            #print word_count
            self.add_to_dict(word, fname, line_num)

    # Determines which dictionary to add to: stop words dictionary or word keys dictionary
    def add_to_dict(self, key, fname, line_num):
        # Coment out if we want to continue maintaining info for stop words
        # # If word is a stop word
        # if key in stop_words.keys():
        #     # Get list of tuples for current word key
        #     pairs = stop_words.get(key)
        #     for tuple in pairs:
        #         # If file name is in the tuple, add line number to its list
        #         if (fname == tuple[0]):
        #             tuple[1].append(line_num)
        # If word is a stop word
        if key in stop_words.keys():
            # Get list of tuples for current word key
            file = stop_words.get(key)
            # If key corresponds to this file, do nothing
            if (fname == file):
                return
        else:
            # If word is a legit word key
            if key in word_keys.keys():
                # Get list of tuples for current word key
                pairs = word_keys.get(key)
                # Traverse all tuples, (file_name, list of line numbers for word key) for each word key
                for tuple in pairs:
                    # If file name is in the tuple, add line number to its list
                    if (fname == tuple[0]):
                        tuple[1].append(line_num)
                        line_numbers = tuple[1][:]
                    # If file name not encountered yet
                    elif (fname != tuple[0]):
                        line_numbers = [line_num]
                        pairs.append((fname, line_number))
                # If the key becomes a stop word, add it to stop words dictionary
                if (self.stop_word(key, fname, line_numbers)):
                    #stop_words[key] = pairs
                    stop_words[key] = fname
                    #print "New stop word found: {0}, {1}".format(key, pairs)
                else:
                    word_keys[key] = pairs
            else:
                #print "New key added: {0}".format([(fname, [line_num])])
                word_keys[key] = [(fname, [line_num])]

    # Determines if word is stop word or not based on an occurrence of greater than 200
    def stop_word(self, word, fname, count):
        if (len(count) > 200):
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
    #print_wk()
    print_sw()
    sys.stderr.write("Total word count: " + str(word_count) + " (" + str(round(stop, 2)) + " secs) " + '\n')
