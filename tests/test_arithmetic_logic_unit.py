import unittest
from advent_of_code.utilities import read_lines
import z3

MIN_VALUE = 11111111111111
MAX_VALUE = 99999999999999


class Alu:
    def __init__(self):
        self.memory = {
            'w': 0,
            'x': 0,
            'y': 0,
            'z': 0
        }

    def execute_instruction(self, instruction, numbers):
        match = instruction.split()
        operation = match[0]
        first = match[1]
        if operation == 'inp':
            number = int(numbers.pop(0))
            self.memory[first] = number
            return

        second = match[2]
        if operation == 'add':
            if second in self.memory.keys():
                self.memory[first] = self.memory[first] + self.memory[second]
            else:
                self.memory[first] = self.memory[first] + int(second)
        elif operation == 'mul':
            if second in self.memory.keys():
                self.memory[first] = self.memory[first] * self.memory[second]
            else:
                self.memory[first] = self.memory[first] * int(second)
        elif operation == 'div':
            if second in self.memory.keys():
                self.memory[first] = self.memory[first] // self.memory[second]
            else:
                self.memory[first] = self.memory[first] // int(second)
        elif operation == 'mod':
            if second in self.memory.keys():
                self.memory[first] = self.memory[first] % self.memory[second]
            else:
                self.memory[first] = self.memory[first] % int(second)
        elif operation == 'eq':
            if second in self.memory.keys():
                self.memory[first] = 1 if self.memory[first] == self.memory[second] else 0
            else:
                self.memory[first] = 1 if self.memory[first] == int(second) else 0


class ArithmeticLogicUnit(unittest.TestCase):
    def test_run_instructions(self):
        alu_input = [
            'inp w',
            'add z w',
            'mod z 2',
            'div w 2',
            'add y w',
            'mod y 2',
            'div w 2',
            'add x w',
            'mod x 2',
            'div w 2',
            'mod w 2'
        ]
        alu = Alu()
        for instruction in alu_input:
            alu.execute_instruction(instruction, ['10'])
        self.assertEqual({'w': 1, 'x': 0, 'y': 1, 'z': 0}, alu.memory)

    def test_puzzle1(self):
        alu_input = read_lines('input_day24.txt')
        self.assertEqual(93959993429899, find_max(alu_input))


def find_max(alu_input):
    solver = z3.Optimize()

    digits = [z3.BitVec(f'd{i}', 64) for i in range(14)]
    for d in digits:
        solver.add(1 <= d)
        solver.add(d <= 9)
    digit_input = iter(digits)

    registers = {r: 0 for r in 'xyzw'}

    for i, instruction in enumerate(alu_input):
        inst = instruction.split()
        if inst[0] == 'inp':
            registers[inst[1]] = next(digit_input)
            continue
        a, b = inst[1:]
        b = registers[b] if b in registers else int(b)
        c = z3.BitVec(f'v{i}', 64)
        if inst[0] == 'add':
            solver.add(c == registers[a] + b)
        elif inst[0] == 'mul':
            solver.add(c == registers[a] * b)
        elif inst[0] == 'mod':
            solver.add(registers[a] >= 0)
            solver.add(b > 0)
            solver.add(c == registers[a] % b)
        elif inst[0] == 'div':
            solver.add(b != 0)
            solver.add(c == registers[a] / b)
        elif inst[0] == 'eql':
            solver.add(c == z3.If(registers[a] == b, z3.BitVecVal(1, 64), 0))
        registers[a] = c
    solver.add(registers['z'] == 0)
    
    solver.push()
    solver.maximize(sum((10 ** i) * d for i, d in enumerate(digits[::-1])))
    if not solver.check() == z3.sat:
        raise 'Impossible to find a solution!'
    model = solver.model()
    return int(''.join([str(model[d]) for d in digits]))
