import unittest

from advent_of_code.utilities import read_lines

HEX_TO_BINARY = {
    '0': '0000',
    '1': '0001',
    '2': '0010',
    '3': '0011',
    '4': '0100',
    '5': '0101',
    '6': '0110',
    '7': '0111',
    '8': '1000',
    '9': '1001',
    'A': '1010',
    'B': '1011',
    'C': '1100',
    'D': '1101',
    'E': '1110',
    'F': '1111'
}


def convert_hex_string(hex_string):
    binary_string = ''
    for c in hex_string:
        binary_string += HEX_TO_BINARY[c]
    return binary_string


def read_headers(binary_packets, headers, index=0):
    if len(binary_packets) == 0:
        return headers
    if all(v == '0' for v in binary_packets):
        return headers
    header = binary_packets[index: index + 3]
    headers.append(int(header, 2))
    index += 3
    type_id_bits = binary_packets[index: index + 3]
    type_id = int(type_id_bits, 2)
    index += 3
    if type_id == 4:
        while binary_packets[index] != '0':
            index += 5
        index += 5
        return read_headers(binary_packets[index:], headers)

    length_type_id = int(binary_packets[index], 2)
    index += 1
    if length_type_id == 0:
        index += 15
        return read_headers(binary_packets[index:], headers)
    index += 11
    return read_headers(binary_packets[index:], headers)


class PacketDecoderTest(unittest.TestCase):
    def test_puzzle1(self):
        raw_packets = read_lines('input_day16.txt')[0]
        headers = []
        read_headers(convert_hex_string(raw_packets), headers)
        self.assertEqual(974, sum(headers))
