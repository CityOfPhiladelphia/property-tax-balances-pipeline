"""
Street codes parser
File: 'br63trf.stcode'
"""
from struct import Struct
from csv import DictWriter
from sys import stdin, stdout

from .layouts import STREET_CODES_LAYOUT
from .util import construct_layout, get_active_header, get_stdin_bytes

def main():
    layout = construct_layout(STREET_CODES_LAYOUT)
    header = get_active_header(STREET_CODES_LAYOUT)

    # Prepare CSV output to stdout
    writer = DictWriter(stdout, fieldnames=header)
    writer.writeheader()

    parse = Struct(layout).unpack_from

    for line in get_stdin_bytes().readlines():
        # Deconstruct fixed-width string
        row = parse(line)

        # Decode each value
        row = (v.decode('ascii', 'ignore') for v in row)

        # Trim whitespace in each field
        row = [field.strip() for field in row]

        # Convert to dict using header
        row = dict(zip(header, row))

        writer.writerow(row)

if __name__ == '__main__':
    main()
