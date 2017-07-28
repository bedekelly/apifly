from functools import wraps
from flask import request


def converter(content_type, default=False):
    """
    Define a decorator to register a function as being the converter
    for a particular content-type.

    For example, when a client requests a response type of "text/html", the
    function to handle this response might be registered as follows:
    
    @converter("text/html")
    def to_html(content):
        return f"<html><pre>{content}</pre></html>"

    If `default` is provided, the function decorated will also be used
    for any unknown or unprovided content types.
    """

    # Attach a `funcs` property to this decorator for convenient access.
    try:
        funcs = converter.funcs
    except AttributeError:
        funcs = converter.funcs = {}

    def decorator(fn):
        """
        This decorator will actually be applied to our 'transformer' function,
        but won't affect its behaviour other than registering it for later use
        For that reason, we don't need to define a function inside this one.
        """
        converter.funcs[content_type] = fn
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

    For example, to indicate that a view should be served as XML and JSON:

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
                A simple error response for when the client provides an
                invalid Accept header, or one this API doesn't currently
                support.
                """
                return jsonify(
                    error="No handler found for Accept header provided!")

            # Given the Accept header, produce an acceptable response.
            response_type = request.headers.get("Accept", "*/*").split(",")[0]
            converter_func = converter.funcs.get(
                response_type, converter.funcs["*/*"])
            original_data = fn(*args, **kwargs)
            return converter_func(original_data)

        return decorated
    return decorator

