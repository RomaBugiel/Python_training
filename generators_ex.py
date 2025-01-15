# Generators in Python
# ---------------------
# Generators are a type of iterable, like lists or tuples, but they don't store all their values in memory.
# Instead, they generate values on the fly using the `yield` keyword.
# Generators are especially useful when working with large datasets or streams of data, as they allow for
# memory-efficient iteration. They are defined like regular functions but use `yield` instead of `return`.
# Examples of use cases include reading large files, processing streams, or generating infinite sequences.

def odd_lines_with_numbers(file_path: str):
    with open(file_path, 'r') as file:
        for line_number, line in enumerate(file, start=1):
            if line_number % 2 != 0:
                yield f"{line_number}: {line.strip()}"


file_path = "example.txt"

for odd_line in odd_lines_with_numbers(file_path):
    print(odd_line)


# reminder: enumerate - fuction that applies indexing for each elemenet of iterable object. Returns tuple [krotke] in format: (intex, element)
