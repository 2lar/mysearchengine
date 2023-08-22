#!/usr/bin/env python3
"""
Reduce 4.

https://github.com/eecs485staff/madoop/blob/main/README_Hadoop_Streaming.md
"""
import sys
import itertools

# Goal: Output final inverted index

# Hopefully it works


# Calculate |d|

def reduce_one_group(key, group):
    """Reduce one group."""
    group = list(group)
    doc_id = key
    d_i = 0
    # line: doc_id  term wik tfik idfk}'
    for line in group:
        vals = line.split("\t")[1]
        wik = vals.split()[1]
        wik = float(wik)
        # Add to d_i value for specific doc_id
        d_i = d_i + (wik * wik)
    for line in group:
        vals = line.split("\t")[1]
        term, wik, tfik, idfk = vals.split()
        print(f"{term} {doc_id}\t{idfk} {tfik} {d_i}")


def keyfunc(line):
    """Return the key from a TAB-delimited key-value pair."""
    return line.partition("\t")[0]


def main():
    """Divide sorted lines into groups that share a key."""
    for key, group in itertools.groupby(sys.stdin, keyfunc):
        reduce_one_group(key, group)


if __name__ == "__main__":
    main()
