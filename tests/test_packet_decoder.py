import unittest

from advent_of_code.utilities import read_lines


class Number:
    def __init__(self, value):
        self.value = value

    def calculate(self):
        return self.value

    def __str__(self):
        return f"{self.calculate()}"

    def __repr__(self):
        return f"{self.calculate()}"


class Sum:
    def __init__(self, operands):
        self.operands = operands

    def calculate(self):
        value = 0
        for op in self.operands:
            value += op.calculate()
        return value


class Product:
    def __init__(self, operands):
        self.operands = operands

    def calculate(self):
        value = 1
        for op in self.operands:
            value *= op.calculate()
        return value


class Minimum:
    def __init__(self, operands):
        self.operands = operands

    def calculate(self):
        return min([o.calculate() for o in self.operands])


class Maximum:
    def __init__(self, operands):
        self.operands = operands

    def calculate(self):
        return max([o.calculate() for o in self.operands])


class Less:
    def __init__(self, operands):
        if len(operands) != 2:
            raise 'Max two operands!'
        self.operands = operands

    def calculate(self):
        if self.operands[0].calculate() < self.operands[1].calculate():
            return 1
        return 0


class Greater:
    def __init__(self, operands):
        if len(operands) != 2:
            raise 'Max two operands!'
        self.operands = operands

    def calculate(self):
        if self.operands[0].calculate() > self.operands[1].calculate():
            return 1
        return 0


class Equal:
    def __init__(self, operands):
        if len(operands) != 2:
            raise 'Max two operands!'
        self.operands = operands

    def calculate(self):
        if self.operands[0].calculate() != self.operands[1].calculate():
            return 0
        return 1


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


def read_packet_versions(binary_packets, headers, index=0):
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
        return read_packet_versions(binary_packets[index:], headers)

    length_type_id = int(binary_packets[index], 2)
    index += 1
    if length_type_id == 0:
        index += 15
        return read_packet_versions(binary_packets[index:], headers)
    index += 11
    return read_packet_versions(binary_packets[index:], headers)


def parse_packet(packet):
    expression_type = int(packet[3:6], 2)
    packet = packet[6:]
    if expression_type == 4:
        number, packet = read_number(packet)
        return Number(number), packet

    operands, packet = read_operands(packet)
    if expression_type == 0:
        return Sum(operands), packet
    if expression_type == 1:
        return Product(operands), packet
    if expression_type == 2:
        return Minimum(operands), packet
    if expression_type == 3:
        return Maximum(operands), packet
    if expression_type == 6:
        return Less(operands), packet
    if expression_type == 5:
        return Greater(operands), packet
    if expression_type == 7:
        return Equal(operands), packet


def read_operands(packet):
    length_type = packet[0]
    packet = packet[1:]
    if length_type == '0':
        sub_packet_length = int(packet[: 15], 2)
        packet = packet[15:]
        sub_packets = packet[:sub_packet_length]
        packet = packet[sub_packet_length:]
        operands = []
        while len(sub_packets) != 0:
            (n, sub_packets) = parse_packet(sub_packets)
            operands.append(n)
        return operands, packet

    number_of_packets = int(packet[: 11], 2)
    packet = packet[11:]
    operands = []
    for _ in range(number_of_packets):
        (n, packet) = parse_packet(packet)
        operands.append(n)
    return operands, packet


def read_number(packet):
    number = ''
    while packet[0] != '0':
        number += packet[1:  5]
        packet = packet[5:]
    number += packet[1:  5]
    return int(number, 2), packet[5:]


class PacketDecoderTest(unittest.TestCase):
    def test_puzzle1(self):
        raw_packets = read_lines('input_day16.txt')[0]
        self.assertEqual(974, sum(read_packet_versions(convert_hex_string(raw_packets), [])))

    def test_number_packet(self):
        packet = convert_hex_string('D2FE28')
        (operation, _) = parse_packet(packet)
        self.assertEqual(2021, operation.calculate())

    def test_sum_packet(self):
        packet = convert_hex_string('C200B40A82')
        (operation, _) = parse_packet(packet)
        self.assertEqual(3, operation.calculate())

    def test_product_packet(self):
        packet = convert_hex_string('04005AC33890')
        (operation, _) = parse_packet(packet)
        self.assertEqual(54, operation.calculate())

    def test_minimum_packet(self):
        packet = convert_hex_string('880086C3E88112')
        (operation, _) = parse_packet(packet)
        self.assertEqual(7, operation.calculate())

    def test_maximum_packet(self):
        packet = convert_hex_string('CE00C43D881120')
        (operation, _) = parse_packet(packet)
        self.assertEqual(9, operation.calculate())

    def test_less_packet(self):
        packet = convert_hex_string('D8005AC2A8F0')
        (operation, _) = parse_packet(packet)
        self.assertEqual(1, operation.calculate())

    def test_greater_packet(self):
        packet = convert_hex_string('F600BC2D8F')
        (operation, _) = parse_packet(packet)
        self.assertEqual(0, operation.calculate())

    def test_equal_packet(self):
        packet = convert_hex_string('9C005AC2F8F0')
        (operation, _) = parse_packet(packet)
        self.assertEqual(0, operation.calculate())

    def test_complex_scenario(self):
        packet = convert_hex_string('9C0141080250320F1802104A08')
        (operation, _) = parse_packet(packet)
        self.assertEqual(1, operation.calculate())

    def test_puzzle2(self):
        raw_packets = read_lines('input_day16.txt')[0]
        packet = convert_hex_string(raw_packets)
        (operation, _) = parse_packet(packet)
        self.assertEqual(180616437720, operation.calculate())
