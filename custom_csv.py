"""
custom_csv.py

CustomCsvReader  - A CSV reader implemented from scratch.
CustomCsvWriter  - A CSV writer implemented from scratch.

This version supports:
- commas
- quoted fields
- escaped quotes ("")
- embedded newlines inside quoted fields
- streaming (reads file gradually)
"""

from typing import IO, Iterable, List


class CustomCsvReader:
    """Simple and correct CSV reader (line-based with multi-line support)."""

    def __init__(self, fh: IO[str]):
        self.fh = fh
        self._finished = False

    def __iter__(self):
        return self

    def __next__(self) -> List[str]:
        if self._finished:
            raise StopIteration

        row: List[str] = []
        field_chars: List[str] = []
        in_quotes = False

        while True:
            line = self.fh.readline()
            if line == "":
                # EOF reached
                if not row and not field_chars:
                    self._finished = True
                    raise StopIteration
                row.append("".join(field_chars))
                self._finished = True
                return row

            i = 0
            while i < len(line):
                ch = line[i]

                # ------------- Inside Quotes -------------
                if in_quotes:
                    if ch == '"':
                        nxt = line[i + 1] if (i + 1) < len(line) else None
                        if nxt == '"':
                            field_chars.append('"')
                            i += 2
                        else:
                            in_quotes = False
                            i += 1
                    else:
                        field_chars.append(ch)
                        i += 1
                # ------------- Outside Quotes -------------
                else:
                    if ch == ',':
                        row.append("".join(field_chars))
                        field_chars = []
                        i += 1

                    elif ch == '"':
                        in_quotes = True
                        i += 1

                    elif ch == '\n':
                        row.append("".join(field_chars))
                        return row

                    else:
                        field_chars.append(ch)
                        i += 1

            # End of line
            if in_quotes:
                # Line continues inside quoted field
                if not line.endswith("\n"):
                    field_chars.append("\n")
            else:
                # Finished row but line had no newline
                row.append("".join(field_chars))
                return row


class CustomCsvWriter:
    """Writes CSV rows, quoting when needed."""

    def __init__(self, fh: IO[str]):
        self.fh = fh

    @staticmethod
    def _needs_quoting(s: str) -> bool:
        return any(ch in s for ch in [",", '"', "\n"])

    @staticmethod
    def _escape_and_quote(s: str) -> str:
        return '"' + s.replace('"', '""') + '"'

    def writerow(self, row: Iterable[str]):
        out = []
        for cell in row:
            cell = "" if cell is None else str(cell)
            if self._needs_quoting(cell):
                out.append(self._escape_and_quote(cell))
            else:
                out.append(cell)
        self.fh.write(",".join(out) + "\n")

    def writerows(self, rows: Iterable[Iterable[str]]):
        for r in rows:
            self.writerow(r)


# Demo when running this file directly
if __name__ == "__main__":
    import io

    sample = io.StringIO('a,"b,1","line\nbreak","He said ""Hi""" ,x\none,two,three\n')

    reader = CustomCsvReader(sample)
    for r in reader:
        print("ROW:", r)
