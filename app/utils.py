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
