"""
Search index (main) view.

URLs include:
/
"""
import threading
import heapq
import search
import requests
import flask


@search.app.route('/', methods=['GET'])
def get_results():
    """Docstring for app route."""
    # print("entered get results")

    # parse parameters
    query = flask.request.args.get("q")
    weight = flask.request.args.get("w", default=0.5)
    # print(query)
    # print(weight)

    context = {
        "search_results": [],
        "num_results": 0,
        "query": query,
        "weight": weight
    }

    if query is None:
        print("query is none here")
        return flask.render_template("search.html", **context), 200
    # print("32")

    # connect to index servers, create rest api request
    rest_api_urls = search.app.config['SEARCH_INDEX_SEGMENT_API_URLS']

    threads = []
    search_results = []
    for url in rest_api_urls:
        # print("Connect to url")
        thread = threading.Thread(target=get_index,
                                  args=(query, weight, url, search_results))
        threads.append(thread)
        thread.start()
    # Join all threads together
    for thread in threads:
        thread.join()

    connection = search.model.get_db()
    for searcher in heapq.merge(*search_results, key=lambda x:
                                x["score"], reverse=True):

        # Use doc_id to look up relevant info in database
        # Connect to database
        cur = connection.execute(
            "SELECT * FROM Documents WHERE docid = ?",
            (searcher["docid"], )
        )
        document = cur.fetchone()
        if len(context["search_results"]) < 10:
            context["search_results"].append({
                "doc_url": document["url"],
                "doc_title": document["title"],
                "doc_summary": document["summary"]
            })
    # Use threads to concurrently hit servers
    # parse rest api request
    # Consider using the heapq.merge() function to combine the
    # results of several Index servers
    # context = {
    #     "search_results": search_results,
    #     "num_results": len(search_results)
    # }
    # print("it here gere")
    context["num_results"] = len(context["search_results"])
    return flask.render_template("search.html", **context)


def get_index(query, weight, url, search_results):
    """Capture index and append to search."""
    # Pass in parameters to index API
    params = {'q': query, 'w': weight}

    # Get information from API, r is response
    response = requests.get(url, params=params, timeout=100)
    # print(response)

    # doc_id = response["hits"]["doc_id"]
    # score = response["hits"]["score"]
    if response:
        search_results.append(response.json()["hits"])
