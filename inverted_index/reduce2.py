#!/usr/bin/env python3
"""
Reduce 2.

https://github.com/eecs485staff/madoop/blob/main/README_Hadoop_Streaming.md
"""
import sys
import itertools

# Goal: Take in the (doc_id,term) 1 from stdin
# and combine them to get the term frequency
# value for each term in each doc_id
# The end result should be
# (doc_id,term) term_freq. (doc_id,term)
# is the key and term_freq is the value
# have docid, term, where docid is all the same


def reduce_one_group(key, group):
    """Reduce one group."""
    # Initialize variables
    last_word = None
    curr_count = 1
    doc_id = key
    # Iterate through group
    for line in group:
        # print(line)
        word = line.partition("\t")[2].strip()
        if word != last_word:
            if last_word is not None:
                print(f'{last_word} {doc_id}\t{curr_count}')
            curr_count = 1
            last_word = word
        else:
            curr_count = curr_count + 1
    # print out last element
    print(f'{last_word} {doc_id}\t{curr_count}')


def keyfunc(line):
    """Return the key from a TAB-delimited key-value pair."""
    return line.partition("\t")[0]


def main():
    """Divide sorted groups that share a key."""
    # for line in sys.stdin:
    #     print(line)
    for key, group in itertools.groupby(sys.stdin, keyfunc):
        reduce_one_group(key, group)


if __name__ == "__main__":
    main()
