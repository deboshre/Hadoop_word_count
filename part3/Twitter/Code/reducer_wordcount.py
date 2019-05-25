#!/usr/bin/env python3
"""reducer.py"""

from operator import itemgetter
import sys

current_word = None
current_count = 0
word = None
reduced_data = {}
top_10 = {}

# input comes from STDIN
for line in sys.stdin:
    # remove leading and trailing whitespace
    line = line.strip()

    # parse the input we got from mapper.py
    word, count = line.split('\t', 1)

    if word in reduced_data:
        reduced_data[word] += int(count)
    else:
        reduced_data[word] = int(count)

    # # convert count (currently a string) to int
    # try:
    #     count = int(count)
    # except ValueError:
    #     # count was not a number, so silently
    #     # ignore/discard this line
    #     continue

    # # this IF-switch only works because Hadoop sorts map output
    # # by key (here: word) before it is passed to the reducer
    # if current_word == word:
    #     current_count += count
    # else:
    #     if current_word:
    #         # write result to STDOUT
    #         print('%s\t%s' % (current_word, current_count))
    #     current_count = count
    #     current_word = word

top_10_key_val = sorted(reduced_data.items(), key=lambda kv: kv[1], reverse= True)[0:20]
# do not forget to output the last word if needed!
for kv in top_10_key_val:
  top_10[kv[0]] = kv[1]
  print('%s\t%s' % (kv[0], kv[1]))
# if current_word == word:
#     print('%s\t%s' % (current_word, current_count))
