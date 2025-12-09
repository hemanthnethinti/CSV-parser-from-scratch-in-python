"""Simple tests to validate CustomCsvReader / CustomCsvWriter against stdlib csv."""

import csv
import io
from custom_csv import CustomCsvReader, CustomCsvWriter


def compare_reader(input_text: str):
    """Compare our reader with stdlib csv.reader for given CSV text."""
    a = list(csv.reader(io.StringIO(input_text)))
    b = list(CustomCsvReader(io.StringIO(input_text)))
    print("EXPECTED:", a)
    print("GOT     :", b)
    assert a == b, "Reader mismatch!"


def compare_writer(rows):
    """Write rows with our writer and stdlib, then compare the outputs parsed by stdlib."""
    # Our writer output
    out1 = io.StringIO()
    writer1 = CustomCsvWriter(out1)
    writer1.writerows(rows)
    out1_val = out1.getvalue()

    # Stdlib csv writer output
    out2 = io.StringIO()
    writer2 = csv.writer(out2, lineterminator="\n")
    writer2.writerows(rows)
    out2_val = out2.getvalue()

    print("OUR OUTPUT:")
    print(out1_val)
    print("STD OUTPUT:")
    print(out2_val)

    # Parse both with stdlib and compare parsed rows
    parsed1 = list(csv.reader(io.StringIO(out1_val)))
    parsed2 = list(csv.reader(io.StringIO(out2_val)))
    assert parsed1 == parsed2, "Writer produced CSV that differs after parsing."


if __name__ == "__main__":
    # Some test cases
    cases = [
        'a,b,c\n1,2,3\n',
        'a,"b,1",c\n"x\ny",z,1\n',
        'a,"He said ""Hi""",d\n',
        ',,\n',  # empty fields
    ]
    for c in cases:
        compare_reader(c)

    # test writer
    rows = [
        ["a", 'He said "Hi"', "b,c"],
        ["line\nbreak", "plain", ""],
        ["", "", ""],
    ]
    compare_writer(rows)
    print("All tests passed.")
