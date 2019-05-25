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

# input_file = open("/home/cse587/Documents/dic/output/nyt_wc", "r")
# keys = input_file.readlines()
# keywords = []
# for key in keys:
#   keywords.append(key.split(" ")[0])

# input = csv.reader(input_file)

input = [ "usa", "trump", "getty", "new", "first","lady","one","white","today","photo"]

dic = {}

def Count_Cooccurence(temp):
  for i, val in enumerate(temp):
    if val not in dic:
        dic[val] = {}
    for j in range(i+1, len(temp)):
      if temp[j] in dic[val]:
        dic[val][temp[j]] += 1
      else:
        dic[val][temp[j]] = 1


def clean(input):
  doc = []
  alphabet_pattern = r'[^a-zA-Z\s]'
  non_unicode_pattern = r'\\x.{2}'
  lemmatizer = WordNetLemmatizer()
  result = re.sub(non_unicode_pattern, '', tweet_process.clean(input))
  result = re.sub(alphabet_pattern, '', result)
  result = lemmatizer.lemmatize(result)
  return result.lower()

stop_words = nltk.corpus.stopwords.words('english')
stop_words += ["mr", "mrs", "would"]

# input comes from STDIN (standard input)
for line in sys.stdin:
    temp = []
    # remove leading and trailing whitespace
    line = line.strip()
    line = clean(line);
    # split the line into words
    words = line.split()
    n = len(words)
    # increase counters
    for row in input:
        # write the results to STDOUT (standard output);
        # what we output here will be the input for the
        # Reduce step, i.e. the input for reducer.py
        #
        # tab-delimited; the trivial word count is 1
        if row in words:
          temp.append(row)
    Count_Cooccurence(temp)           

for row in input:
  if row in dic:
    print('%s\t%s' % (row, json.dumps(dic[row])))

# for row in input:
#     print('%s\t%s' % (row, json.dumps({})))
        
