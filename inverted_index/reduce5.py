#!/usr/bin/env python3
"""
Reduce 5.

https://github.com/eecs485staff/madoop/blob/main/README_Hadoop_Streaming.md
"""
import sys
import itertools
from collections import defaultdict
# Goal: Output final inverted index
# Hopefully it works


def reduce_one_group(group):
    """Reduce one group."""
    group = list(group)

    # Gather all info for matching words together
    words = defaultdict(list)
    for line in group:
        # print(f"{key}\t{term} {doc_id} {idfk} {tfik} {d_i}")
        _, vals = line.strip().split("\t")
        term, doc_id, idfk, tfik, d_i = vals.split()
        words[term].append((idfk, f'{doc_id} {tfik} {d_i}'))

    # Print final output
    for word, val in words.items():
        # val.sort()
        idfk = val[0][0]
        joined_docs = ' '.join(v[1] for v in val)
        print(f"{word} {idfk} {joined_docs}")


def keyfunc(line):
    """Return the key from a TAB-delimited key-value pair."""
    return line.partition("\t")[0]


def main():
    """Divide sorted lines into groups that share a key."""
    for _, group in itertools.groupby(sys.stdin, keyfunc):
        reduce_one_group(group)
    # for line in sys.stdin:
    #     print(line)


if __name__ == "__main__":
    main()
