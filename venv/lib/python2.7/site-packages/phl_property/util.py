from __future__ import print_function
from datetime import datetime
from sys import stderr, stdin

def construct_layout(cols):
    layout_items = []
    current_position = 0

    # Sort cols by start property
    cols.sort(key=lambda col: col.get('start'))

    for col in cols:
        # If any chars were skipped, add a pad byte
        if col['start'] != current_position:
            skip_chars = col['start'] - current_position
            layout_items.append('{0}x'.format(skip_chars))

        size = col['end'] - col['start']
        format_char = col.get('format', 's')

        # If skip property is True, use the pad format character
        if col.get('skip') == True: format_char = 'x'

        layout_items.append('{0}{1}'.format(size, format_char))

        current_position = col['end']

    return ' '.join(layout_items)

# Gets header names, excluding those being skipped
def get_active_header(cols):
    return [col['name'] for col in cols if col.get('skip') != True]

def get_fields_by_type(cols, type):
    return [col['name'] for col in cols if col.get('type') == type]

def clean_date(input):
    if are_all_chars(input, '0'):
        return ''
    elif input[-2:] == '00':
        input = input[:-2] + '01'
    return datetime.strptime(input, '%Y%m%d').strftime('%Y-%m-%d')

def warning(msg):
    print('Warning: ' + msg, file=stderr)

def are_all_chars(input, char):
    return input == len(input) * char

def get_category_code_desc(category_code):
    return {
        1: 'RESIDENTIAL',
        2: 'HOTELS AND APARTMENTS',
        3: 'STORE WITH DWELLING',
        4: 'COMMERCIAL',
        5: 'INDUSTRIAL',
        6: 'VACANT LAND',
    }.get(category_code, '')

def get_stdin_bytes():
    try: return stdin.buffer  # Py 3
    except: return stdin      # Py 2
