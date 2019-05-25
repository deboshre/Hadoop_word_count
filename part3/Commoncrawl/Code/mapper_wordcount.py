#!/usr/bin/env python3
"""mapper.py"""

import sys
import nltk
import csv
import re
import preprocessor as tweet_process
import json
nltk.download('stopwords')
nltk.download('wordnet')
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


input = ["get", "work"]

def clean(input):
  doc = []
  alphabet_pattern = r'[^a-zA-Z\s]'
  non_unicode_pattern = r'\\x.{2}'
  lemmatizer = WordNetLemmatizer()
  result = re.sub(non_unicode_pattern, '', tweet_process.clean(input))
  result = re.sub(alphabet_pattern, '', result)
  result = lemmatizer.lemmatize(result)
  # doc.append(result.lower())
  return result.lower()

stop_words = nltk.corpus.stopwords.words('english')

# input comes from STDIN (standard input)
for line in sys.stdin:
    # remove leading and trailing whitespace
    # line = line[0]
    line = line.strip()
    line = clean(line)
    # split the line into words
    words = line.split()
    # increase counters
    for word in words:
        # write the results to STDOUT (standard output);
        # what we output here will be the input for the
        # Reduce step, i.e. the input for reducer.py
        #
        # tab-delimited; the trivial word count is 1
        if word not in stop_words:
            print('%s\t%s' % (word, 1))
        
