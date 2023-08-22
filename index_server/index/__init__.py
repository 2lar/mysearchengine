"""Index package initializer."""
import os
import flask

# Define Flask app
app = flask.Flask(__name__)

# Configure app to use inverted_index_1.txt by default
app.config["INDEX_PATH"] = os.getenv("INDEX_PATH", "inverted_index_1.txt")

import index.api  # noqa: E402  pylint: disable=wrong-import-position

# Load inverted index, stopwords, and pagerank into memory
index.api.load_index()
