#!/usr/bin/env python3

"""Map 0."""

import sys
import csv

# Write this map program
# The first MapReduce job counts the total
# number of documents in the collection.
# It should read input from input/ and write output to output0.
#  The output should be a single integer.
# In pipeline.sh, copy the output (e.g., output0/part-00000) to
# total_document_count.txt. In later pipeline jobs, read the document count
# from total_document_count.txt, not output0/part-00000.
# Pro-tip: Use the Python csv library and add the line
# csv.field_size_limit(sys.maxsize)
# (doc_body is very large for some documents).
# Word count, change to document count


def main():
    """Count total number of documents."""
    csv.field_size_limit(sys.maxsize)
    for _ in sys.stdin:
        print("line\t1")


if __name__ == "__main__":
    main()
