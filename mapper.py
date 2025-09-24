#!/usr/bin/env python3
import sys

def main():
    for line in sys.stdin:

        try:
            line = line.strip()
            if not line:
                continue
            parts = line.split(',')
            if len(parts) == 3:
                client_id, feature_value, _ = parts
                # Possibly check if they are valid or skip if not
                if client_id == "client_id" and feature_value == "feature_value":
                    continue

                print("{}\t{},1".format(client_id, feature_value))
        except Exception as e:
            sys.stderr.write("Exception in mapper: {}\n".format(str(e)))
            sys.stderr.write("Offending line: {}\n".format(line))
            exit(2)



if __name__ == "__main__":
    main()
