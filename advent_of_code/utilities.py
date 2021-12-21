def read_lines(filename):
    with open(filename, 'r') as file:
        return file.read().splitlines()


def read_blocks(filepath):
    lines = read_lines(filepath)
    blocks = [[]]
    for line in lines:
        if len(line) != 0:
            blocks[-1].append(line)
        else:
            blocks.append([])
    return blocks
