#!/usr/bin/env python
"""
Reducer: Fraud Rate per Amount Range
Input:  amount_range \t class   (sorted by amount_range)
Output: amount_range, total_transactions, fraud_count, normal_count, fraud_rate_%
"""

import sys


current_bucket = None
total_count    = 0
fraud_count    = 0


def emit(bucket, total, fraud):
    normal     = total - fraud
    fraud_rate = (fraud / float(total) * 100) if total > 0 else 0.0
    print("{0}\t{1}\t{2}\t{3}\t{4:.4f}%".format(bucket, total, fraud, normal, fraud_rate))


for line in sys.stdin:
    line = line.strip()

    if not line:
        continue

    parts = line.split("\t")

    if len(parts) != 2:
        continue

    try:
        bucket = parts[0]
        cls    = int(parts[1])
    except ValueError:
        continue

    if bucket == current_bucket:
        total_count += 1
        fraud_count += cls
    else:
        if current_bucket is not None:
            emit(current_bucket, total_count, fraud_count)

        current_bucket = bucket
        total_count    = 1
        fraud_count    = cls

if current_bucket is not None:
    emit(current_bucket, total_count, fraud_count)
