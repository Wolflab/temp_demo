#!/usr/bin/env python
# coding: utf-8



# In[2]:


import csv
import os
import shutil
from fnmatch import fnmatch, filter
from os.path import isdir, join
from shutil import copytree

# create a new dictionary by opening and reading the csv header table file
my_dict = {}  
with open("/Users/chaeheelim/Desktop/BYS431/Project/headers.csv", newline = '') as master_table:
    header_table = csv.reader(master_table, delimiter = '\t') 
    for row in header_table: 
        my_dict[row[1]] = row[2] # for each row in the header table, replace the original header with the new header
        
# create a new directory to put the output files in
    current_directory = os.getcwd()
    final_directory = os.path.join(current_directory, r'new_headers')
        
    def include_patterns(*patterns):
        def _ignore_patterns(path, names):
            keep = set(name for pattern in patterns
                                for name in filter(names, pattern))
            ignore = set(name for name in names
                            if name not in keep and not isdir(join(path, name)))
            return ignore
        return _ignore_patterns
    
# copy only the fasta files from original directory to the new directory 
    copytree(current_directory, final_directory, ignore=include_patterns('*.fasta'))
       
# working in the new directory, loop through all the fasta files and replace with correct headers
    os.chdir(final_directory)
    for filename in os.listdir():
        if filename.endswith(".fasta"):
            
            fasta_file = open(filename, "r") # open one fasta file
            old_file = fasta_file.read().splitlines() # read the fasta file as line delimited
            fasta_file.close() # close fasta file
            read_file=open(filename, 'w')
            
            with open(os.path.join(final_directory, filename)) as f:
                
                for line in old_file: # loop through each line in the old fasta file
                    if line.startswith(">"): # select only headers, which start with a ">"
                        if line in my_dict.keys(): # search if there is a matching line in master table as the selected header
                            my_dict[row[1]] = row[2] # if so, replace the old header with the new header
                            read_file.write(my_dict[line] + "\n") # write the new headers into the new fasta file 
                    else:
                        read_file.write(line + "\n") # for rows that are not headers, don't do anything and skip line

