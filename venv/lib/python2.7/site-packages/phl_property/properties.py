"""
Properties file parser
File: 'br63trf.os13sd'
"""
from struct import Struct
from csv import DictWriter
from sys import stdin, stdout

from .layouts import PROPERTIES_LAYOUT
from .util import (construct_layout, get_active_header, get_fields_by_type,
                   clean_date, are_all_chars, get_category_code_desc, warning,
                   get_stdin_bytes)

def main():
    layout = construct_layout(PROPERTIES_LAYOUT)
    header = get_active_header(PROPERTIES_LAYOUT)
    output_header = header + ['category_code_description']

    date_fields = get_fields_by_type(PROPERTIES_LAYOUT, 'date')
    numeric_fields = get_fields_by_type(PROPERTIES_LAYOUT, 'number')

    # Prepare CSV output to stdout
    writer = DictWriter(stdout, fieldnames=output_header)
    writer.writeheader()

    parse = Struct(layout).unpack_from

    for line in get_stdin_bytes().readlines():
        # Deconstruct fixed-width string
        row = parse(line)

        # Decode each value
        row = (v.decode('ascii', 'ignore') for v in row)

        # Trim whitespace in each field
        row = (field.strip() for field in row)

        # Convert to dict using headers
        row = dict(zip(header, row))

        # Format date fields
        for field in date_fields:
            if row[field] == '': continue
            try:
                row[field] = clean_date(row[field])
            except ValueError:
                warning('[{0}] Invalid date conversion of {1} for "{2}"'.format(
                    row['PARCEL'], field, row[field]))

        # Enforce numeric fields
        for field in numeric_fields:
            if row[field] == '': continue
            try:
                row[field] = int(row[field])
            except ValueError:
                warning('[{0}] Invalid integer conversion of {1} for "{2}"'.format(
                    row['PARCEL'], field, row[field]))
                row[field] = 0

        # Strip leading zeros from other non-numeric fields
        for field in ['UNIT']:
            row[field] = row[field].lstrip('0')

        # Empty fields of all zeros
        for field in ['YR_BUILT', 'BK_PG']:
            if are_all_chars(row[field], '0'): row[field] = ''

        # Fix math of some fields -- Mainframe stores 10 or 100
        # times the actual value so that it can avoid decimals
        # points (wastes of space).
        for field in ['TOT_AREA', 'FRT', 'DPT']:  # total area, frontage, depth
            if row[field] > 0: row[field] /= 100
        for field in ['NO_BATH', 'NO_BD', 'NO_RM', 'STORIES']: # num of bath, bed, room, stories
            if row[field] > 0: row[field] /= 10

        # Add category code description from lookup dict
        row['category_code_description'] = get_category_code_desc(row['CAT_CD'])

        writer.writerow(row)

if __name__ == '__main__':
    main()
