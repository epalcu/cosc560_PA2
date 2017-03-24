#!/usr/bin/python
import sys
import os
import re

class Mapper():
    # Read in contents from file via stdin
    def make_pairs(self):
        for input in sys.stdin:
            input = re.findall(r"(?<![@#])\b\w+(?:'\w+)?", input)
            # For each word, return (key, value) pair of its lowercase form and trivial value of 1
            # Print to stdout for reducer to read in 
            for word in input:
                print '%s\t%s' % (word.lower(), 1)

if __name__ == "__main__":
    mapper = Mapper()
    mapper.make_pairs()
