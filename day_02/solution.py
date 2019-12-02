
def adder(prog):
	def add(a, b, c):
		prog[c] = prog[a] + prog[b]
	return add


def multiplier(prog):
	def mul(a, b, c):
		prog[c] = prog[a] * prog[b]
	return mul


class Halt(Exception):
	pass


def halt(*args):
	raise Halt('Halt!')


def run(prog):
	opcodes = {
			1: adder(prog),
			2: multiplier(prog),
			99: halt,
			}
	pc = 0
	while True:
		try:
			opcodes[prog[pc]](*prog[pc+1:pc+4])
			pc += 4
		except Halt:
			return prog[0]
		except KeyError as e:
			print('bad opcode:', prog[pc])
			raise e


p0 = [1, 0, 0, 0, 99]
assert run(p0) == 2 and p0 == [2, 0, 0, 0, 99]
p0 = [2, 3, 0, 3, 99]
assert run(p0) == 2 and p0 == [2, 3, 0, 6, 99]
p0 = [2, 4, 4, 5, 99, 0]
assert run(p0) == 2 and p0 == [2, 4, 4, 5, 99, 9801]
p0 = [1, 1, 1, 4, 99, 5, 6, 0, 99]
assert run(p0) == 30 and p0 == [30, 1, 1, 4, 2, 5, 6, 0, 99]

with open('input.txt') as f:
	program = [int(x) for x in f.read().split(',')]

program[1] = 12
program[2] = 2
print('Day 2, part 1:', run(program))

