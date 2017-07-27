from pprint import pformat
from functools import wraps

from flask import Flask, request, jsonify


app = Flask(__name__)


def converter(content_type, default=False):
    """
    Define a meta-decorator to register a function as being the 'transformation'
    subroutine for a particular data-type.

    For example, when a client requests a response type of "text/html", the
    function to handle this response might be registered as follows:
    
    @converter("text/html")
    def to_html(content):
        return f"<html><pre>{content}</pre></html>"
    """

    # Attach a `funcs` property to this decorator for convenient access.
    try:
        funcs = converter.funcs
    except AttributeError:
        funcs = converter.funcs = {}

    def decorator(fn):
        """
        This decorator will actually be applied to our 'transformer' function,
        but won't affect its behaviour other than registering it for later use.
        
        For that reason, we don't need to define a function inside this one.
        """
        converter.funcs[content_type] = fn

        # The @converter("application/json") syntax doesn't look pretty enough.
        abbreviations = {
            "json": "application/json",
            "csv": "text/csv",
            "html": "text/html"}
        if content_type in abbreviations:
            converter.funcs[abbreviations[content_type]] = fn

        # Some clients may use "*/*" as their default Accept header,
        # some may just leave the header out altogether.
        if default:
            converter.funcs["*/*"] = fn
            converter.funcs[None] = fn

        return fn
    return decorator


def expose_as(*content_types):
    """
    This decorator is used to indicate that a resource, or 'view', should
    be exposed as several different content types.

    For example, to indicate that a view should be served as both XML and JSON:

    @app.route("/api/transactions")
    @expose_as("xml", "json")
    def get_transactions():
        return ...
    """
    
    def decorator(fn):
        @wraps(fn)
        def decorated(*args, **kwargs):
            def error_response(*args, **kwargs):
                """
                A simple error response for when the client provides an invalid Accept
                header, or one this API doesn't currently support.
                """
                return jsonify(error="No handler found for Accept header provided!")

            # Given the Accept header, produce an acceptable response for the client.
            response_type = request.headers.get("Accept", "*/*").split(",")[0]
            print(response_type)
            converter_func = converter.funcs.get(response_type, converter.funcs["*/*"])
            print(converter.funcs)
            original_data = fn(*args, **kwargs)
            return converter_func(original_data)

        return decorated
    return decorator


def csv_tag(header, example_data):
    """
    Utility function to produce a CSV-style header from the text and and example piece of data.
    """
    return header + " ({})".format({
        int: "N",
        str: "S",
        dict: "M"
    }[type(example_data)])


@converter("csv")
def to_csv(content):
    """
    A naîve example converter: from a list of dictionaries to CSV format.
    """
    formatted_headers = []
    header_titles, example_data = zip(*content[0].items())

    for header_title, datum in zip(header_titles, example_data):
        formatted_headers.append(csv_header(header_title, datum))
    rows = [','.join(headers)]

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
        html + "</tr>"
    html += "</table></body></html>"
    return html


@app.route("/")
@expose_as("csv", "json", "html")
def display_content():
    """Some example content intended to be served as CSV, JSON and HTML."""
    return [
        {
            "a": 1, "b": 2
        },
        {
            "a": 3, "b": 4
        },
        {
            "a": 5, "b": 6
        }
    ]


app.run(debug=True)
