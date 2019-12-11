
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


class Mem(dict):
	__slots__ = ()

	def __setitem__(self, i, val):
		assert i >= 0
		return super().__setitem__(i, val)

	def __getitem__(self, i):
		assert i >= 0
		try:
			return super().__getitem__(i)
		except KeyError:
			self[i] = 0
			return 0


class Intcode:
	default_id = count()

	def __init__(self, fd0=None, fd1=None, *, name=None):
		self.id = name or f'C_{next(Intcode.default_id)}'
		self.fd0 = fd0 or IO(prompt=(self.id + ' in', ''))
		self.fd1 = fd1 or IO(prompt=('', self.id + ' out'))

	def __call__(self, program):
		return asyncio.run(self.task(program))

	def addrs(self, m, n):
		a = []
		for i in range(1, n + 1):
			m, x = divmod(m, 10)
			if x == 0:
				v = self.prog[self.ip + i]
			elif x == 1:
				v = self.ip + i
			elif x == 2:
				v = self.base + self.prog[self.ip + i]
			a.append(v)
		if n == 1:
			return a[0]
		return a

	async def binop(self, m, op):
		a, b, c = self.addrs(m, 3)
		self.prog[c] = op(self.prog[a], self.prog[b])
		self.ip += 4

	async def io(self, fd, m):
		a = self.addrs(m, 1)
		if fd == 0:
			self.prog[a] = await self.fd0.get()
		else:
			await self.fd1.put(self.prog[a])
		self.ip += 2

	async def jump(self, m, pred):
		a, b = self.addrs(m, 2)
		if pred(self.prog[a]):
			self.ip = self.prog[b]
		else:
			self.ip += 3

	async def set_base(self, m):
		a = self.addrs(m, 1)
		self.base += self.prog[a]
		self.ip += 2

	async def task(self, program):
		self.ip = 0
		self.base = 0
		self.prog = Mem(enumerate(program))
		add = lambda a, b: a + b
		mul = lambda a, b: a * b
		true = lambda x: x
		false = lambda x: not x
		lt = lambda a, b: a < b
		eq = lambda a, b: a == b
		opcodes = {
				1: lambda m: self.binop(m, add),
				2: lambda m: self.binop(m, mul),
				3: lambda m: self.io(0, m),
				4: lambda m: self.io(1, m),
				5: lambda m: self.jump(m, true),
				6: lambda m: self.jump(m, false),
				7: lambda m: self.binop(m, lt),
				8: lambda m: self.binop(m, eq),
				9: self.set_base
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
			except (KeyboardInterrupt, EOFError):
				print()
				break

