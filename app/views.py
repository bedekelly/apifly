from flask import jsonify, request

from .apifly import converter, expose_as
from .utils import csv_header
from . import flask_app as app


@converter("csv")
def to_csv(content):
    """
    A naîve example converter: from a list of dictionaries to CSV format.
    """
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
    """Using Flask's inbuilt object->json converter."""
    return jsonify(content)


@converter("html", default=True)
def to_html(content):
    """
    A naîve example converter: from a list of dictionaries to formatted HTML
    including the JSON response. This could also have included a table of the
    data.
    """
    headers = content[0].keys()
    html = "<html><body><h1>Your data:</h1><table><tr>"
    for header in headers:
        html += f"<th>{header}</th>"
    html += "</tr>"
    for row in content:
        html += "<tr>"
        for item in row.values():
            html += f"<td>{item}</td>"
        html += "</tr>"
    html += "</table></body></html>"
    return html


@app.route("/")
@expose_as("csv", "json", "html")
def display_content():
    """Some example content intended to be served as CSV, JSON and HTML."""
    return [{"a": 1, "b": 2},
            {"a": 3, "b": 4},
            {"a": 5, "b": 6}]
