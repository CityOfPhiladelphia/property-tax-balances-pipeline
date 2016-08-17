"""
Off property parser
File: 'br63trf.offpr'
"""
from struct import Struct, calcsize
from csv import DictWriter
from sys import stdin, stdout

from .layouts import OFF_PROPERTY_LAYOUT
from .util import construct_layout, get_active_header, get_stdin_bytes

def main():
    layout = construct_layout(OFF_PROPERTY_LAYOUT)
    header = get_active_header(OFF_PROPERTY_LAYOUT)

    # Prepare CSV output to stdout
    writer = DictWriter(stdout, fieldnames=header)
    writer.writeheader()

    parse = Struct(layout).unpack_from
    struct_length = calcsize(layout)

    for line in get_stdin_bytes().readlines():
        # Ensure string length is what deconstructer expects
        if len(line) != struct_length:
            line = '{:<{}s}'.format(line.decode(), struct_length).encode()

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
