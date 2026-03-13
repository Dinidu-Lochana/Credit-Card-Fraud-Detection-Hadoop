#!/usr/bin/env python
"""
Mapper: Fraud Rate per Amount Range
Dataset: creditcard.csv (284,807 rows)
Input:  Time, V1..V28, Amount, Class
Output: amount_range \t class (0 or 1)
"""

import sys


def get_amount_bucket(amount):
    if amount < 10:
        return "1_Bucket_$0-$10"
    elif amount < 50:
        return "2_Bucket_$10-$50"
    elif amount < 100:
        return "3_Bucket_$50-$100"
    elif amount < 500:
        return "4_Bucket_$100-$500"
    elif amount < 1000:
        return "5_Bucket_$500-$1000"
    else:
        return "6_Bucket_$1000+"


first_line = True

for line in sys.stdin:
    line = line.strip()

    if not line:
        continue

    # Skip header row
    if first_line:
        first_line = False
        if "Time" in line and "Amount" in line:
            continue

    fields = line.split(",")

    if len(fields) < 31:
        continue

    try:
        amount = float(fields[29].strip().replace('"', ''))
        cls    = int(fields[30].strip().replace('"', ''))

        bucket = get_amount_bucket(amount)

        print("{0}\t{1}".format(bucket, cls))

    except ValueError:
        continue
