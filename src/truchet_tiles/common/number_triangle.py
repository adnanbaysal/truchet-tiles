from functools import cache


class NumberTriangle:
    def __init__(
        self,
        as_rows: list[list[int]] | None = None,
        as_sequence: list[int] | None = None,
    ) -> None:
        if as_rows is None and as_sequence is None:
            raise ValueError("Either as_rows or as_sequence must be provided")

        if as_rows is not None and as_sequence is not None:
            raise ValueError("Only one of as_rows or as_sequence can be provided")

        if as_rows is not None:
            self.as_rows = as_rows
            self.as_sequence = self.rows_to_sequence(as_rows)

        elif as_sequence is not None:
            self.as_sequence = as_sequence
            self.as_rows = self.sequence_to_rows(as_sequence)

    @classmethod
    def from_sequence(cls, sequence: list[int]) -> "NumberTriangle":
        return cls(as_sequence=sequence)

    @classmethod
    def from_rows(cls, rows: list[list[int]]) -> "NumberTriangle":
        return cls(as_rows=rows)

    @staticmethod
    def rows_to_sequence(rows: list[list[int]]) -> list[int]:
        return [number for row in rows for number in row]

    @staticmethod
    def sequence_to_rows(sequence: list[int]) -> list[list[int]]:
        rows = []
        index = 0
        row_size = 1

        while index < len(sequence):
            rows.append(sequence[index : index + row_size])
            index += row_size
            row_size += 1

        return rows

    def __str__(self) -> str:
        last_row = " ".join(str(number) for number in self.as_rows[-1])
        row_width = len(last_row)
        out = ""

        for row in self.as_rows:
            row_str = " ".join(str(number) for number in row)
            out += row_str.center(row_width) + "\n"

        return out


@cache
def get_pascal_triangle(height: int) -> NumberTriangle:
    rows = [[1]]
    for i in range(1, height):
        row = [1]
        for j in range(1, i):
            row.append(rows[i - 1][j - 1] + rows[i - 1][j])

        row.append(1)
        rows.append(row)

    return NumberTriangle(as_rows=rows)


@cache
def get_hosoya_triangle(height: int) -> NumberTriangle:
    rows = [[1] * (i + 1) for i in range(height)]

    for row in range(2, height):
        edge_value = rows[row - 1][-1] + rows[row - 2][-1]
        rows[row][-1] = edge_value
        if row < height - 1:
            rows[row + 1][-2] = edge_value

    for col in range(height):
        for row in range(col + 2, height):
            rows[row][col] = rows[row - 1][col] + rows[row - 2][col]

    return NumberTriangle(as_rows=rows)


@cache
def get_baysal_triangle(height: int) -> NumberTriangle:
    rows = [[1] * (i + 1) for i in range(height)]

    for row in range(2, height):
        for col in range(1, row):
            rows[row][col] = rows[row - 1][col - 1] + rows[row - 1][col]

        edge_value = rows[row - 1][0] + rows[row][1]
        rows[row][0] = edge_value
        rows[row][-1] = edge_value

    return NumberTriangle(as_rows=rows)


bt = get_baysal_triangle(8)
print(bt)
print("\n".join([str(row) for row in bt.as_rows]))
print(bt.as_sequence)
