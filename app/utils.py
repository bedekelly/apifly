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
