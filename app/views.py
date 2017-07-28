from flask import jsonify, request

from .apifly import converter, expose_as
from .utils import csv_header, html_table
from . import flask_app as app


@converter("csv")
def to_csv(content):
    """Expose the content as a CSV file."""
    formatted_headers = []
    header_titles, example_data = zip(*content[0].items())

    for header_title, datum in zip(header_titles, example_data):
        formatted_headers.append(csv_header(header_title, datum))
    rows = [','.join(formatted_headers)]

    for row in content:
        rows.append(','.join(map(str, row.values())))

    return '\n'.join(rows)


@converter("json")
def to_json(content):
    """Expose the content as a JSON document."""
    return jsonify(data=content)


@converter("html", default=True)
def to_html(content):
    """
    Return the content as a formatted HTML table for browsers.
    """
    headers = content[0].keys()
    rows = (r.values() for r in content)
    return html_table(headers, rows)
    


@app.route("/")
@expose_as("csv", "json", "html")
def display_content():
    """Some example content intended to be served as CSV, JSON and HTML."""
    return [{"a": 1, "b": 2},
            {"a": 3, "b": 4},
            {"a": 5, "b": 6}]

@app.route("/me")
def other():
    return "Hello, world!"
