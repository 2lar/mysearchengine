#!/usr/bin/env python3

"""Map 1."""

import csv
import sys
import re


# Convert input into document id, cleaned up document contents key-value pair
# in mapping, convert comma seperated
# input file into key value pair based on document id
# in reduce, just output lines that were cleaned in map

# CLEANING FOR 1 DOCUMENT

# Follow these cleaning steps for one document.
# When you parse a query in the Index server,
# you’ll use the same procedure.

# Combine both document title and document body by concatenating them,
# separated by a space.

# Remove non-alphanumeric characters (that also aren’t spaces) like this:
# import re
# text = re.sub(r"[^a-zA-Z0-9 ]+", "", text)
# The inverted index should be case insensitive.
# Convert upper case characters to lower case using casefold().
# Split the text into whitespace-delimited terms.

# Remove stop words. We have provided a list of stop words
# in inverted_index/stopwords.txt

def main():
    """Clean document output."""
    csv.field_size_limit(sys.maxsize)
    # Iterate through all documents in input.csv
    for line in csv.reader(sys.stdin):
        # print key (doc id)
        print(line[0] + '\t', end='')
        # combine title with body text
        text = line[1] + ' ' + line[2]
        # remove non alphanumeric characters
        text = re.sub(r"[^a-zA-Z0-9 ]+", "", text)
        # Convert to lowercase
        text = text.casefold()
        # Remove stop words
        with open('stopwords.txt', newline='', encoding='utf-8') as stop_file:
            stop_words = stop_file.read().split()
            # using list comprehension, print only output
            # words that are not in list of stop words
            for word in text.split():
                if word not in stop_words:
                    print(word, end=' ')
            # stop_list = ["apart", "artful"]
            # for thing in stop_list:
            #     if "art" in thing:
            #         print("Art is a stop word")
            # convert text_arr back to string
        print('\n', end='')


if __name__ == "__main__":
    main()
