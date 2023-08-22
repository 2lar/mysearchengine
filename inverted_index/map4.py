#!/usr/bin/env python3

"""Map 4."""

import sys

# The goal of this map reduce job is
# to get the normalization factor for each document
# and put everything together


def main():
    """Make doc_id the primary key."""
    # print(f'{doc_id} {term}\t{wik} {tfik} {idfk}'

    for line in sys.stdin:
        line = line.strip()
        key, vals = line.split("\t")
        doc_id, term = key.split()
        term = term.strip()
        doc_id = doc_id.strip()
        print(f"{doc_id}\t{term} {vals}")


if __name__ == "__main__":
    main()
