#!/usr/bin/env python3
import sys

def main():
    current_client = None
    sum_feature_values = 0.0
    count = 0

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue

        # Example line => "client1    10.5,1"
        client_id, value_str = line.split('\t', 1)
        
        # value_str => "10.5,1"
        feature_value_str, occur_str = value_str.split(',', 1)
        
        try:
            feature_value = float(feature_value_str)
            occur = int(occur_str)
        except ValueError:
            # If there's parsing error, skip or handle gracefully
            continue

        if current_client == client_id:
            # Same client_id; accumulate
            sum_feature_values += feature_value
            count += occur
        else:
            # New client_id; output the previous client's aggregates first
            if current_client is not None:
                print("{}\t{}\t{}".format(current_client, sum_feature_values, count))

            # Reset for the new client_id
            current_client = client_id
            sum_feature_values = feature_value
            count = occur

    # Print the last client’s result if it exists
    if current_client is not None:
        print("{}\t{}\t{}".format(current_client, sum_feature_values, count))

if __name__ == "__main__":
    main()
