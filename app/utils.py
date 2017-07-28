def csv_headers(content):
    """
    Given a list of dictionaries, format & yield each CSV header.
    """
    header_titles, example_data = zip(*content[0].items())
    for header_title, datum in zip(header_titles, example_data):
        yield csv_header(header_title, datum)


def csv_format(headers, content):
    """Generate and join a set of CSV rows and headers."""
    return '\n'.join(csv_rows(headers, content))


def csv_rows(headers, content):
    """Generate a series of CSV rows given its headers and data."""
    yield ','.join(headers)
    for row in content:
        yield ','.join(map(str, row.values()))


def csv_header(header, example_data):
    """
    Utility function to produce a CSV-style header from the
    text and an example piece of data.
    """
    return header + " ({})".format({
        int: "N",
        str: "S",
        dict: "M"
    }[type(example_data)])


def html_table(headers, rows):
    """
    Incredibly naive process to create an HTML table. For
    illustration only.
    """
    html = "<html><body><h1>Your data:</h1><table><tr>"
    for header in headers:
        html += f"<th>{header}</th>"
    html += "</tr>"
    for row in rows:
        html += "<tr>"
        for item in row:
            html += f"<td>{item}</td>"
        html += "</tr>"
    html += "</table></body></html>"
    return html
