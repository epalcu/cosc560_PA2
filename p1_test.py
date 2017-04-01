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
        global file_name
        global word_count
        for input in sys.stdin:
            # Breaks up input into list of words
            input = input.strip()
            word, fname, line_num = input.split('\t', 2)
            try:
                if fname != file_name:
                    file_name = fname
                    word_count = 0
                else:
                    word_count = word_count + 1
            except:
                file_name = fname
                word_count = 0
            #print word_count
            self.add_to_dict(word, fname, line_num)

    # Determines which dictionary to add to: stop words dictionary or word keys dictionary
    def add_to_dict(self, key, fname, line_num):
        # If word is a legit word key
        if key in word_keys.keys():
            found = False
            # Get list of tuples for current word key
            pairs = word_keys.get(key)
            # Traverse all tuples, (file_name, list of line numbers for word key) for each word key
            for tuple in pairs:
                # If file name is in the tuple, add line number to its list
                if (fname == tuple[0]):
                    found = True
                    tuple[1].append(line_num)
                    line_numbers = tuple[1][:]
                    break
            # If file name not encountered
            if (found == False):
                line_numbers = [line_num]
                pairs.append((fname, line_numbers))
        else:
            word_keys[key] = [(fname, [line_num])]

# Determines if word is stop word or not based on an occurrence of greater than 200
def find_stop_words(self):
    frequency = int(word_count*0.005)
    for key, value in word_keys.items():
        for file in value:
            if (len(file[1]) > frequency):
                word_keys.pop(word, None)
                stop_words[key] = [(file[0], file[1])]

# Print out dictionary of word keys
def print_wk():
    print "\n|------------------------- Word Keys -------------------------|\n"
    for key, value in word_keys.items():
        for file in value:
            print '%s\t%s' % (key, len(file[1]))

# Print out dictionary of stop words
def print_sw():
    print "\n|------------------------- Stop words -------------------------|\n"
    for key, value in stop_words.items():
        print '%s\t%s' % (key, value)

if __name__ == "__main__":
    reducer = Reducer()
    start = time.time()
    reducer.readin_pairs()
    find_stop_words
    stop = time.time() - start
    #print_wk()
    print_sw()
    #sys.stderr.write("Total word count: " + str(word_count) + " (" + str(round(stop, 2)) + " secs) " + '\n')
    print ("Total elapsed time: {0} secs.").format(stop)
