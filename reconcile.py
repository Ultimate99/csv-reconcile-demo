"""Compare two CSV exports locally by a unique key; Python 3.10+, no dependencies."""
import argparse
import csv
import json
import sys
from pathlib import Path


def read_rows(path, key):
    with open(path, encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        headers = reader.fieldnames or []
        if not headers or len(set(headers)) != len(headers) or any(not h for h in headers):
            raise ValueError(f"{path}: missing, blank or duplicate column headers")
        if key not in headers:
            raise ValueError(f"{path}: key column {key!r} missing")
        rows = {}
        for row in reader:
            if None in row or any(v is None for v in row.values()):
                raise ValueError(f"{path}: malformed record ending at line {reader.line_num}")
            identity = row[key]
            if not identity.strip() or identity in rows:
                raise ValueError(f"{path}: blank or duplicate key at line {reader.line_num}")
            rows[identity] = row
        return headers, rows


def compare(left, right, key):
    lh, lr = read_rows(left, key)
    rh, rr = read_rows(right, key)
    if set(lh) != set(rh):
        raise ValueError("Column sets differ; map column names before comparing")
    changes = []
    matched = 0
    for identity in sorted(lr.keys() | rr.keys()):
        if identity not in lr:
            changes.append({"key": identity, "status": "right_only", "right": rr[identity]})
        elif identity not in rr:
            changes.append({"key": identity, "status": "left_only", "left": lr[identity]})
        else:
            fields = {f: {"left": lr[identity][f], "right": rr[identity][f]}
                      for f in lh if lr[identity][f] != rr[identity][f]}
            if fields:
                changes.append({"key": identity, "status": "changed", "fields": fields})
            else:
                matched += 1
    return {"summary": {"left_rows": len(lr), "right_rows": len(rr),
                        "matched": matched, "differences": len(changes)}, "changes": changes}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("left", type=Path)
    parser.add_argument("right", type=Path)
    parser.add_argument("--key", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        report = compare(args.left, args.right, args.key)
        # Exclusive creation prevents overwriting an input or an earlier report.
        with args.output.open("x", encoding="utf-8") as handle:
            json.dump(report, handle, indent=2, ensure_ascii=False)
            handle.write("\n")
        print(json.dumps(report["summary"]))
        return 0
    except (OSError, ValueError, csv.Error) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
