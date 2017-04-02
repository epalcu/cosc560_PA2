#!/usr/bin/python
import sys
import os
import re

class Query():
    def find_instances(self):
        line_list = []

        with open('inverted_index.txt') as fname:
            lines = fname.readlines()
            for line in lines:
                line_list.append(line)

        while(1):

            words = raw_input("Enter one or more words to search or \'q\' to quit: ")
            words =  words.split()

            for w in words:
                if(w.lower() == 'q'):
                    exit(1)

                found = False
                for l in line_list:
                    l_split = l.split('\t')
                    if(l_split[0] == w.lower()):
                        print l
                        found = True            
                        break

                if(found == False):
                    print "Query \'{0}\' not found \n".format(w)


if __name__ == "__main__":
    query = Query()
    query.find_instances()
