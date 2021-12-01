def read_lines(filename):
    with open(filename, 'r') as file:
        return file.read().splitlines()