#!/usr/bin/python
import sys
import os
import re

class Mapper():
    
    # Read in contents from file via stdin
    def make_pairs(self):
        line_num = 1
        for input in sys.stdin:
            input = re.findall(r"(?<![@#])\b\w+(?:'\w+)?", input)
            
            # For each word, return (key, value) pair of its lowercase form and trivial value of 1
            # Print to stdout for reducer to read in
            for word in input:
                filepath = os.environ['map_input_file'] 
                filename = os.path.split(filepath)[-1]
                print '%s\t%s\t%s' % (word.lower(), filename, line_num)
            line_num = line_num + 1

if __name__ == "__main__":
    mapper = Mapper()
    mapper.make_pairs()
