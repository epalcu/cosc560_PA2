#!/usr/bin/python
import sys
import os
import re
import time

word_keys = {}

class Reducer():
    # Read in (key, value) pairs from stdin (stdout of mapper)
    def readin_pairs(self):
        global file_name
        for input in sys.stdin:
            # Breaks up input into list of words
            input = input.strip()
            word, fname, line_num = input.split('\t', 2)
            try:
                if (fname != file_name):
                    distinct_words = remove_stop_words(distinct_words)
                    file_name = fname
                    distinct_words = 0
            except:
                file_name = fname
                distinct_words = 0
            distinct_words = self.add_to_dict(word, fname, line_num, distinct_words)
        return remove_stop_words(distinct_words)

    # Determines which dictionary to add to: stop words dictionary or word keys dictionary
    def add_to_dict(self, key, fname, line_num, distinct_words):
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
                distinct_words = distinct_words + 1
        else:
            word_keys[key] = [(fname, [line_num])]
            distinct_words = distinct_words + 1
        return distinct_words

def remove_stop_words(distinct_words):
    frequency = int(distinct_words*0.05)
    for key, value in word_keys.items():
        for file in range(0, len(value)):
            if (value[file][0] == file_name):
                if (len(value[file][1]) >= frequency):
                    #print '%s\t%s\t%s' % (key, value[file][0], len(value[file][1]))
                    value.pop(file)

# Print out dictionary of word keys
def print_wk():
    print "\n|------------------------- Word Keys -------------------------|\n"
    for key, value in word_keys.items():
        for file in value:
            print '%s\t%s' % (key, len(value))

if __name__ == "__main__":
    reducer = Reducer()
    start = time.time()
    reducer.readin_pairs()
    stop = time.time() - start
    print_wk()
    #sys.stderr.write("Total word count: " + str(word_count) + " (" + str(round(stop, 2)) + " secs) " + '\n')
    print ("Total elapsed time: {0} secs.").format(stop)
