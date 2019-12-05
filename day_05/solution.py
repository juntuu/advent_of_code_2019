
class Intcode:
	def __init__(self, fd0=None, fd1=None):
		self.fd0 = fd0 or (lambda: int(input('in > ')))
		self.fd1 = fd1 or (lambda x: print('out>', x))

	def values(self, *modes):
		vs = []
		for i, m in enumerate(modes):
			v = self.prog[self.ip + 1 + i]
			if m == 0:
				v = self.prog[v]
			vs.append(v)
		return vs

	def binop(self, left, right, op):
		a, b, c = self.values(left, right, 1)
		self.prog[c] = op(a, b)
		self.ip += 4

	def io(self, fd, left):
		a = self.values(left)[0]
		if fd == 0:
			self.prog[a] = self.fd0()
		else:
			self.fd1(a)
		self.ip += 2

	def __call__(self, program):
		self.ip = 0
		self.prog = program
		add = lambda a, b: a + b
		mul = lambda a, b: a * b
		opcodes = {
				1: lambda m: self.binop(m % 10, m // 10, add),
				2: lambda m: self.binop(m % 10, m // 10, mul),
				3: lambda _: self.io(0, 1),
				4: lambda m: self.io(1, m % 10),
				}
		while self.prog[self.ip] != 99:
			try:
				code = self.prog[self.ip]
				opcodes[code % 100](code // 100)
			except KeyError as e:
				print('bad opcode:', self.prog[self.ip])
				raise e
			except IndexError as e:
				print('bad access')
				raise e


with open('input.txt') as f:
	program = [int(x) for x in f.read().split(',')]


def gets(seq):
	seq = iter(seq)
	return lambda: next(seq)


def puts(buf):
	return lambda i: buf.append(i)


result = []
computer = Intcode(gets([1]), puts(result))

computer(program[:])
print('Day 5, part 1:', result[-1])

