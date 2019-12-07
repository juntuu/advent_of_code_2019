
import asyncio
from itertools import count
from collections import namedtuple


def a_fun(f, *args):
	async def fun(*fargs):
		return f(*args, *fargs)
	return fun


class IO(namedtuple('IO', ['get', 'put'])):
	__slots__ = ()

	def __new__(cls, get=None, put=None, *, prompt=('in', 'out')):
		if get is None:
			cin = count(1)
			get = lambda: int(input(f'{prompt[0]} [{next(cin)}]> '))
		if put is None:
			cout = count(1)
			put = lambda i: print(f'{prompt[1]} [{next(cout)}]> {i}')
		return super().__new__(cls, a_fun(get), a_fun(put))


def gets(seq):
	seq = iter(seq)
	return IO(get=lambda: next(seq))


def puts(buf):
	return IO(put=lambda i: buf.append(i))


class Intcode:
	default_id = count()

	def __init__(self, fd0=None, fd1=None, *, name=None):
		self.id = name or f'C_{next(Intcode.default_id)}'
		self.fd0 = fd0 or IO(prompt=(self.id + ' in', ''))
		self.fd1 = fd1 or IO(prompt=('', self.id + ' out'))

	def __call__(self, program):
		return asyncio.run(self.task(program))

	def values(self, *modes):
		vs = []
		for i, m in enumerate(modes):
			v = self.prog[self.ip + 1 + i]
			if m == 0:
				v = self.prog[v]
			vs.append(v)
		return vs

	async def binop(self, left, right, op):
		a, b, c = self.values(left, right, 1)
		self.prog[c] = op(a, b)
		self.ip += 4

	async def io(self, fd, left):
		a = self.values(left)[0]
		if fd == 0:
			self.prog[a] = await self.fd0.get()
		else:
			await self.fd1.put(a)
		self.ip += 2

	async def jump(self, left, right, pred):
		a, b = self.values(left, right)
		if pred(a):
			self.ip = b
		else:
			self.ip += 3

	async def task(self, program):
		self.ip = 0
		self.prog = program
		add = lambda a, b: a + b
		mul = lambda a, b: a * b
		true = lambda x: x
		false = lambda x: not x
		lt = lambda a, b: a < b
		eq = lambda a, b: a == b
		opcodes = {
				1: lambda m: self.binop(m % 10, m // 10, add),
				2: lambda m: self.binop(m % 10, m // 10, mul),
				3: lambda _: self.io(0, 1),
				4: lambda m: self.io(1, m % 10),
				5: lambda m: self.jump(m % 10, m // 10, true),
				6: lambda m: self.jump(m % 10, m // 10, false),
				7: lambda m: self.binop(m % 10, m // 10, lt),
				8: lambda m: self.binop(m % 10, m // 10, eq),
				}
		while self.prog[self.ip] != 99:
			try:
				code = self.prog[self.ip]
				await opcodes[code % 100](code // 100)
			except KeyError as e:
				print('bad opcode:', self.prog[self.ip])
				raise e
			except IndexError as e:
				print('bad access')
				raise e

