#!/usr/bin/env python3

"""Reduce 1."""

import sys
import itertools

# # Goal: Output doc_id,text


def reduce_one_group(group):
    """Reduce one group."""
    group = list(group)
    for line in group:
        print(line.strip())  # This should output the docid, text


def keyfunc(line):
    """Return the key from a TAB-delimited key-value pair."""
    return line.partition("\t")[0]


def main():
    """Divide sorted lines into groups that share a key."""
    for _, group in itertools.groupby(sys.stdin, keyfunc):
        reduce_one_group(group)


if __name__ == "__main__":
    main()
