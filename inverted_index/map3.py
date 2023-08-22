#!/usr/bin/env python3

"""Map 3."""

import sys

# Write this map program

# The goal of this map reduce job is to
# use the (doc_id,term),term_freq from stdin
# and flip it to get a term,(doc_id,term_freq,1).
# Each term key will have multiple
# (doc_id, term_freq,1) values. We need to
# do this since eventually all calculated
# values will be found on a per term basis.

# The goal of this mapping is to be able
# to calculate nk for each term, which is the number
# of documents a term appears in. To do
# this we need a value 1 for each unique document.


# Goal: Take input from stdin and modify
# it to fit the format expected by Reduce 3
# Input format from Reduce 2: (doc_id,term) term_freq
# Output format for Reduce 3: term, (idf, (doc_id,term_freq), ...)

def main():
    """Read input from stdin, apply mapping function, and print output."""
    for line in sys.stdin:
        line = line.strip()
        key, term_freq = line.split("\t")
        term = key.split()[0]
        print(f"{term}\t{key.split()[1]} {term_freq}")


if __name__ == "__main__":
    main()
