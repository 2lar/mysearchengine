#!/usr/bin/env python3

"""Map 4."""

import sys

# The goal of this map reduce job is
# to get the normalization factor for each document
# and put everything together


def main():
    """Split stuff into 3 parititions."""
    for line in sys.stdin:
        line = line.strip()
        curkey, vals = line.split("\t")
        term, doc_id = curkey.split()
        # print(f"{term} {doc_id}\t{idfk} {tfik} {d_i}")
        idfk, tfik, d_i = vals.split()
        key = int(doc_id) % 3
        print(f"{key}\t{term} {doc_id} {idfk} {tfik} {d_i}")


if __name__ == "__main__":
    main()
