#!/usr/bin/env python3
"""reducer.py"""

from operator import itemgetter
import sys
import json

current_word = None
current_count = 0
word = None
final_dic = {}

# input comes from STDIN
for line in sys.stdin:
    # remove leading and trailing whitespace
    line = line.strip()

    # parse the input we got from mapper.py
    word, dic = line.split('\t', 1)
    # print('%s\t%s' % (word, json.dumps(dic)))

    # convert count (currently a string) to int
    try:
        dic = json.loads(dic)
    except ValueError:
        # count was not a number, so silently
        # ignore/discard this line
        continue

    # if word not in final_dic:
    #     final_dic[word] = dic
    # else :
    #     for key in dic.keys():
    #         if key in final_dic[word]:
    #             final_dic[word][key] += dic[key]
    #         else :
    #             final_dic[word][key] = dic[key]

    # this IF-switch only works because Hadoop sorts map output
    # by key (here: word) before it is passed to the reducer
    if current_word == word:
        # current_count += count
        for key in dic.keys():
            if key in final_dic[word]:
                final_dic[word][key] += dic[key]
            else :
                final_dic[word][key] = dic[key]
    else:
        if current_word:
            # write result to STDOUT
            if current_word in final_dic:
                for key in final_dic[current_word].keys():
                    print('%s-%s\t%s' % (current_word,key,final_dic[current_word][key]))
        final_dic[word] = dic
        current_word = word

# do not forget to output the last word if needed!
if current_word == word:
    if word in final_dic:
        for key in final_dic[word].keys():
            print('%s-%s\t%s' % (current_word,key,final_dic[word][key]))
