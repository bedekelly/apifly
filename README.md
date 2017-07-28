# APIfly

_Serve your API in different formats depending on the request_

Example use case: display a formatted HTML page with documentation to a request from a browser, but the pure JSON data to a request from curl.

This relies on the `Accept` header being set, which browsers do automatically for HTML data. Defaults can also be set for clients like curl where setting headers might be an annoyance.

Some rough sample code shown below, and a slightly more complete MVP given in `run.py` for CSV, JSON and HTML.


```
...

@converter("html")
def to_html(content):
    return (
        "<html><body><pre>"
        + content
 	+ "</pre></body></html>"
    )"


@converter("json")
def to_json(content, default=True):
    return flask.jsonify(content)


@app.route("/")
@expose_as("json", "html")
def display_content():
    return {'a': 1, 'b': 2, 'c': 3}
```
