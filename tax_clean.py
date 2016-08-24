#!/usr/bin/env python

import sys
import csv
from decimal import Decimal
from collections import defaultdict

SOURCE_COLS = [
  'parcel_number',
  'lien_number',
  'tax_period',
  'principal',
  'interest',
  'penalty',
  'other',
  'total',
]

OUTPUT_COLS = [
  'record_id',
  'parcel_number',
  'tax_period',
  'principal',
  'interest',
  'penalty',
  'other',
  'total',
  'lien_number',
]

CURRENCY_COLS = [
  'principal',
  'interest',
  'penalty',
  'other',
  'total',
]

def exclude_null_bytes(line):
  return line.replace('\x00', '')

# TODO: Verify field names

reader = csv.reader((exclude_null_bytes(line) for line in sys.stdin), delimiter=';')

# Skip header row
reader.next()

grouped_dict = defaultdict(lambda: {
  'principal': Decimal(0),
  'interest': Decimal(0),
  'penalty': Decimal(0),
  'other': Decimal(0),
  'total': Decimal(0),
  'lien_number': [],
})

# Loop through lines in file
for row in reader:
  # Trim whitespace in each field and remove last column (it's empty)
  row = [field.strip() for field in row[:-1]]

  # Convert row to a dict
  row = dict(zip(SOURCE_COLS, row))

  # Strip month and day from tax period, leaving only the year
  row['tax_period'] = row['tax_period'][:4]

  # Group by parcel number and tax period, summing the numeric columns
  group = grouped_dict[(row['parcel_number'], row['tax_period'])]

  # Store lien numers in an array in case there are more than one per parcel+period
  if row['lien_number']:
    group['lien_number'].append(row['lien_number'])

  for key in CURRENCY_COLS:
    # If there's a minus at the end, move it to the front so it can be parsed
    if row[key][-1] == '-':
      row[key] = '-' + row[key][:-1]

    group[key] += Decimal(row[key])

# Prepare CSV output to stdout
writer = csv.DictWriter(sys.stdout, fieldnames=OUTPUT_COLS)
writer.writeheader()

for key, values in grouped_dict.iteritems():
  # Put grouped_dict key into each dict and convert it to list of dicts
  key_as_items = dict(zip(['parcel_number', 'tax_period'], key))
  values.update(key_as_items)

  # Add record_id column consisting of parcel_number and tax_period
  values['record_id'] = ''.join(key)

  # Convert lien_number to comma-separated string (for edge cases)
  values['lien_number'] = ', '.join(values['lien_number'])
  # grouped_rows.append(values)
  writer.writerow(values)
