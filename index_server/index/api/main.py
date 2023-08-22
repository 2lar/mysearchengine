"""REST API for index."""
import math
import re
import index
import flask


def load_index():
    """Load inverted index file, PageRank file, stopwords files into memory."""
    index.inverted_index = {}
    index.pagerank = {}
    index.stopwords = []

    index_directory = "index_server/index/inverted_index/"
    index_directory = index_directory + index.app.config['INDEX_PATH']
    with open(index_directory, "r", encoding="utf-8") as indexer:
        for line in indexer:
            line_list = line.strip().split()
            # term, idfk, [doc_id, term_freq, normalization_factor] []...
            # 0003 3.514282047860378 27687935 1 42750.538057535094
            word = line_list[0].strip()
            index.inverted_index[word] = {}
            index.inverted_index[word]["idfk"] = float(line_list[1].strip())
            index.inverted_index[word]["docs"] = {}
            for i in range(2, len(line_list), 3):
                doc_id = line_list[i].strip()
                term_freq = float(line_list[i+1].strip())
                norm = float(line_list[i+2].strip())
                index.inverted_index[word]["docs"][doc_id] = {}
                index.inverted_index[word]["docs"][doc_id][
                                    'frequency'] = term_freq
                index.inverted_index[word]["docs"][doc_id][
                                    'normalization'] = norm

    with open('index_server/index/stopwords.txt', encoding="utf-8") as stops:
        for line in stops:
            index.stopwords.append(line.strip())

    with open('index_server/index/pagerank.out', "r", encoding='utf-8') as f_i:
        for line in f_i:
            # 14533,0.00629158
            docid, rank = line.split(',')
            index.pagerank[int(docid)] = float(rank)


@index.app.route('/api/v1/', methods=['GET'])
def get_services():
    """Return a list of services available."""
    context = {
        "hits": "/api/v1/hits/",
        "url": "/api/v1/"
    }
    return flask.jsonify(**context)


@index.app.route('/api/v1/hits/', methods=['GET'])
def get_hits():
    """Return a list of hits with doc ID and score."""
    query = flask.request.args.get('q')
    weight = float(flask.request.args.get('w', default=0.5))

    # need to clean query
    query = clean_query(query)

    # SPEC SAYS AND for all query searches. inverted index must contain all
    for word in query:
        if word not in index.inverted_index:
            # print("Went inside here")
            return flask.jsonify({"hits": []})
            # print("NOT GOING IN")
    # search with the query and weights
    sorted_ranks = search(query, weight)
    # print(sorted_ranks)
    # after sorted append to a final hitlist
    hitlist = []
    for item in sorted_ranks:
        hitlist.append({
            'docid': int(item[1]),
            'score': float(item[0])
        })

    # return the results of the search into json context thing
    context = {
        "hits": hitlist
    }
    return flask.jsonify(**context)


def clean_query(query):
    """Clean query."""
    # Cleaning the input
    query = re.sub(r"[^a-zA-Z0-9 ]+", "", query)
    # Convert to lowercase
    query = query.casefold()
    query_words = query.strip().split()
    query_cleaned = []
    # Remove stop words
    query_cleaned = [word for word in query_words if word
                     not in index.stopwords]

    # Return query words without any of the stop words
    return query_cleaned


def search(query, weight):
    """Search the queries."""
    # Search has too many variables
    # ALso has too many branches, should use helper functions
    hit_docs = {}
    # Find docs that contain each word
    query_term_freqs = {}
    if query == ' ':
        return []
    make_hitdocs_queryterms(hit_docs, query_term_freqs, query)
    # eliminate hits that are only for one word
    hit_list = [doc_id for doc_id, num_hits in hit_docs.items()
                if num_hits == len(query)]

    # calculate query vector
    query_vector = []
    for word in query:
        query_vector.append(query_term_freqs[word] *
                            index.inverted_index[word]["idfk"])

    # tf-idf score is to dot product of query and document vector.
    # have a running sum of query vector * document vector
    # then return that running sum divided by
    # (query normalization factor * doc...)
    # ument normalization factor which is
    # the sqrt(focumentvector of idf values)
    thedocvec = {}
    final_ranks = doc_query_calc(hit_list, thedocvec, query,
                                 query_vector, weight)

    # sort towards the end
    final_ranks.sort(reverse=True)

    return final_ranks
    # check for docs that hit for each word


def make_hitdocs_queryterms(hit_docs, query_term_freqs, query):
    """Make and check the hitdocs and check query."""
    for word in query:
        # doc contains word
        if index.inverted_index[word] is not None:
            for doc in index.inverted_index[word]["docs"]:
                if str(int(doc)) not in hit_docs:
                    hit_docs[str(int(doc))] = 1
                else:
                    hit_docs[str(int(doc))] += 1
        # check if word has previously occured in query
        if word not in query_term_freqs:
            query_term_freqs[word] = 1
        # If it has occurred, increase frequency
        else:
            query_term_freqs[word] += 1


def doc_query_calc(hit_list, thedocvec, query, query_vector, weight):
    """Calculate in vectors."""
    for docid in hit_list:
        thedocvec[docid] = []
        # calculate doc vector
        # calculate document vector by
        # word of doc id's frequency by idf score, for each document
        for word in query:
            # calc term frequency in document i * inverse document frequency
            thedocvec[docid].append((index.inverted_index[word][
                                    "docs"][docid]['frequency'] *
                    index.inverted_index[word]["idfk"],
                    float(index.inverted_index[word][
                          "docs"][docid]["normalization"])))
        # Compute the dot product of the query vector and the document vector.
        # (numerator of tfidf equation)
        # dot_prod = numpy.dot(doc_vector, query_vector)

    # compute the normalization factor of the query
    # The normalization factor for the query is the length of the query vector,
    # which is the sum-of-squares of the query vector
    query_norm = 0.0
    for item in query_vector:
        query_norm += item**2
    query_norm = math.sqrt(query_norm)
    return docquery2(hit_list, query_vector, thedocvec, query_norm, weight)


def docquery2(hit_list, query_vector, thedocvec, query_norm, weight):
    """Calculate in vectors two."""
    final_ranks = []
    for docid in hit_list:
        dot_prod = 0.0
        doc_norm = thedocvec[docid][0][1]
        for i, qval in enumerate(query_vector):
            dot_prod += qval * thedocvec[docid][i][0]

        # Calculate tfidf
        tfidf = dot_prod / (query_norm * math.sqrt(doc_norm))

        # calculate weighted score
        # for docid in hit_list:
        chunk_one = weight * index.pagerank[int(docid)]
        chunk_two = (1.0 - weight) * tfidf
        first_half_score = chunk_one + chunk_two

        final_ranks.append((first_half_score, docid))
    return final_ranks
