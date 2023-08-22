#!/usr/bin/env python3

"""Map 2."""

import sys

# Write this map program

# The goal of this map reduce job is to
# map each doc_id with the terms in it.
# So we should have (doc_id, term),1.
# We need to make sure that there are no stop words
# in this mapping by using stopwords.txt.
# (doc_id,term) is a key tuple. The value
# is the singular digit 1 which means an occurrence.
# We are eventually trying to get the term frequency
# in this job by reducing these together


def main():
    """Map doc_id with terms."""
    for line in sys.stdin:
        doc_id, doc_body = line.split("\t")
        doc_body = doc_body.split()
        for word in doc_body:
            print(f"{doc_id}\t{word}")


if __name__ == "__main__":
    main()
