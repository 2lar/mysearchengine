#!/usr/bin/env python3
"""
Reduce 3.

https://github.com/eecs485staff/madoop/blob/main/README_Hadoop_Streaming.md
"""
import sys
import itertools
import math

# Goal: Take in the stuff from stdin and
# use it to calculate n_k, and then using
# n_k and doc_count(big_n), find the idf value for each term


# Given: big_n, tfik, and n_k, calculate idfk and then get wik

# Eventually, we want term, (idf, (doc_id,term_freq), ...)
def reduce_one_group(key, group):
    """Reduce one group."""
    lgroup = list(group)
    n_k = len(lgroup)
    term = key.strip()
    idfk = 0
    with open("total_document_count.txt", encoding='utf-8') as doc_count:
        big_n = int(doc_count.readline())  # Read the count
        idfk = math.log10(big_n/n_k)

    for line in lgroup:
        line = line.strip()
        term, vals = line.split("\t")
        doc_id, tfik = vals.split()
        wik = float(tfik) * idfk
        print(f'{doc_id} {term}\t{wik} {tfik} {idfk}')


def keyfunc(line):
    """Return the key from a TAB-delimited key-value pair."""
    return line.partition("\t")[0]


def main():
    """Divide sorted groups that share a key."""
    for key, group in itertools.groupby(sys.stdin, keyfunc):
        reduce_one_group(key, group)
    # for line in sys.stdin:
    #     print(line)
    # Use term  doc_id,term_freq to find n_k and use that to find idfk and use
    # that to find w and use that to find normalization


if __name__ == "__main__":
    main()
